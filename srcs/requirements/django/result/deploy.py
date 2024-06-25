import os
import json
import asyncio
from pathlib import Path
from typing import Set, cast

from web3 import AsyncWeb3
from web3.exceptions import TimeExhausted
from web3.middleware import async_construct_simple_cache_middleware
from web3.middleware.signing import async_construct_sign_and_send_raw_middleware
from web3.middleware.cache import SIMPLE_CACHE_RPC_WHITELIST
from web3.utils.caching import SimpleCache
from web3.types import RPCEndpoint
from solcx import compile_standard, install_solc
from channels.layers import get_channel_layer

abi_path = Path(__file__).parent/"contracts" / \
    "TournamentContract.abi.json"
sol_path = Path(__file__).parent/"contracts"/"TournamentContract.sol"


class TournamentResultManager:
    _instance = None
    _init = False
    _ainit = False

    @classmethod
    async def instance(cls):
        if cls._instance is None:
            cls._instance = TournamentResultManager()
            async with cls._instance.lock:
                await cls._instance.__ainit()
        return cls._instance

    def __new__(cls, *args):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args)
        return cls._instance

    def __init__(self):
        if self._init:
            return

        self.lock = asyncio.Lock()
        self.channel_layer = get_channel_layer()
        self.pending_tx_tasks = {}

        self.chain_address = os.getenv("BLOCKCHAIN_CHAIN_ADDRESS")
        self.chain_id = os.getenv("BLOCKCHAIN_CHAIN_ID")
        self.private_key = os.getenv("BLOCKCHAIN_PRIVATE_KEY")
        self.contract_address = os.getenv("BLOCKCHAIN_CONTRACT_ADDRESS")
        self.endpoint = os.getenv("BLOCKCHAIN_ENDPOINT")

        # 디버깅용 로컬 환경 설정이 존재하면 덮어씀
        hardhat_endpoint = os.getenv("HARDHAT_ENDPOINT")
        if hardhat_endpoint:
            self.endpoint = hardhat_endpoint
            self.chain_id = os.getenv("HARDHAT_CHAIN_ID")
            self.chain_address = os.getenv("HARDHAT_ACCOUNT")
            self.private_key = os.getenv("HARDHAT_PRIVATE_KEY")
            self.contract_address = os.getenv("HARDHAT_CONTRACT_ADDRESS")

        if any(x is None for x in (self.chain_address, self.chain_id, self.private_key, self.endpoint)) or not self.chain_id.isdecimal():
            raise ValueError("Please set .env file.")

        self.chain_id = int(self.chain_id)

        # aniit에서 초기화
        self.w3 = None
        self.nonce = None
        self.contract = None

        self._init = True

    async def __ainit(self):
        if self._ainit:
            return

        # 블록체인 네트워크와 연결
        self.w3 = AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(self.endpoint))
        if not await self.w3.is_connected():
            raise ConnectionError("Cannot connect to the blockchain.")

        # 미들웨어 추가
        account = self.w3.eth.account.from_key(self.private_key)
        self.w3.middleware_onion.add(await async_construct_sign_and_send_raw_middleware(account))
        self.w3.eth.default_account = account.address

        cache = SimpleCache(256)
        CACHE_WHITELIST = cast(
            Set[RPCEndpoint],
            (
                "web3_clientVersion",
                "net_version",
                # "eth_getBlockTransactionCountByHash",
                # "eth_getUncleCountByBlockHash",
                # "eth_getBlockByHash",
                "eth_getTransactionByHash",
                "eth_getTransactionByBlockHashAndIndex",
                "eth_getRawTransactionByHash",
                "eth_getUncleByBlockHashAndIndex",
                "eth_chainId",
                "ech_call",
            ),
        )

        def should_cache_fn(method, params, _):
            if method == "eth_call" and self.contract.decode_function_input(
                    params[0]["data"])[0].fn_name == "get_tournament":
                return True
            if method in CACHE_WHITELIST:
                return True

        self.w3.middleware_onion.add(await async_construct_simple_cache_middleware(
            cache, CACHE_WHITELIST, should_cache_fn,
        ))

        self.nonce = await self.w3.eth.get_transaction_count(self.chain_address)

        if self.nonce == 0 or self.contract_address is None:
            # 컨트랙트 주소나 기록이 없으면 컴파일하고 배포
            self.__compile_sol()
            self.__backup_abi()
            await self.__deploy_contract()
        else:
            with open(abi_path, 'r', encoding="utf-8") as file:
                self.abi = file.read()
        self.contract = self.w3.eth.contract(
            address=self.contract_address, abi=self.abi)

        self._ainit = True

    @ classmethod
    def _reset(cls):
        cls._instance = None
        cls._init = False
        cls._ainit = False

    def __compile_sol(self):
        solc_version = os.getenv("SOLC_VERSION")
        install_solc(solc_version)

        if not sol_path.exists():
            raise FileNotFoundError("Cannot find .sol file.")
        with open(sol_path, "rt", encoding="utf-8") as file:
            tournament_sol_data = file.read()

        compiled_sol = compile_standard({
            "language": "Solidity",
            "sources": {"TournamentContract.sol": {"content": tournament_sol_data}},
            "settings": {
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                    }
                }
            },
        }, solc_version=solc_version)

        contract_info = compiled_sol["contracts"]["TournamentContract.sol"]["TournamentContract"]
        self.abi = contract_info["abi"]
        self.bytecode = contract_info["evm"]["bytecode"]["object"]

    async def __deploy_contract(self):
        """
        Deploy the contract to the blockchain.
        초기 배포나 컨트랙트 어드레스가 없을시 사용하므로 트랜잭션을 기다림
        """
        nonce = await self.w3.eth.get_transaction_count(self.chain_address)

        tournament = self.w3.eth.contract(abi=self.abi, bytecode=self.bytecode)
        tx = {
            "chainId": self.chain_id,
            "gasPrice": await self.w3.eth.gas_price,
            "nonce": nonce,
        }
        tx_hash = await tournament.constructor().transact(tx)
        tx_receipt = await self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120, poll_latency=1)
        self.contract_address = tx_receipt["contractAddress"]
        self.nonce = nonce + 1

    def __backup_abi(self):
        with open(abi_path, "wt", encoding="utf-8") as file:
            file.write(json.dumps(self.abi))

    async def __transact(self, func: str, *args):
        async with self.lock:
            nonce = self.nonce

            tx = {
                "chainId": self.chain_id,
                "gasPrice": await self.w3.eth.gas_price,
                # "from": self.chain_address,
                "nonce": nonce,
            }
            tx_hash = await getattr(self.contract.functions, func)(*args).transact(tx)
            self.pending_tx_tasks[tx_hash] = {
                "task": asyncio.create_task(self.__transact_task(tx_hash)),
                "nonce": nonce,
                "func": func,
                "args": args,
            }
            self.nonce += 1

    async def __transact_task(self, tx_hash):
        try:
            nonce = self.pending_tx_tasks[tx_hash]["nonce"]
            tx_receipt = await self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120, poll_latency=5)
        except TimeExhausted:
            # 대충 리트라이 - 재시도할때는 락걸고 독점적으로 실행
            print(f"Transaction {nonce} timeout.")
            return
        finally:
            async with self.lock:
                self.pending_tx_tasks.pop(tx_hash)

    async def __call(self, func, *args):
        return await getattr(self.contract.functions, func)(*args).call()

    async def __retry(self, func, *args, attempts=3):
        # 어떻게 만들지..
        pass

    async def _wait_all(self):
        await asyncio.gather(*map(lambda x: x["task"], self.pending_tx_tasks.values()))

    async def start_game(self, game_id, timestamp, players):
        hash = await self.__transact(
            "add_game", game_id, timestamp, players)

    async def save_sub_game(self, game_id, sub_game_info):
        hash = await self.__transact(
            "add_sub_game", game_id, sub_game_info)

    async def get_tournament(self, game_id):
        return await self.__call("get_tournament", game_id)

    async def get_all_tournaments(self):
        # TODO: 요청 최적화 필요
        # 여기 요청이 너무 많으면 429 Too Many Requests 에러 발생할 수 있음
        tournaments = await self.__call("get_valid_tournaments")
        return await asyncio.gather(*map(self.get_tournament, tournaments))

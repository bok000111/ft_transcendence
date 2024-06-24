import os
import json
from web3 import Web3
from solcx import compile_standard, install_solc
from django.conf import settings

abi_path = settings.BASE_DIR / "blockchain" / "abi.json"
sol_path = settings.BASE_DIR / "blockchain" / "TournamentContract.sol"


class TournamentResultManager:
    _instance = None
    _initialized = False

    def __new__(cls, *args):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, provider):
        if self._initialized:
            return

        self.chain_address = os.getenv("CHAIN_ADDRESS")
        self.private_key = os.getenv("PRIVATE_KEY")
        self.chain_id = os.getenv("CHAIN_ID")
        if self.chain_address is None or self.private_key is None or self.chain_id is None:
            raise ValueError(
                "Please set the CHAIN_ADDRESS, PRIVATE_KEY and CHAIN_ID in the .env file.")
        self.chain_id = int(self.chain_id)

        self.w3 = Web3(Web3.HTTPProvider(provider))

        if (
            self.w3.eth.get_transaction_count(self.chain_address) == 0
            or os.getenv("CONTRACT_ADDRESS") == ""
        ):
            self.__set_initial_settings()

        else:
            with open(abi_path, 'r', encoding="utf-8") as file:
                self.abi = file.read()
            self.contract_address = os.getenv("CONTRACT_ADDRESS")
        self._initialized = True

    def __set_initial_settings(self):
        bytecode = self.__compile_sol()
        contract_address = self.__deploy_contract(bytecode)
        self.contract_address = str(contract_address)
        print("The contract address is as follows: " + self.contract_address)
        print(
            "Set the above contract address as the CONTRACT_ADDRESS in the .env file."
        )

    def __compile_sol(self):
        solc_version = "0.6.0"
        install_solc(solc_version)
        # sol_path = os.path.join(
        #     settings.BASE_DIR, "/blockchain/TournamentContract.sol")
        try:
            with open(sol_path, "rt", encoding="utf-8") as file:
                tournament_file = file.read()
        except Exception as e:
            print(e)
            return None

        compiled_sol = compile_standard(
            {
                "language": "Solidity",
                "sources": {"TournamentContract.sol": {"content": tournament_file}},
                "settings": {
                    "outputSelection": {
                        "*": {
                            "*": [
                                "abi",
                                "metadata",
                                "evm.bytecode",
                                "evm.bytecode.sourceMap",
                            ]
                        }
                    }
                },
            },
            solc_version=solc_version,
        )
        self.abi = compiled_sol["contracts"]["TournamentContract.sol"][
            "TournamentContract"
        ]["abi"]
        bytecode = compiled_sol["contracts"]["TournamentContract.sol"][
            "TournamentContract"
        ]["evm"]["bytecode"]["object"]

        # for get abi
        if abi_path.exists() is False:
            with open(abi_path, "w", encoding="utf-8") as file:
                json.dump(self.abi, file)
        return bytecode

    def __deploy_contract(self, bytecode):
        nonce = self.w3.eth.get_transaction_count(self.chain_address)

        tournament = self.w3.eth.contract(abi=self.abi, bytecode=bytecode)
        transaction = tournament.constructor().build_transaction(
            {
                "chainId": self.chain_id,
                "gasPrice": self.w3.eth.gas_price,
                "from": self.chain_address,
                "nonce": nonce,
            }
        )
        signed_txn = self.w3.eth.account.sign_transaction(
            transaction, private_key=self.private_key
        )
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt.contractAddress

    def start_game(self, game_id, timestamp, players):
        nonce = self.w3.eth.get_transaction_count(self.chain_address)
        started_game = self.w3.eth.contract(
            address=self.contract_address, abi=self.abi)
        tx = started_game.functions.add_game(
            game_id, timestamp, players
        ).build_transaction(
            {
                "chainId": self.chain_id,
                "gasPrice": self.w3.eth.gas_price,
                "from": self.chain_address,
                "nonce": nonce,
            }
        )
        signed_txn = self.w3.eth.account.sign_transaction(
            tx, private_key=self.private_key
        )
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        # print(started_game.functions.test_start(id).call())
        return tx_receipt

    def save_sub_game(self, game_id, sub_game_info):
        nonce = self.w3.eth.get_transaction_count(self.chain_address)
        sub_game = self.w3.eth.contract(
            address=self.contract_address, abi=self.abi)
        tx = sub_game.functions.add_sub_game(game_id, sub_game_info).build_transaction(
            {
                "chainId": self.chain_id,
                "gasPrice": self.w3.eth.gas_price,
                "from": self.chain_address,
                "nonce": nonce,
            }
        )
        signed_txn = self.w3.eth.account.sign_transaction(
            tx, private_key=self.private_key
        )
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        # print(sub_game.functions.test_sub(id).call())
        return tx_receipt

    def get_all_tournaments(self):
        cont = self.w3.eth.contract(
            address=self.contract_address, abi=self.abi)
        valid_tournaments = cont.functions.get_valid_tournaments().call()
        all_tournaments = []
        for game_id in valid_tournaments:
            tournament_info = cont.functions.get_tournament(game_id).call()
            all_tournaments.append(tournament_info)
        return all_tournaments


# tournament_contract = TournamentResultManager(
#     "../../blockchain/TournamentContract.sol", os.getenv("ENDPOINT"))

# tournament_contract.start_game(4, 1695940800, [262, 4, 9, 11])
# tournament_contract.save_sub_game(4, [2, 8, 10])
# tournament_contract.save_sub_game(4, [3, 10, 2])
# tournament_contract.save_sub_game(4, [1, 7, 10])

# a = tournament_contract.get_all_tournaments()
# print(a)

# for res in a:
#     print(TournamentResult(res))

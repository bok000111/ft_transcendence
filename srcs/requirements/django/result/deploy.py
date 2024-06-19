from result import *
import json
from web3 import Web3
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv
from django.conf import settings


class TournamentResultManager:
    _instance = None
    _initialized = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, provider):
        if self._initialized:
            return

        load_dotenv()
        self.chain_address = os.getenv("CHAIN_ADDRESS")
        self.private_key = os.getenv("PRIVATE_KEY")
        if self.chain_address == "" or self.private_key == "":
            print("Please set the CHAIN_ADDRESS and PRIVATE_KEY in the .env file.")
            return
        self.w3 = Web3(Web3.HTTPProvider(provider))
        self.chain_id = 1337

        if self.w3.eth.get_transaction_count(self.chain_address) == 0 or os.getenv("CONTRACT_ADDRESS") == "":
            self.__set_initial_settings()
        else:
            with open(str(settings.BASE_DIR) + "/../blockchain/abi.json", 'r', encoding='utf-8') as file:
                self.abi = file.read()
            self.contract_address = os.getenv("CONTRACT_ADDRESS")

    def __set_initial_settings(self):
        bytecode = self.__compile_sol()
        contract_address = self.__deploy_contract(bytecode)
        self.contract_address = str(contract_address)
        print("The contract address is as follows: " + self.contract_address)
        print("Set the above contract address as the CONTRACT_ADDRESS in the .env file.")

    def __compile_sol(self):
        solc_version = "0.6.0"
        install_solc(solc_version)
        sol_path = str(settings.BASE_DIR) + \
            "/../blockchain/TournamentContract.sol"
        try:
            with open(sol_path, "rt", encoding='utf-8') as file:
                tournament_file = file.read()
        except Exception as e:
            print(e)
            return

        compiled_sol = compile_standard(
            {
                "language": "Solidity",
                "sources": {"TournamentContract.sol": {"content": tournament_file}},
                "settings": {
                    "outputSelection": {
                        "*": {
                            "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                        }
                    }
                },
            },
            solc_version=solc_version,
        )
        self.abi = compiled_sol["contracts"]["TournamentContract.sol"]["TournamentContract"]["abi"]
        bytecode = compiled_sol["contracts"]["TournamentContract.sol"]["TournamentContract"]["evm"]["bytecode"]["object"]

        # for get abi
        if not os.path.exists(str(settings.BASE_DIR) + "/../blockchain/abi.json"):
            with open(str(settings.BASE_DIR) + "/../blockchain/abi.json", "w") as file:
                json.dump(self.abi, file)
        return bytecode

    def __deploy_contract(self, bytecode):
        nonce = self.w3.eth.get_transaction_count(self.chain_address)

        Tournament = self.w3.eth.contract(abi=self.abi, bytecode=bytecode)
        transaction = Tournament.constructor().build_transaction(
            {
                "chainId": self.chain_id,
                "gasPrice": self.w3.eth.gas_price,
                "from": self.chain_address,
                "nonce": nonce
            }
        )
        signed_txn = self.w3.eth.account.sign_transaction(
            transaction, private_key=self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt.contractAddress

    def start_game(self, id, timestamp, players):
        nonce = self.w3.eth.get_transaction_count(self.chain_address)
        started_game = self.w3.eth.contract(
            address=self.contract_address, abi=self.abi)
        tx = started_game.functions.add_game(id, timestamp, players).build_transaction(
            {
                "chainId": self.chain_id,
                "gasPrice": self.w3.eth.gas_price,
                "from": self.chain_address,
                "nonce": nonce
            }
        )
        signed_txn = self.w3.eth.account.sign_transaction(
            tx, private_key=self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        # print(started_game.functions.test_start(id).call())
        return tx_receipt

    def save_sub_game(self, id, sub_game_info):
        nonce = self.w3.eth.get_transaction_count(self.chain_address)
        sub_game = self.w3.eth.contract(
            address=self.contract_address, abi=self.abi)
        tx = sub_game.functions.add_sub_game(id, sub_game_info).build_transaction(
            {
                "chainId": self.chain_id,
                "gasPrice": self.w3.eth.gas_price,
                "from": self.chain_address,
                "nonce": nonce
            }
        )
        signed_txn = self.w3.eth.account.sign_transaction(
            tx, private_key=self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        # print(sub_game.functions.test_sub(id).call())
        return tx_receipt

    def get_all_tournaments(self):
        cont = self.w3.eth.contract(
            address=self.contract_address, abi=self.abi)
        valid_tournaments = cont.functions.get_valid_tournaments().call()
        all_tournaments = []
        for id in valid_tournaments:
            tournament_info = cont.functions.get_tournament(id).call()
            all_tournaments.append(tournament_info)
        return all_tournaments


# tournament_contract = TournamentResultManager(
#     "../../blockchain/TournamentContract.sol", os.getenv("GANACHE_URL"))

# tournament_contract.start_game(4, 1625940800, [263, 456, 989, 1011])
# tournament_contract.save_sub_game(4, [2, 10, 1])
# tournament_contract.save_sub_game(4, [3, 2, 10])
# tournament_contract.save_sub_game(4, [1, 4, 10])

# a = tournament_contract.get_all_tournaments()
# print(a)

# for res in a:
#     print(TournamentResult(res))

import json
from web3 import Web3
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv
from TournamentResult import TournamentResult

class TournamentResultManager:
    def __init__(self, sol_path, provider):
        self.solc_version = "0.6.0"
        self.w3 = Web3(Web3.HTTPProvider(provider))
        self.chain_address = os.getenv("CHAIN_ADDRESS")
        self.private_key = os.getenv("PRIVATE_KEY")
        self.abi = os.getenv("ABI")
        # self.__compile_sol(sol_path)
        self.chain_id = 1337
        receipt = self.__deploy_contract(sol_path)
        if receipt == None:
            self.contract_address = os.getenv("CONTRACT_ADDRESS")
        else:
            self.contract_address = str(receipt.contractAddress)


    def __compile_sol(self, sol_path):
        install_solc(self.solc_version)
        with open(sol_path, "rt", encoding='UTF8') as file:
            tournament_file = file.read()
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
            solc_version=self.solc_version,
        )
        bytecode = compiled_sol["contracts"]["TournamentContract.sol"]["TournamentContract"]["evm"]["bytecode"]["object"]
        self.abi = compiled_sol["contracts"]["TournamentContract.sol"]["TournamentContract"]["abi"]
        # for get abi
        with open("abi.json", "w") as file:
            json.dump(self.abi, file)
        return bytecode

    def __deploy_contract(self, sol_path):
        nonce = self.w3.eth.get_transaction_count(self.chain_address)
        if nonce != 0:
            print("Contract already deployed")
            return None
        bytecode = self.__compile_sol(sol_path)
        Tournament = self.w3.eth.contract(abi=self.abi, bytecode=bytecode)
        transaction = Tournament.constructor().build_transaction(
            {
                "chainId": self.chain_id,
                "gasPrice": self.w3.eth.gas_price,
                "from": self.chain_address,
                "nonce": nonce,
            }
        )
        signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key=self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        print(tx_receipt.contractAddress)
        return tx_receipt.contractAddress

    def start_game(self, id, timestamp, players):
        nonce = self.w3.eth.get_transaction_count(self.chain_address)
        started_game = self.w3.eth.contract(address=self.contract_address, abi=self.abi)
        tx = started_game.functions.add_game(id, timestamp, players).build_transaction(
            {
                "chainId": self.chain_id,
                "gasPrice": self.w3.eth.gas_price,
                "from": self.chain_address,
                "nonce": nonce,
            }
        )
        signed_txn = self.w3.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        # print(started_game.functions.test_start(id).call())
        return tx_receipt
    
    def save_sub_game(self, id, sub_game_info):
        nonce = self.w3.eth.get_transaction_count(self.chain_address)
        sub_game = self.w3.eth.contract(address=self.contract_address, abi=self.abi)
        tx = sub_game.functions.add_sub_game(id, sub_game_info).build_transaction(
            {
                "chainId": self.chain_id,
                "gasPrice": self.w3.eth.gas_price,
                "from": self.chain_address,
                "nonce": nonce
            }
        )
        signed_txn = self.w3.eth.account.sign_transaction(tx, private_key=self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        # print(sub_game.functions.test_sub(id).call())
        return tx_receipt
    
    def get_all_tournaments(self):
        cont = self.w3.eth.contract(address=self.contract_address, abi=self.abi)
        valid_tournaments = cont.functions.get_valid_tournaments().call()
        all_tournaments = []
        for id in valid_tournaments:
            tournament_info = cont.functions.get_tournament(id).call()
            all_tournaments.append(tournament_info)
        return all_tournaments

# Usage
load_dotenv() 
tournament_contract = TournamentResultManager("./TournamentContract.sol", os.getenv("GANACHE_URL"))
tournament_contract.start_game(20, 1625940800, [263, 456, 989, 1011])
tournament_contract.save_sub_game(20, [2, 10, 1])
tournament_contract.save_sub_game(20, [3, 2, 10])
tournament_contract.save_sub_game(20, [1, 4, 10])

a = tournament_contract.get_all_tournaments()
print(a)

for res in a:
    print(TournamentResult(res))

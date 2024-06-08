import json
from web3 import Web3
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv

# 1. 초기에 Smart contract를 배포하는 함수(1번만 하면 됨)
# 2. 받은 결과를 바탕으로 contract 객체를 배포하는 함수(tournament가 끝나는 시점마다 실행)
# 3. 현재 있는 contract 객체를 바탕으로 저장된 결과들을 가공해서 frontend에 던지는 함수
class TournamentContract:
    def __init__(self, sol_path, provider):
        self.solc_version = "0.6.0"
        self.w3 = Web3(Web3.HTTPProvider(provider))
        self.chain_id = 1337
        self.chain_address = os.getenv("ADDRESS")
        self.private_key = os.getenv("PRIVATE_KEY")
        self.bytecode = None
        self.abi = None
        self.__compile_sol(sol_path)

    def __compile_sol(self, sol_path):
        install_solc(self.solc_version)
        with open(sol_path, "rt", encoding='UTF8') as file:
            tournament_file = file.read()
        compiled_sol = compile_standard(
            {
                "language": "Solidity",
                "sources": {"TournamentManager.sol": {"content": tournament_file}},
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
        self.bytecode = compiled_sol["contracts"]["TournamentManager.sol"]["TournamentManager"]["evm"]["bytecode"]["object"]
        # for get bytecode
        with open("bytecode.json", "w") as file:
            json.dump(self.bytecode, file)
        self.abi = compiled_sol["contracts"]["TournamentManager.sol"]["TournamentManager"]["abi"]
        
        # for get abi
        # with open("abi.json", "w") as file:
        #     json.dump(self.abi, file)

    def deploy_contract(self):
        Tournament = self.w3.eth.contract(abi=self.abi, bytecode=self.bytecode)
        nonce = self.w3.eth.get_transaction_count(self.chain_address)
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
        self.tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        return self.tx_receipt.contractAddress

    def start_game(self, id, timestamp, players):
        nonce = self.w3.eth.get_transaction_count(self.chain_address)
        started_game = self.w3.eth.contract(address=self.tx_receipt.contractAddress, abi=self.abi)
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
        sub_game = self.w3.eth.contract(address=self.tx_receipt.contractAddress, abi=self.abi)
        tx = sub_game.functions.add_sub_game(id, sub_game_info).build_transaction(
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
        # print(sub_game.functions.test_sub(id).call())
        return tx_receipt
    
    def get_all_tournaments(self):
        cont = self.w3.eth.contract(address=self.tx_receipt.contractAddress, abi=self.abi)
        valid_tournaments = cont.functions.get_valid_tournaments().call()
        print(valid_tournaments)
        all_tournaments = []
        for id in valid_tournaments:
            tournament_info = cont.functions.get_tournament(id).call()
            all_tournaments.append(tournament_info)
        return all_tournaments

# Usage
load_dotenv()
tournament_contract = TournamentContract("./TournamentManager.sol", os.getenv("GANACHE_URL"))
contract_address = tournament_contract.deploy_contract()
print(f"Contract deployed at address: {contract_address}")
tournament_contract.start_game(12, 1625140800, [123, 456, 789, 1011])
tournament_contract.save_sub_game(12, [2, 123, 456, 1, 10])
tournament_contract.save_sub_game(12, [3, 789, 1011, 10, 5])
tx_receipt = tournament_contract.save_sub_game(12, [1, 456, 789, 3, 10])
a = tournament_contract.get_all_tournaments()
print(a)


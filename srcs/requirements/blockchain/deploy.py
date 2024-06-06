import json
from web3 import Web3
from solcx import compile_standard, install_solc
import os
from dotenv import load_dotenv

load_dotenv()
install_solc("0.6.0"),
with open("./Tournament.sol", "r") as file:
    tournament_file = file.read()

# Compile Our Solidity
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"Tournament.sol": {"content": tournament_file}},
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.6.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# Get Bytecode
bytecode = compiled_sol["contracts"]["Tournament.sol"]["Tournament"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["Tournament.sol"]["Tournament"]["abi"]

# For connecting to Ganache
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id = 1337
my_address = os.getenv("ADDRESS")
private_key = os.getenv("PRIVATE_KEY")
print(w3)

Tournament = w3.eth.contract(abi=abi, bytecode=bytecode)
print(Tournament)

# Get the latest transaction
nonce = w3.eth.get_transaction_count(my_address)

# 1. Build a transaction
# 2. Sign a transaction
# 3. Send a transaction
transaction = Tournament.constructor().build_transaction(
    {
        "chainId": chain_id,
        "gasPrice": w3.eth.gas_price,
        "from": my_address,
        "nonce": nonce,
    }
)
print(transaction)

signed_txn = w3.eth.account.sign_transaction(
    transaction, private_key=private_key)

tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

tournament = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

store_transaction = tournament.functions.setFinishedRound(10).build_transaction(
    {"chainId": chain_id, "from": my_address,
        "nonce": nonce + 1, "gasPrice": w3.eth.gas_price}
)
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)

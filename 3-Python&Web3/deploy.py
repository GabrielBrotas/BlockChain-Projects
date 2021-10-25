from solcx import compile_standard
from web3 import Web3
from dotenv import load_dotenv
import json
import os

load_dotenv()

# whit this file, we will 'r' => read, and execute the following
with open("./SimpleStorage.sol", "r") as file:
    # we are going to execute some code and after this we close this file
    simple_storage_file = file.read()


compile_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
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

# w => write a data
with open("compiled_code.json", "w") as file:
    # put the compile_sol data in this file
    json.dump(compile_sol, file)

# get bytecode
bytecode = compile_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compile_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]


# connect with blockchain ganache
# w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))  # RCP Server Localhost
w3 = Web3(Web3.HTTPProvider("https://rinkeby.infura.io/v3/88330c4f8444451db2ddfd0a877ec814"))  # RCP Server
# chain_id = 1337  # Network ID Localhost
chain_id=4 # search the chain id of host you connecting, in this case 4 is from rinkeby
my_address = "0xA10f23bFf599AE4ce7e73d39A4b4BCFf118b7A3f"  # any address
private_key = os.getenv("PRIVATE_KEY") # transform the password in a hex10

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# Get latest transaction
nonce = w3.eth.getTransactionCount(my_address)

print(' call 1 -------')

# 1. Build a transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chain_id, "from": my_address, "nonce": nonce}
)

# 2.  Sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# 3. send this signed transaction
tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction) # this code will send our transaction to blockchain
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash) 

# working with the contract
simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# we can interact with the call or the transact
# Call => simulate making the call and getting an return value, doesnt make a state change
# Transact => actually make a state change
print(simple_storage.functions.retrieve().call()) # 0, initial value from storaged number
simple_storage.functions.store(15).call()
print(simple_storage.functions.retrieve().call()) # still 0 because the call does not change the state

print(' call 2 -------')

# 1 - Build transaction
store_transaction = simple_storage.functions.store(15).buildTransaction({
    "chainId": chain_id,
    "from": my_address,
    "nonce": nonce + 1 # we need to plus the nonce because we already used once so we cant repeat
})
# 2 - Sign transaction
signed_store_tx = w3.eth.account.sign_transaction(store_transaction, private_key=private_key)

# 3 - Send transaction signed
send_store_tx = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print(simple_storage.functions.retrieve().call()) # 15

# Contract Address

# Contract ABI

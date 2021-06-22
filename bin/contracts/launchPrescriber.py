import os
import json

from web3 import Web3

# Initiate w3
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
w3.isConnected()

with open(os.path.join('Prescriber.abi'), 'r') as file:
    prescriber_abi = json.load(file)
    print(prescriber_abi)

with open(os.path.join('Prescriber.bin'), 'rb') as file:
    prescriber_bytecode = file.read()
    print(prescriber_bytecode)

testContract = w3.eth.contract(abi=prescriber_abi, bytecode=prescriber_bytecode)

tx_hash = testContract.constructor().transact(contractOwner=w3.eth.get_accounts[0], newNpi=1811054877)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

prescriber = w3.eth.contract(address=tx_receipt.contractAddress, abi=prescriber_abi)

print(w3.eth.get_transaction_receipt(testContract)['contractAddress'])
import json

from web3 import Web3
from solc import compile_standard


standard_json = {
    "language": "Solidity",
    "sources": {
        "Greeter.sol": {
            "content": ""
        }
    },
    "settings":
    {
        "outputSelection": {
            "*": {
                "*": [
                    "metadata", "evm.bytecode", "evm.bytecode.sourceMap"
                ]
            }
        }
    }
}

with open('contracts/Greeter.sol') as file:
    source_code = file.read()

standard_json['sources']['Greeter.sol']['content'] = source_code

compiled_sol = compile_standard(standard_json)

w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
w3.eth.default_account = w3.eth.accounts[0]

bytecode = compiled_sol['contracts']['Greeter.sol']['Greeter']['evm']['bytecode']['object']
abi = json.loads(compiled_sol['contracts']['Greeter.sol']['Greeter']['metadata'])['output']['abi']

try:
    Greeter = w3.eth.contract(abi=abi, bytecode=bytecode)

    tx_hash = Greeter.constructor().transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    greeter = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
    print(greeter.functions.greet().call())

    tx_hash = greeter.functions.setGreeting('Nihao').transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(greeter.functions.greet().call())
except Exception as e:
    print('abi:\n', abi, '\n\n')
    print('error:\n', e, '\n\n')
import json
import os
import time

from web3 import Web3
from solc import compile_standard


def compile(contracts, dir):
    standard_json = {
        'language': 'Solidity',
        'sources': {},
        'settings':
        {
            'outputSelection': {
                '*': {
                    '*': [
                        'metadata', 'evm.bytecode', 'evm.bytecode.sourceMap'
                    ]
                }
            }
        }
    }

    for contract in contracts:
        with open(os.path.join(dir, contract)) as file:
            source = file.read()
            standard_json['sources'][contract] = {'content': ''}
            standard_json['sources'][contract]['content'] = source

    return compile_standard(standard_json)


def deploy(contracts, dir, host):
    compiled_sol = compile(contracts, dir)

    w3 = Web3(Web3.HTTPProvider(host))
    w3.eth.default_account = w3.eth.accounts[0]

    for contract in contracts:
        name = contract.replace('.sol', '')

        bytecode = compiled_sol['contracts'][contract][name]['evm']['bytecode']['object']
        abi = json.loads(compiled_sol['contracts'][contract][name]['metadata'])['output']['abi']

        Contract = w3.eth.contract(abi=abi, bytecode=bytecode)

        if contract == 'Prescriber.sol':
            tx_hash = Contract.constructor(w3.eth.accounts[0], 1811054877).transact()
        elif contract == 'Prescription.sol':
            tx_hash = Contract.constructor(w3.eth.accounts[1], 23, 43, 35).transact()

        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        deployed_contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
        print(f'Success: Deployed {contract} at address {deployed_contract.address}')


if __name__ == '__main__':
    deploy(['Prescriber.sol', 'Prescription.sol'], 'contracts', 'http://localhost:8545')

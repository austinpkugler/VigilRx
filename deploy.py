import json
import os
import time

from web3 import Web3
from solc import compile_standard


def compile():
    start = time.time()

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

    contracts = os.listdir(os.path.join('contracts'))
    print(contracts)
    for contract in contracts:
        with open(os.path.join('contracts', contract)) as file:
            source = file.read()
            standard_json['sources'][contract] = {'content': ''}
            standard_json['sources'][contract]['content'] = source

    try:
        compiled_sol = compile_standard(standard_json)
        runtime = round(time.time() - start, 2)
        print(f'Success: Compiled {len(contracts)} contracts in {runtime}s')
    except Exception as e:
        print(f'Error: Compilation failed\n\t{e}')

    # with open('save.json', 'w') as file:
    #     json.dump(compiled_sol, file, indent=4)

    return contracts, compiled_sol


def deploy():
    contracts, compiled_sol = compile()

    w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
    w3.eth.default_account = w3.eth.accounts[0]

    print(f'Status: Deploying {len(contracts)} contracts')
    for contract in contracts:
        try:
            name = contract.replace('.sol', '')
            bytecode = compiled_sol['contracts'][contract][name]['evm']['bytecode']['object']
            abi = json.loads(compiled_sol['contracts'][contract][name]['metadata'])['output']['abi']
            Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
            tx_hash = Contract.constructor().transact()
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            deployed_contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
            print(f'Success: Deployed {contract} at address {deployed_contract.address}')
        except Exception as e:
            print(f'Error: Deployment failed on {contract}\n\t{e}')


if __name__ == '__main__':
    deploy()

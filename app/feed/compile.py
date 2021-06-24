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
        with open(os.path.join('..', '..', 'contracts', contract)) as file:
            source = file.read()
            standard_json['sources'][contract] = {'content': ''}
            standard_json['sources'][contract]['content'] = source

    compiled_sol = compile_standard(standard_json)

    for contract in contracts:
        name = contract.replace('.sol', '')
        bytecode = compiled_sol['contracts'][contract][name]['evm']['bytecode']['object']
        abi = json.loads(compiled_sol['contracts'][contract][name]['metadata'])['output']['abi']

        with open(os.path.join('..', '..', 'contracts', name + '.abi'), 'w') as file:
            json.dump(abi, file, indent=4)
        with open(os.path.join('..', '..', 'contracts', name + '.bin'), 'w') as file:
            file.write(bytecode)


if __name__ == '__main__':
    compile(['Prescriber.sol', 'Prescription.sol'], 'contracts')

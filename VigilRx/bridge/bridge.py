import json
import os

from web3 import Web3

import errors


try:
    with open(os.path.join('build', 'Registrar.abi'), 'r') as file:
        _REGISTRAR_ABI = json.load(file)
    with open(os.path.join('build', 'Registrar.bin'), 'r') as file:
        _REGISTRAR_BIN = file.read()
except Exception as e:
    raise errors.NotCompiledException()

try:
    w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
    w3.eth.default_account = w3.eth.accounts[0]
except:
    raise errors.GanacheException()


def new_registrar():
    contract = w3.eth.contract(abi=_REGISTRAR_ABI, bytecode=_REGISTRAR_BIN)
    tx_hash = contract.constructor().transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    registrar_contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=_REGISTRAR_ABI)
    with open(os.path.join('build', 'bridge.json'), 'w') as file:
        json.dump({'grc_address': registrar_contract.address}, file, indent=4)


if __name__ == '__main__':
    new_registrar()

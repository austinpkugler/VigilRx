from VigilRx.bridge.errors import GanacheException
import json
import os

from web3 import Web3

from VigilRx.bridge.errors import NotCompiledException, GanacheException


try:
    with open(os.path.join('build', 'Prescriber.abi'), 'r') as file:
        _PRESCRIBER_ABI = json.load(file)
    with open(os.path.join('build', 'Prescriber.bin'), 'r') as file:
        _PRESCRIBER_BIN = file.read()
except Exception as e:
    raise NotCompiledException()

w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))


def new_prescriber(instance):
    print(f'Prescriber(instance={instance}, role={instance.role}, address={instance.address})')
    # """Deploys a new prescriber contract to the Ganache blockchain.

    # :param prescriber_info: Dictionary of prescriber info, including a
    #     personal address and National Provider Identifier.
    # :type prescriber_info: dict
    # :return: Address of now deployed prescriber contract.
    # :rtype: str
    # """
    # try:
    #     w3.eth.default_account = prescriber_info['address']
    # except:
    #     raise GanacheException()

    # contract = w3.eth.contract(abi=_PRESCRIBER_ABI, bytecode=_PRESCRIBER_BIN)
    # tx_hash = contract.constructor(prescriber_info['address'], int(prescriber_info['identifier'])).transact()
    # tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    # prescriber_contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=_PRESCRIBER_ABI)
    # return prescriber_contract.address


def new_prescription():
    pass


def refill_prescription():
    pass

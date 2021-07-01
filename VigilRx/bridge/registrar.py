import json
import os

from web3 import Web3

import config
import errors


try:
    with open(os.path.join('build', 'Registrar.abi'), 'r') as file:
        _REGISTRAR_ABI = json.load(file)
    with open(os.path.join('build', 'Registrar.bin'), 'r') as file:
        _REGISTRAR_BIN = file.read()
except Exception as e:
    raise errors.NotCompiledException()

try:
    w3 = Web3(Web3.HTTPProvider(config.PORT))
    w3.eth.default_account = w3.eth.accounts[0]
except:
    raise errors.GanacheException()


def new_patient(instance):
    registrar_contract = w3.eth.contract(address=config.GRC, abi=_REGISTRAR_ABI)
    tx_hash = registrar_contract.functions.createPatient(instance.address).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print('\n\n', registrar_contract.events.NewAddress().processReceipt(tx_receipt))
    # print(f'Patient(instance={instance}, role={instance.role}, address={instance.address}, contract={patient_address})')
    # return patient_address


def new_pharmacy(instance):
    print(f'Pharmacy(instance={instance}, role={instance.role}, address={instance.address})')


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

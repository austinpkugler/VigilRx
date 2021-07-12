import json
import os

from web3 import Web3

import errors


try:
    with open(os.path.join('build', 'Registrar.abi'), 'r') as file:
        _REGISTRAR_ABI = json.load(file)
    with open(os.path.join('build', 'bridge.json'), 'r') as file:
        _GRC_ADDRESS = json.load(file)['grc_address']
except Exception as e:
    raise errors.NotCompiledException()

try:
    w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
    w3.eth.default_account = w3.eth.accounts[0]
except:
    raise errors.GanacheException()

REGISTRAR_CONTRACT = w3.eth.contract(address=_GRC_ADDRESS, abi=_REGISTRAR_ABI)


def new_patient(instance):
    tx_hash = REGISTRAR_CONTRACT.functions.createPatient(instance.address).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    patient_contract = str(REGISTRAR_CONTRACT.events.NewAddress().processReceipt(tx_receipt)[0]['args']['contractAddress'])
    print(f'Patient(role={instance.role}, address={instance.address}, contract={patient_contract})')
    return patient_contract


def new_prescriber(instance):
    tx_hash = REGISTRAR_CONTRACT.functions.createPharmacy(instance.address, int(instance.identifier)).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    prescriber_contract = str(REGISTRAR_CONTRACT.events.NewAddress().processReceipt(tx_receipt)[0]['args']['contractAddress'])
    print(f'Prescriber(role={instance.role}, address={instance.address}, contract={prescriber_contract}, identifier={instance.identifier}))')
    return prescriber_contract


def new_pharmacy(instance):
    tx_hash = REGISTRAR_CONTRACT.functions.createPharmacy(instance.address, int(instance.identifier)).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    pharmacy_contract = str(REGISTRAR_CONTRACT.events.NewAddress().processReceipt(tx_receipt)[0]['args']['contractAddress'])
    print(f'Pharmacy(role={instance.role}, address={instance.address}, contract={pharmacy_contract}, identifier={instance.identifier})')
    return pharmacy_contract

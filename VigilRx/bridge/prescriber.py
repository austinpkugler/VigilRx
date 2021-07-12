import json
import os

from web3 import Web3

import errors


try:
    with open(os.path.join('build', 'Prescriber.abi'), 'r') as file:
        _PRESCRIBER_ABI = json.load(file)
except Exception as e:
    raise errors.NotCompiledException()

try:
    w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
except:
    raise errors.GanacheException()


def new_prescription(prescriber_address, patient_address, ndc, quantity, refills):
    w3.eth.default_account = w3.eth.accounts[1]
    prescriber_contract = w3.eth.contract(address=prescriber_address, abi=_PRESCRIBER_ABI)
    tx_hash = prescriber_contract.functions.npi().transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)

    # tx_hash = prescriber_contract.functions.createPrescription(patient_address, ndc, quantity, refills).transact()
    # tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    # prescription_contract = str(prescriber_contract.events.NewAddress().processReceipt(tx_receipt)[0]['args']['contractAddress'])
    # print(f'Prescription(prescriber={prescriber_address}, patient={patient_address}, contract={prescription_contract}, ndc={ndc})')
    # return prescription_contract


new_prescription(
    '0x44e166fc0Ad2ec0A8dB2265aE6B4908d2a010e39', # The prescriber role contract
    '', # The patient role contract
    434,
    2,
    10
)

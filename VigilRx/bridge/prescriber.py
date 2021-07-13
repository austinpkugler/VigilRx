import json
import os

from web3 import Web3

import errors


try:
    with open(os.path.join('build', 'Prescriber.abi'), 'r') as file:
        _PRESCRIBER_ABI = json.load(file)
    with open(os.path.join('build', 'Patient.abi'), 'r') as file:
        _PATIENT_ABI = json.load(file)
except Exception as e:
    raise errors.NotCompiledException()

try:
    w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
except:
    raise errors.GanacheException()


def new_prescription(prescriber_address, patient_address, ndc, quantity, refills):
    pass


def test_new_prescription():
    ndc = 1294
    quantity = 2
    refills = 13

    prescriber_personal_address = '0x95535f1c5652Ac0858838f1ad76c38eE81c345c9'
    prescriber_role_contract = '0x10dDB2eFEEE77f540573Fbc1958fE2f1f8A21f79'

    patient_personal_address = '0x53D20cBCFD24aA63448232F330307cF1d65797a3'
    patient_role_contract = '0xa0DA27D9985939EC4906ae7939df4370040594F8'

    # Add the prescriber as permissioned for the patient
    patient_contract = w3.eth.contract(address=patient_role_contract, abi=_PATIENT_ABI)
    tx_hash = patient_contract.functions.addPermission(
        prescriber_role_contract
    ).transact({'from': w3.eth.accounts[2]})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)

    # Check if permissioned (block 5)
    # tx_hash = patient_contract.functions.permissioned(
    #     prescriber_role_contract
    # ).transact({'from': w3.eth.accounts[2]})
    # tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    # print(tx_receipt)

    # Create a new prescription using the prescriber (that transfers to the patient)
    prescriber_contract = w3.eth.contract(address=prescriber_role_contract, abi=_PRESCRIBER_ABI)
    tx_hash = prescriber_contract.functions.createPrescription(
        patient_role_contract,
        ndc,
        quantity,
        refills
    ).transact({'from': w3.eth.accounts[1]})
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt)


test_new_prescription()
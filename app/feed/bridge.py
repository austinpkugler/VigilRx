import json
import os
from eth_utils.conversions import to_bytes

from web3 import Web3


w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
w3.eth.default_account = w3.eth.accounts[0]

with open(os.path.join('..', '..', 'contracts', 'Prescriber.abi'), 'r') as file:
    PRESCRIBER_ABI = json.load(file)
with open(os.path.join('..', '..', 'contracts', 'Prescriber.bin'), 'r') as file:
    PRESCRIBER_BIN = file.read()

with open(os.path.join('..', '..', 'contracts', 'Prescription.abi'), 'r') as file:
    PRESCRIPTION_ABI = json.load(file)
with open(os.path.join('..', '..', 'contracts', 'Prescription.bin'), 'r') as file:
    PRESCRIPTION_BIN = file.read()


def create_prescriber(prescriber: dict) -> str:
    Contract = w3.eth.contract(abi=PRESCRIBER_ABI, bytecode=PRESCRIBER_BIN)
    tx_hash = Contract.constructor(prescriber['address'], int(prescriber['npi'])).transact()
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    deployed_contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=PRESCRIBER_ABI)
    return deployed_contract.address


def create_prescription(prescriber_contract: str, prescription: dict) -> str:
    # Create new contract object
    deployed_contract = w3.eth.contract(address=prescriber_contract, abi=PRESCRIBER_ABI)

    # Execute new prescription call
    tx_hash = deployed_contract.functions.newPrescription(
        prescription['patient'],
        int(prescription['ndc']),
        int(prescription['quantity']),
        int(prescription['refills'])
    ).call()

    return deployed_contract.address


def get_prescriptions():
    return [
        {
            'name': 'Aspirin',
            'ndc': '89342875',
            'prescriber': '0x89205A3A3b2A69De6Dbf7f01ED13B2108B2c43e7',
            'date': 'June 18, 2021'
        },
        {
            'name': 'Hydrocodone',
            'ndc': '532634634453',
            'prescriber': '0x89205A3A3b2A69De6Dbf7f01ED13B2108B2c43e7',
            'date': 'June 12, 2021'
        },
        {
            'name': 'Fentanyl',
            'ndc': '3253434553',
            'prescriber': '0x89205A3A3b2A69De6Dbf7f01ED13B2108B2c43e7',
            'date': 'November 18, 2020'
        }
    ]


def test():
    prescriber = {
        'address': '0x2ceD722F43588cb6F54C1EF600e014aA3a7dF26d',
        'npi': '1204'
    }
    prescriber_contract = create_prescriber(prescriber)
    # print(f'Deployed new prescriber at {prescriber_contract}')

    prescription = {
        'patient': '0xea21DF16985b026369f5B70Ba37fe983FDa61384',
        'ndc': '214',
        'quantity': '2234',
        'refills': '11',
    }
    prescription_contract = create_prescription(prescriber_contract, prescription)
    print(f'Deployed new prescription at {prescription_contract}')


if __name__ == '__main__':
    test()

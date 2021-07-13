from VigilRx.experiments.compiled import REGISTRAR_ABI
import json
import os

from web3 import Web3

import errors
import compiled
from compiled import w3


class Registrar:

    def __init__(self):
        self.personal_address = w3.eth.accounts[0]

        generic_registrar = w3.eth.contract(abi=compiled.REGISTRAR_ABI, bytecode=compiled.REGISTRAR_BIN)
        tx_hash = generic_registrar.constructor().transact({'from': self.personal_address})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        self.contract_address = tx_receipt.contractAddress
        self.contract = w3.eth.contract(address=self.contract_address, abi=compiled.REGISTRAR_ABI)

    def new_patient(self, patient_personal_address):
        tx_hash = self.contract.functions.createPatient(patient_personal_address).transact({'from': self.personal_address})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        patient_contract_address = str(self.contract.events.NewAddress().processReceipt(tx_receipt)[0]['args']['contractAddress'])
        return patient_contract_address

    def new_prescriber(self, prescriber_personal_address):
        tx_hash = self.contract.functions.createPrescriber(prescriber_personal_address).transact({'from': self.personal_address})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        prescriber_contract_address = str(self.contract.events.NewAddress().processReceipt(tx_receipt)[0]['args']['contractAddress'])
        return prescriber_contract_address

    def new_pharmacy(self, pharmacy_personal_address):
        tx_hash = self.contract.functions.createPharmacy(pharmacy_personal_address).transact({'from': self.personal_address})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        pharmacy_contract_address = str(self.contract.events.NewAddress().processReceipt(tx_receipt)[0]['args']['contractAddress'])
        return pharmacy_contract_address

import json
import os

from web3 import Web3

import errors
import compiled
from compiled import w3
from registrar import Registrar


registrar = Registrar()


class Patient():

    def __init__(self, personal_address):
        self.personal_address = personal_address
        self.contract_address = registrar.new_patient(self.personal_address)
        self.contract = w3.eth.contract(address=self.contract_address, abi=compiled.PATIENT_ABI)
        self.gas_used = 0

    def add_permissioned(self, prescriber):
        tx_hash = self.contract.functions.addPermissionedPrescriber(prescriber.contract_address).transact({'from': self.personal_address})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        self.gas_used += tx_receipt.gasUsed


    def remove_permissioned_prescriber(self, prescriber):
        tx_hash = self.contract.functions.removePermissionedPrescriber(prescriber.contract_address).transact({'from': self.personal_address})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        self.gas_used += tx_receipt.gasUsed

    def __repr__(self):
        return f'Patient(personal_address={self.personal_address}, contract_address={self.contract_address})'


class Prescriber():

    def __init__(self, personal_address, npi):
        self.personal_address = personal_address
        self.npi = npi
        self.contract_address = registrar.new_prescriber(self.personal_address, self.npi)
        self.contract = w3.eth.contract(address=self.contract_address, abi=compiled.PRESCRIBER_ABI)
        self.gas_used = 0

    def __repr__(self):
        return f'Prescriber(personal_address={self.personal_address}, contract_address={self.contract_address})'

    def new_prescription(self, patient, ndc, quantity, refills):
        tx_hash = self.contract.functions.createPrescription(patient.contract_address, ndc, quantity, refills).transact({'from': self.personal_address})
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        self.gas_used += tx_receipt.gasUsed


class Pharmacy():

    def __init__(self, personal_address, npi):
        self.personal_address = personal_address
        self.npi = npi
        self.contract_address = registrar.new_pharmacy(self.personal_address, self.npi)
        self.contract = w3.eth.contract(address=self.contract_address, abi=compiled.PHARMACY_ABI)
        self.gas_used = 0

    def __repr__(self):
        return f'Pharmacy(personal_address={self.personal_address}, contract_address={self.contract_address})'

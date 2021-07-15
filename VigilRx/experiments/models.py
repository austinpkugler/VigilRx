import json
import os

from web3 import Web3

import errors
import compiled
from compiled import w3
from registrar import Registrar


registrar = Registrar()


class Prescription():

    def __init__(self, contract_address, patient, ndc, quantity, refills):
        self.contract_address = contract_address
        self.patient = patient
        self.ndc = ndc
        self.quantity = quantity
        self.refills = refills

    def __repr__(self):
        return f'Prescription(patient={self.patient}, ndc={self.ndc}, quantity={self.quantity}, refills={self.refills})'


class Role():

    def __init__(self, personal_address):
        self.personal_address = personal_address
        self._from = {'from': self.personal_address}


class Provider(Role):

    def __init__(self, npi, **kwargs):
        super().__init__(**kwargs)
        self.npi = npi
        self.contract_address = None
        self.contract = None
        self._from = {'from': self.personal_address}

    def get_patients(self):
        patient_list = self.contract.functions.getPatientList().call()
        return patient_list

    def get_prescriptions(self):
        prescriptions = []
        for i in self.get_patients():
            prescriptions += self.contract.functions.getPrescriptionList(i).call()

        return prescriptions


class Patient(Role):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.contract_address = registrar.new_patient(self.personal_address)
        self.contract = w3.eth.contract(address=self.contract_address, abi=compiled.PATIENT_ABI)
        self.gas_used = 0

    def __repr__(self):
        return f'Patient(personal_address={self.personal_address}, contract_address={self.contract_address}, gas_used={self.gas_used})'

    def add_permissioned(self, prescriber):
        tx_hash = self.contract.functions.addPermissionedPrescriber(prescriber.contract_address).transact(self._from)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        self.gas_used += tx_receipt.gasUsed

    def remove_permissioned(self, prescriber):
        tx_hash = self.contract.functions.removePermissionedPrescriber(prescriber.contract_address).transact(self._from)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        self.gas_used += tx_receipt.gasUsed

    def add_prescription_permissions(self, prescription, pharmacy):
        tx_hash = self.contract.functions.addPrescriptionPermissions(prescription.contract_address, pharmacy.contract_address).transact(self._from)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        self.gas_used += tx_receipt.gasUsed

    def remove_prescription_permissions(self, prescription, pharmacy):
        tx_hash = self.contract.functions.removePrescriptionPermissions(prescription.contract_address, pharmacy.contract_address).transact(self._from)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        self.gas_used += tx_receipt.gasUsed

    def request_fill(self, prescription):
        tx_hash = self.contract.functions.requestFill(prescription.patient.contract_address).transact(self._from)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        self.gas_used += tx_receipt.gasUsed

    def get_prescriptions(self):
        return self.contract.functions.getPrescriptionList().call()


class Prescriber(Provider):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.contract_address = registrar.new_prescriber(self.personal_address, self.npi)
        self.contract = w3.eth.contract(address=self.contract_address, abi=compiled.PRESCRIBER_ABI)
        self.gas_used = 0

    def __repr__(self):
        return f'Prescriber(personal_address={self.personal_address}, contract_address={self.contract_address}, gas_used={self.gas_used})'

    def new_prescription(self, patient, ndc, quantity, refills):
        tx_hash = self.contract.functions.createPrescription(patient.contract_address, ndc, quantity, refills).transact(self._from)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        prescription_contract_address = str(self.contract.events.NewAddress().processReceipt(tx_receipt)[0]['args']['contractAddress'])
        self.gas_used += tx_receipt.gasUsed
        return Prescription(prescription_contract_address, patient, ndc, quantity, refills)

    def refill_prescription(self, prescription, refill_count):
        tx_hash = self.contract.functions.refillPrescription(prescription.contract_address, refill_count).transact(self._from)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        prescription.refills = refill_count
        self.gas_used += tx_receipt.gasUsed

    def cancel_prescription(self, prescription):
        self.refill_prescription(prescription, 0)
        prescription.refills = 0


class Pharmacy(Provider):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.contract_address = registrar.new_pharmacy(self.personal_address, self.npi)
        self.contract = w3.eth.contract(address=self.contract_address, abi=compiled.PHARMACY_ABI)
        self.gas_used = 0

    def __repr__(self):
        return f'Pharmacy(personal_address={self.personal_address}, contract_address={self.contract_address}, gas_used={self.gas_used})'

    def add_prescription(self, prescription):
        tx_hash = self.contract.functions.addPrescription(prescription.contract_address).transact(self._from)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        self.gas_used += tx_receipt.gasUsed

    def fill(self, prescription, fill_count):
        tx_hash = self.contract.functions.fillPrescription(prescription.contract_address, fill_count).transact(self._from)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        self.gas_used += tx_receipt.gasUsed

    def request_refill(self, prescription):
        tx_hash = self.contract.functions.requestRefill(prescription.contract_address).transact(self._from)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        self.gas_used += tx_receipt.gasUsed

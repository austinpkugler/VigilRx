import json
import os

from web3 import Web3

import errors
import compiled
from compiled import w3
from registrar import Registrar


registrar = Registrar()


class Role:

    def __init__(self, personal_address):
        self.personal_address = personal_address


class Patient(Role):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.contract_address = registrar.new_patient(self.personal_address)
        self.contract = w3.eth.contract(address=self.contract_address, abi=compiled.PATIENT_ABI)

    def add_permissioned(self, prescriber):
        tx_hash = self.contract.functions.addPermissionedPrescriber(prescriber.contract).transact({'from': self.personal_address})
        w3.eth.wait_for_transaction_receipt(tx_hash)

    def remove_permissioned_prescriber(self, prescriber):
        tx_hash = self.contract.functions.removePermissionedPrescriber(prescriber.contract).transact({'from': self.personal_address})
        w3.eth.wait_for_transaction_receipt(tx_hash)


class Prescriber(Role):

    def __init__(self, npi, **kwargs):
        super().__init__(**kwargs)
        self.npi = npi
        self.contract_address = registrar.new_patient(self.personal_address, self.npi)
        self.contract = w3.eth.contract(address=self.contract_address, abi=compiled.PRESCRIBER_ABI)

    def new_prescription(self, patient_contract_address, ndc, quantity, refills):
        tx_hash = self.contract.functions.createPrescription(patient_contract_address, ndc, quantity, refills).transact({'from': self.personal_address})
        w3.eth.wait_for_transaction_receipt(tx_hash)


class Pharmacy(Role):

    def __init__(self, npi, **kwargs):
        super().__init__(**kwargs)
        self.npi = npi
        self.contract_address = registrar.new_patient(self.personal_address, self.npi)
        self.contract = w3.eth.contract(address=self.contract_address, abi=compiled.PHARMACY_ABI)


'''
*****Deployment Pseudocode*****

Deploy(patientCount = int, prescriberCount = int, pharmacyCount = int)
	grc = Registrar()
	patientList []
	prescriberList []
	pharmacyList []

	for(int i = 0; i < patientCount; i++) {
		temp = Patient()
        temp.personalAddress = x;
		temp.contractAddress = Registrar().createPatient(personalAddress);
        temp.contract = PATIENT_ABI;

        patientList.push(temp);
	}

    for(int i = 0; i < prescriberCount; i++) {
		temp = Prescriber()
        temp.npi = rand(9999999999);
        temp.personalAddress = x;
		temp.contractAddress = Registrar().createPrescriber(personalAddress, npi);
        temp.contract = PRESCRIBER_ABI;

        prescriberList.push(temp);
	}

    for(int i = 0; i < pharmacyCount; i++) {
		temp = Pharmacy()
        temp.npi = rand(9999999999);
        temp.personalAddress = x;
		temp.contractAddress = Registrar().createPharmacy(personalAddress, npi);
        temp.contract = PHARMACY_ABI;

        pharmacyList.push(temp);
	}
'''


# from web3 import Web3


# w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
# address = w3.geth.personal.new_account('plswork')

# for i, account in enumerate(w3.eth.accounts):
#     balance = w3.eth.get_balance(account)
#     print(f'{i}\t{account}\t{balance}')

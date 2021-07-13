import json
import os

from web3 import Web3

import errors


try:
    with open(os.path.join('build', 'Registrar.abi'), 'r') as file:
        REGISTRAR_ABI = json.load(file)
    with open(os.path.join('build', 'Registrar.bin'), 'r') as file:
        REGISTRAR_BIN = file.read()
    with open(os.path.join('build', 'Patient.abi'), 'r') as file:
        PATIENT_ABI = json.load(file)
    with open(os.path.join('build', 'Prescriber.abi'), 'r') as file:
        PRESCRIBER_ABI = json.load(file)
    with open(os.path.join('build', 'Pharmacy.abi'), 'r') as file:
        PHARMACY_ABI = json.load(file)
except Exception as e:
    raise errors.NotCompiledException()

w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))

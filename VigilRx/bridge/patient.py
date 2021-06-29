import json
import os

from web3 import Web3

from VigilRx.bridge.errors import NotCompiledException


try:
    with open(os.path.join('..', 'build', 'Patient.abi'), 'r') as file:
        PATIENT_ABI = json.load(file)
    with open(os.path.join('..', 'build', 'Patient.bin'), 'r') as file:
        PATIENT_BIN = file.read()
except Exception as e:
    raise NotCompiledException()


def new_patient():
    pass


def view_history():
    pass


def add_permissioned():
    pass


def remove_permissioned():
    pass

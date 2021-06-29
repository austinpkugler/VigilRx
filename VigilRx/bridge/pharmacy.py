import json
import os

from web3 import Web3

from VigilRx.bridge.errors import NotCompiledException


try:
    with open(os.path.join('..', 'build', 'Pharmacy.abi'), 'r') as file:
        PHARMACY_ABI = json.load(file)
    with open(os.path.join('..', 'build', 'Pharmacy.bin'), 'r') as file:
        PHARMACY_BIN = file.read()
except Exception as e:
    raise NotCompiledException()


def new_pharmacy():
    pass

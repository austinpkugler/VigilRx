import json
import os

from web3 import Web3

import errors


try:
    with open(os.path.join('build', 'Prescriber.abi'), 'r') as file:
        _PRESCRIBER_ABI = json.load(file)
    with open(os.path.join('build', 'Prescriber.bin'), 'r') as file:
        _PRESCRIBER_BIN = file.read()
except Exception as e:
    raise errors.NotCompiledException()


def new_prescription():
    pass


def refill_prescription():
    pass

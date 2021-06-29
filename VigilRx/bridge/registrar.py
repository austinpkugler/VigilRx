import json
import os

from web3 import Web3

from VigilRx.bridge.errors import NotCompiledException


try:
    with open(os.path.join('build', 'Registrar.abi'), 'r') as file:
        _REGISTRAR_ABI = json.load(file)
    with open(os.path.join('build', 'Registrar.bin'), 'r') as file:
        _REGISTRAR_BIN = file.read()
except Exception as e:
    raise NotCompiledException()


def new_registrar():
    pass

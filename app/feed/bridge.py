import json
import os

from web3 import Web3

# Deploy Prescriber contract
# Create Prescription   (deploy a Prescription Contract)
# View Prescription      (accessed the info in the Prescription Contract from the front end)

w3 = Web3(Web3.HTTPProvider('http://localhost:7545'))
w3.eth.default_account = w3.eth.accounts[0]

with open(os.path.join('..', '..', 'bin', 'contracts', 'Prescription.abi'), 'r') as file:
    rx_abi = json.load(file)
    print(rx_abi)

with open(os.path.join('..', '..', 'bin', 'contracts', 'Prescriber.abi'), 'r') as file:
    prescriber_abi = json.load(file)
    print(prescriber_abi)

def new_prescription(prescription):
    # prescription = {'patient': '0x2355234', 'ndc': '324', 'quantity': '2', 'refills': '5'}
    # ABI and address used to create contract https://web3py.readthedocs.io/en/stable/web3.eth.html#web3.eth.Eth.contract
    # Contract Constructor Call:
    #       function newPrescription(address _patientAddress, uint32 _ndc, uint _quantity, uint _refills) external onlyOwner returns(address)
    pass


def new_prescriber():
    pass


def new_patient():
    pass


def view_prescription():
    # Contract Method Call:
    #       function viewRx(address rxAddress) external onlyOwner returns(PrescriptionInfo memory){
    pass

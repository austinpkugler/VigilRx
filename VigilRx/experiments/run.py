from random import randint, seed
import time

from web3 import Web3

from compiled import w3
from models import Patient, Prescriber, Pharmacy


seed(int(time.time()))


def deploy(num_patients=0, num_prescribers=0, num_pharmacies=0):
    start = time.time()

    role_pool = {'patients': [], 'prescribers': [], 'pharmacies': []}
    current_account = 1

    for i in range(num_patients):
        patient = Patient(w3.eth.accounts[current_account])
        role_pool['patients'].append(patient)
        current_account += 1

    for i in range(num_prescribers):
        npi = randint(1000000000, 9999999999)
        prescriber = Prescriber(w3.eth.accounts[current_account], npi)
        role_pool['prescribers'].append(prescriber)
        current_account += 1

    for i in range(num_pharmacies):
        npi = randint(1000000000, 9999999999)
        pharmacy = Pharmacy(w3.eth.accounts[current_account], npi)
        role_pool['pharmacies'].append(pharmacy)
        current_account += 1

    return role_pool, time.time() - start


def simulate_prescribing(role_pool):
    start = time.time()
    for i, patient in enumerate(role_pool['patients']):
        patient.add_permissioned(role_pool['prescribers'][i])
        ndc = 1103716366 #randint(1000000000, 9999999999)
        quantity = 3 #randint(1, 250)
        refills = 14 #randint(1, 250)
        role_pool['prescribers'][i].new_prescription(patient, ndc, quantity, refills)
    return time.time() - start


if __name__ == '__main__':
    role_pool, runtime = deploy(, )
    print(f'\n\nDeployed role contracts in {runtime}s\n')

    runtime = simulate_prescribing(role_pool)
    print(f'\n\nSimulated prescribing in {runtime}s\n')

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

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
    print(f'Deploying role contracts')
    role_pool, runtime = deploy(3, 3)
    print(f'Deployed role contracts in {runtime}s\n')

    runtime = simulate_prescribing(role_pool)
    print(f'Simulated prescribing in {runtime}s\n')

    print('---- Prescribers ----')
    for i, prescriber in enumerate(role_pool['prescribers']):
        if i > 10:
            print('...')
            break
        print(f'{i}\t{prescriber}')

    print('\n\n---- Patients ----')
    for i, patient in enumerate(role_pool['patients']):
        if i > 10:
            print('...')
            break
        print(f'{i}\t{patient}')

import random
import time

from bridge import w3, PATIENT_ABI, PRESCRIBER_ABI, PRESCRIPTION_ABI, PHARMACY_ABI
from models import Patient, Prescriber, Pharmacy


def deploy_role_pool(pool_size):
    random.seed(int(time.time()))

    role_pool = {'patients': [], 'prescribers': [], 'pharmacies': []}
    current_account = 1

    for i in range(pool_size // 3):
        patient = Patient(w3.eth.accounts[current_account])
        role_pool['patients'].append(patient)
        current_account += 1

        npi = random.randint(1000000000, 9999999999)
        prescriber = Prescriber(w3.eth.accounts[current_account], npi)
        role_pool['prescribers'].append(prescriber)
        current_account += 1

        npi = random.randint(1000000000, 9999999999)
        pharmacy = Pharmacy(w3.eth.accounts[current_account], npi)
        role_pool['pharmacies'].append(pharmacy)
        current_account += 1

    return role_pool


def simulate_patient(role_pool, patient):
    # Phase 1 - Has Prescriber?
    if not patient.get_prescriptions():
        # Patient selects a new doctor and permissions them
        rand_prescriber = random.choice(role_pool['prescribers'])
        patient.add_permissioned(rand_prescriber)

        # New doctor issues the patient a new prescription
        ndc = random.randint(1000000000, 9999999999)
        quantity = random.randint(1, 9)
        refills = random.randint(10, 99)
        prescription_address = rand_prescriber.new_prescription(patient, ndc, quantity, refills)

        # Patient selects a new pharmacy to have it filled and permissions them
        rand_pharmacy = random.choice(role_pool['pharmacies'])
        patient.add_prescription_permissions(prescription_address, rand_pharmacy)

        # Pharmacy adds the prescription to their records
        rand_pharmacy.add_prescription(prescription_address)

        # Triad is now complete and can be cycled

    # Phase 2 - Request Prescriptions Fills
    for prescription_address in patient.get_prescriptions():
        temp_contract = w3.eth.contract(address=prescription_address, abi=PRESCRIPTION_ABI)

        fillSignature = temp_contract.functions.fillSigRequired().call()
        refillSignature = temp_contract.functions.refillSigRequired().call()

        if not fillSignature and not refillSignature:
            patient.request_fill(prescription_address)


def simulate_prescriber(prescriber):
    # Phase 1 - Check for refill flags on all prescriptions
    for prescription_address in prescriber.get_prescriptions():
        temp_contract = w3.eth.contract(address=prescription_address, abi=PRESCRIPTION_ABI)

        if temp_contract.functions.refillSigRequired().call():
            prescriber.refill_prescription(prescription_address, random.randint(1, 255))


def simulate_pharmacy(pharmacy):
    # Phase 1 - Check for fill flags on all prescriptions
    for prescription_address in pharmacy.get_prescriptions():
        temp_contract = w3.eth.contract(address=prescription_address, abi=PRESCRIPTION_ABI)

        fillSignature = temp_contract.functions.fillSigRequired().call()
        fillCount = temp_contract.functions.p().call()[2]

        if fillSignature and fillCount:
            pharmacy.fill_prescription(prescription_address, 1)
        elif fillSignature and not fillCount:
            pharmacy.request_refill(prescription_address)


def calculate_gas_used(role_pool):
    patient_gas_used = sum(p.gas_used for p in role_pool['patients'])
    prescriber_gas_used = sum(p.gas_used for p in role_pool['prescribers'])
    pharmacy_gas_used = sum(p.gas_used for p in role_pool['pharmacies'])
    return patient_gas_used + prescriber_gas_used + pharmacy_gas_used


def cycle(pool_size, num_cycles=1):
    runtime = []
    gas_used = []
    role_pool = deploy_role_pool(pool_size)

    print ("Deployment phase complete.")

    for i in range(num_cycles):
        start = time.time()
        for patient in role_pool['patients']:
            simulate_patient(role_pool, patient)
        for pharmacy in role_pool['pharmacies']:
            simulate_pharmacy(pharmacy)
        for prescriber in role_pool['prescribers']:
            simulate_prescriber(prescriber)

        runtime.append(time.time() - start)
        gas_used.append(calculate_gas_used(role_pool))

    return runtime, gas_used



if __name__ == '__main__':
    CYCLES = 5
    runtime, gas_used = cycle(99, CYCLES)

    print(f'cycle\truntime\tgas used')
    for i in range(CYCLES):
        print(f'{i + 1}\t{runtime[i]}\t{gas_used[i]}')

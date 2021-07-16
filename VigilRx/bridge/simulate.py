import random
import time

from bridge import w3, PRESCRIPTION_ABI
from models import Patient, Prescriber, Pharmacy


random.seed(int(time.time()))


def deploy_role_pool(pool_size):
    """Deploys a pool of patient, prescriber, and pharmacy role
    contracts to Ganache.

    :param pool_size: Number of role contracts to deploy.
    :type pool_size: int
    :return: Dictionary with roles as keys as lists of role contracts as
        values.
    :rtype: dict
    """
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
    """Simulates the actions of a patient, like adding permissions and
    participating in multisig prescription fills and refills.

    :param role_pool: Pool of patient, prescriber, and pharmacy role
        contracts deployed to Ganache.
    :type rool_pool: dict
    :param patient: Patient object to simulate actions for.
    :type patient: :class:`Patient`
    """
    # If the patient does not have a prescriber
    if not patient.get_prescriptions():
        # Patient selects and permissions a random prescriber
        prescriber = random.choice(role_pool['prescribers'])
        patient.add_permissioned(prescriber)

        # Prescriber issues patient a new prescription
        ndc = random.randint(1000000000, 9999999999)
        quantity = random.randint(1, 9)
        refills = random.randint(10, 99)
        prescription_address = prescriber.new_prescription(
            patient,
            ndc,
            quantity,
            refills
        )

        # Patient selects and permissions a random pharmacy
        pharmacy = random.choice(role_pool['pharmacies'])
        patient.add_prescription_permissions(prescription_address, pharmacy)

        # Pharmacy adds the prescription to their records
        pharmacy.add_prescription(prescription_address)

    # Patient requests prescriptions fills for each prescription
    for prescription_address in patient.get_prescriptions():
        prescription_contract = w3.eth.contract(
            address=prescription_address,
            abi=PRESCRIPTION_ABI
        )

        fill_sig = prescription_contract.functions.fillSigRequired().call()
        refill_sig = prescription_contract.functions.refillSigRequired().call()

        if not fill_sig and not refill_sig:
            patient.request_fill(prescription_address)


def simulate_prescriber(prescriber):
    """Simulates the actions of a prescriber, like performing multisig
    prescription refills.

    :param prescriber: Prescriber object to simulate actions for.
    :type prescriber: :class:`Prescriber`
    """
    # Prescriber checks for refill flags and completes multisig refills.
    for prescription_address in prescriber.get_prescriptions():
        prescription_contract = w3.eth.contract(
            address=prescription_address,
            abi=PRESCRIPTION_ABI
        )

        if prescription_contract.functions.refillSigRequired().call():
            prescriber.refill_prescription(
                prescription_address,
                random.randint(10, 99)
            )


def simulate_pharmacy(pharmacy):
    """Simulates the actions of a pharmacy, like performing multisig
    prescription fills.

    :param pharmacy: Pharmacy object to simulate actions for.
    :type pharmacy: :class:`Pharmacy`
    """
    # Pharmacy checks for fill flags and completes multisig fills.
    for prescription_address in pharmacy.get_prescriptions():
        prescription_contract = w3.eth.contract(
            address=prescription_address,
            abi=PRESCRIPTION_ABI
        )

        fill_sig = prescription_contract.functions.fillSigRequired().call()
        fillCount = prescription_contract.functions.p().call()[2]

        if fill_sig and fillCount:
            pharmacy.fill_prescription(prescription_address, 1)
        elif fill_sig and not fillCount:
            pharmacy.request_refill(prescription_address)


def calculate_gas_used(role_pool):
    """Calculates the total gas used by the patient, prescriber, and
    pharmacy role contracts, as measured by Ganache.

    :param role_pool: Pool of patient, prescriber, and pharmacy role
        contracts deployed to Ganache.
    :type rool_pool: dict
    :return: Total count of gas used in wei.
    :rtype: float
    """
    patient_gas_used = sum(p.gas_used for p in role_pool['patients'])
    prescriber_gas_used = sum(p.gas_used for p in role_pool['prescribers'])
    pharmacy_gas_used = sum(p.gas_used for p in role_pool['pharmacies'])
    return patient_gas_used + prescriber_gas_used + pharmacy_gas_used


def cycle(pool_size, num_cycles=1):
    """Simulates the actions of patient, prescriber, and pharmacy role
    contracts using Ganache. Simulation is performed for a passed number
    of cycles, where every role contract performs their relevant actions
    once per cycle.

    :param pool_size: Number of role contracts to simulate.
    :type pool_size: int
    :param num_cycles: Number of cycles to simulate.
    :type num_cycles: int
    """
    runtime = []
    gas_used = []
    role_pool = deploy_role_pool(pool_size)

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
    num_cycles = 5
    runtime, gas_used = cycle(99, num_cycles)

    print(f'cycle\ttotal runtime (s)\tgas used (wei)')
    for i in range(num_cycles):
        print(f'{i + 1}\t{runtime[i]}\t{gas_used[i]}')

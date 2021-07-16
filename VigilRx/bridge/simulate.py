import json
import os
import random
import time

import pandas as pd

from bridge import w3, PRESCRIPTION_ABI
from models import Patient, Prescriber, Pharmacy


random.seed(int(time.time()))


class Simulator():

    def __init__(self, pool_size, num_cycles, patient_ratio, prescriber_ratio,
                 pharmacy_ratio):
        self.pool_size = pool_size
        self.num_cycles = num_cycles
        self.patient_ratio = patient_ratio
        self.prescriber_ratio = prescriber_ratio
        self.pharmacy_ratio = pharmacy_ratio
        self.role_pool = {'patients': [], 'prescribers': [], 'pharmacies': []}
        self.deploy_role_pool()

    def deploy_role_pool(self):
        """Deploys a pool of patient, prescriber, and pharmacy role
        contracts to Ganache.

        :param pool_size: Number of role contracts to deploy.
        :type pool_size: int
        """
        current_account = 1

        for i in range(int(self.pool_size * self.patient_ratio)):
            patient = Patient(w3.eth.accounts[current_account])
            self.role_pool['patients'].append(patient)
            current_account += 1

        for i in range(int(self.pool_size * self.prescriber_ratio)):
            npi = 5555555555
            prescriber = Prescriber(w3.eth.accounts[current_account], npi)
            self.role_pool['prescribers'].append(prescriber)
            current_account += 1

        for i in range(int(self.pool_size * self.pharmacy_ratio)):
            npi = 5555555555
            pharmacy = Pharmacy(w3.eth.accounts[current_account], npi)
            self.role_pool['pharmacies'].append(pharmacy)
            current_account += 1
        
        print("===== Role pool deployment complete =====")

    def simulate_patient(self, patient):
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
            prescriber = random.choice(self.role_pool['prescribers'])

            patient.add_permissioned(prescriber)

            # Prescriber issues patient a new prescription
            ndc = 5555555555
            quantity = random.randint(1, 9)
            refills = random.randint(1, 9)
            prescription_address = prescriber.new_prescription(
                patient,
                ndc,
                quantity,
                refills
            )

            # Patient selects and permissions a random pharmacy
            pharmacy = random.choice(self.role_pool['pharmacies'])
            patient.add_prescription_permissions(
                prescription_address,
                pharmacy
            )

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

    def simulate_prescriber(self, prescriber):
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
                    random.randint(1, 9)
                )

    def simulate_pharmacy(self, pharmacy):
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
            fill_count = prescription_contract.functions.p().call()[3]
            if fill_sig and fill_count:
                pharmacy.fill_prescription(prescription_address, 1)
            elif fill_sig and not fill_count:
                pharmacy.request_refill(prescription_address)

    def cycle(self):
        """Simulates the actions of patient, prescriber, and pharmacy role
        contracts using Ganache. Simulation is performed for a passed number
        of cycles, where every role contract performs their relevant actions
        once per cycle.
        """
        for i in range(self.num_cycles):
            for patient in self.role_pool['patients']:
                self.simulate_patient(patient)

            for prescriber in self.role_pool['prescribers']:
                self.simulate_prescriber(prescriber)

            for pharmacy in self.role_pool['pharmacies']:
                self.simulate_pharmacy(pharmacy)

            print("===== Cycle ", i + 1, "/", self.num_cycles, " Complete =====")

        print("✧･ﾟ: *✧･ﾟ:* Simulation Complete *:･ﾟ✧*:･ﾟ✧")

    def save_role_pool(self):
        role_dicts = []
        for role, role_objects in self.role_pool.items():
            for role_object in role_objects:
                role_dict = role_object.to_dict()
                for function, value in role_dict['runtime'].items():
                    role_dict[function + '_runtime'] = value
                for function, value in role_dict['gas_used'].items():
                    role_dict[function + '_gas_used'] = value
                for function, value in role_dict['transactions'].items():
                    role_dict[function + '_transactions'] = value

                role_dict.pop('runtime')
                role_dict.pop('gas_used')
                role_dict.pop('transactions')

                role_dicts.append(role_dict)

        if not os.path.exists('experiments'):
            os.mkdir(os.path.join('experiments'))

        save_time = int(time.time())

        df = pd.DataFrame(role_dicts)
        df.to_csv(os.path.join('experiments', f'role_pool_{save_time}.csv'))


if __name__ == '__main__':
    simulator = Simulator(50, 10, 0.8, 0.16, 0.04)
    simulator.cycle()
    simulator.save_role_pool()

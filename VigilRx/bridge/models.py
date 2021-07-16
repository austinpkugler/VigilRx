import json
import os

from web3 import Web3

import bridge
from bridge import w3


class Registrar():
    """Represents Solidity registrar contract and allows role contract
    deployment to Ganache via Web3.
    """

    def __init__(self):
        self.personal_address = w3.eth.accounts[0]
        self.sender = {'from': self.personal_address}

        template = w3.eth.contract(
            abi=bridge.REGISTRAR_ABI,
            bytecode=bridge.REGISTRAR_BIN
        )
        tx_hash = template.constructor().transact(self.sender)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

        self.contract_address = tx_receipt.contractAddress
        self.contract = w3.eth.contract(
            address=self.contract_address,
            abi=bridge.REGISTRAR_ABI
        )

    def new_patient(self, personal_address):
        """Deploys new patient role contract to Ganache.

        :param personal_address: A valid Ganache account address used to
            deploy a new patient role contract.
        :type personal_address: str
        :returns: Patient object representing newly deployed patient
            role contract.
        :rtype: Patient
        """
        tx_hash = self.contract.functions.createPatient(
            personal_address
        ).transact(self.sender)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        tx_event = self.contract.events.NewAddress().processReceipt(tx_receipt)
        return str(tx_event[0]['args']['contractAddress'])

    def new_prescriber(self, personal_address, npi):
        """Deploys new prescriber role contract to Ganache.

        :param personal_address: A valid Ganache account address used to
            deploy a new prescriber role contract.
        :type personal_address: str
        :param npi: National provider identifier of prescriber being
            created.
        :type npi: int
        :returns: Prescriber object representing newly deployed
            prescriber role contract.
        :rtype: Prescriber
        """
        tx_hash = self.contract.functions.createPrescriber(
            personal_address,
            npi
        ).transact(self.sender)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        tx_event = self.contract.events.NewAddress().processReceipt(tx_receipt)
        return str(tx_event[0]['args']['contractAddress'])

    def new_pharmacy(self, personal_address, npi):
        """Deploys new pharmacy role contract to Ganache.

        :param personal_address: A valid Ganache account address used to
            deploy a new pharmacy role contract.
        :type personal_address: str
        :param npi: National provider identifier of pharmacy being
            created.
        :type npi: int
        :returns: Pharmacy object representing newly deployed pharmacy
            role contract.
        :rtype: Pharmacy
        """
        tx_hash = self.contract.functions.createPharmacy(
            personal_address,
            npi
        ).transact(self.sender)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        tx_event = self.contract.events.NewAddress().processReceipt(tx_receipt)
        return str(tx_event[0]['args']['contractAddress'])


class Roles():
    """Base class for all role contracts. A single registrar contract is
    deployed to Ganache to control all role contracts.

    :param personal_address: A valid Ganache account address used to
        deploy a new role contract.
    :type personal_address: str
    """

    _registrar = Registrar()

    def __init__(self, personal_address):
        self.personal_address = personal_address
        self.sender = {'from': self.personal_address}
        self.contract_address = None
        self.contract = None
        self.gas_used = 0


class Provider(Roles):
    """Base class for prescriber and pharmacy role contracts. Inherits
    from :class:`Roles`.

    :param personal_address: A valid Ganache account address used to
        deploy a new role contract.
    :type personal_address: str
    :param npi: National provider identifier of provider.
    :type npi: int
    """

    def __init__(self, personal_address, npi):
        super().__init__(personal_address)
        self.npi = npi

    def get_patients(self):
        """Returns a list of all patient role contract addresses
        associated with the :class:`Provider` instance.

        :returns: List of patient role contract addresses.
        :rtype: list
        """
        return self.contract.functions.getPatientList().call()

    def get_prescriptions(self):
        """Returns a list of all prescription contract addresses
        associated with the :class:`Provider` instance.

        :returns: List of prescription contract addresses.
        :rtype: list
        """
        prescriptions = []
        for i in self.get_patients():
            prescriptions += self.contract.functions.getPrescriptionList(
                i
            ).call()

        return prescriptions


class Patient(Roles):
    """Represents Solidity patient role contract and allows patient
    prescription actions to be performed via Web3. Inherits from
    :class:`Roles`.

    :param personal_address: A valid Ganache account address used to
        deploy a new patient role contract.
    :type personal_address: str
    """

    def __init__(self, personal_address):
        super().__init__(personal_address)
        self.contract_address = Roles._registrar.new_patient(
            self.personal_address
        )
        self.contract = w3.eth.contract(
            address=self.contract_address,
            abi=bridge.PATIENT_ABI
        )

    def __repr__(self):
        return f'Patient(contract_address={self.contract_address})'

    def add_permissioned(self, prescriber):
        """Adds a prescriber as permissioned to prescribe to the
        :class:`Patient` instance.

        :param prescriber: An instance of :class:`Prescriber` to add
            as a permissioned prescriber.
        :type personal_address: :class:`Prescriber`
        """
        tx_hash = self.contract.functions.addPermissionedPrescriber(
            prescriber.contract_address
        ).transact(self.sender)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        self.gas_used += tx_receipt.gasUsed

    def remove_permissioned(self, prescriber):
        """Removes a prescriber as permissioned to prescribe to the
        :class:`Patient` instance.

        :param prescriber: Instance of :class:`Prescriber` to remove
            as a permissioned prescriber.
        :type personal_address: :class:`Prescriber`
        """
        tx_hash = self.contract.functions.removePermissionedPrescriber(
            prescriber.contract_address
        ).transact(self.sender)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        self.gas_used += tx_receipt.gasUsed

    def add_prescription_permissions(self, prescription_address, pharmacy):
        """Adds a pharmacy as permissioned to view and fill the
        prescriptions for the :class:`Patient` instance.

        :param prescription_address: Address of prescription to add
            permissions to.
        :param prescription_address: str
        :param pharmacy: Instance of :class:`Pharmacy` to add as
            permissioned on the prescription.
        :type personal_address: :class:`Pharmacy`
        """
        tx_hash = self.contract.functions.addPrescriptionPermissions(
            prescription_address,
            pharmacy.contract_address
        ).transact(self.sender)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        self.gas_used += tx_receipt.gasUsed

    def remove_prescription_permissions(self, prescription_address, pharmacy):
        """Removes a pharmacy as permissioned to view and fill the
        prescriptions for the :class:`Patient` instance.

        :param prescription_address: Address of prescription to remove
            permissions from.
        :param prescription_address: str
        :param pharmacy: Instance of :class:`Pharmacy` to remove as
            permissioned on the prescription.
        :type personal_address: :class:`Pharmacy`
        """
        tx_hash = self.contract.functions.removePrescriptionPermissions(
            prescription_address,
            pharmacy.contract_address
        ).transact(self.sender)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        self.gas_used += tx_receipt.gasUsed

    def request_fill(self, prescription_address):
        """Sets a request fill flag to true for the specified
        prescription, part of multisig prescription filling.

        :param prescription_address: Address of prescription to request
            a fill for.
        :param prescription_address: str
        """
        tx_hash = self.contract.functions.requestFill(
            prescription_address
        ).transact(self.sender)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        self.gas_used += tx_receipt.gasUsed

    def get_prescriptions(self):
        """Returns a list of all prescription contract addresses
        associated with the :class:`Patient` instance.

        :returns: List of prescription contract addresses.
        :rtype: list
        """
        return self.contract.functions.getPrescriptionList().call()


class Prescriber(Provider):
    """Represents Solidity prescriber role contract and allows prescriber
    prescription actions to be performed via Web3. Inherits from
    :class:`Provider`.

    :param personal_address: A valid Ganache account address used to
        deploy a new prescriber role contract.
    :type personal_address: str
    :param npi: National provider identifier of prescriber.
    :type npi: int
    """

    def __init__(self, personal_address, npi):
        super().__init__(personal_address, npi)
        self.contract_address = Roles._registrar.new_prescriber(
            self.personal_address,
            self.npi
        )
        self.contract = w3.eth.contract(
            address=self.contract_address,
            abi=bridge.PRESCRIBER_ABI
        )

    def __repr__(self):
        return f'Prescriber(contract_address={self.contract_address})'

    def new_prescription(self, patient, ndc, quantity, refills):
        """Deploys new prescription contract to Ganache.

        :param patient: Instance of :class:`Patient` to use as the
            prescription contract owner.
        :type patient: :class:`Patient`
        :param ndc: National drug code of prescription.
        :type ndc: int
        :param quantity: Number of drugs per each prescription fill.
        :type quantity: int
        :param refills: Number of prescription refills.
        :type refills: int
        :returns: Contract address of the newly deployed prescription.
        :rtype: str
        """
        tx_hash = self.contract.functions.createPrescription(
            patient.contract_address,
            ndc,
            quantity,
            refills
        ).transact(self.sender)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        tx_event = self.contract.events.NewAddress().processReceipt(tx_receipt)
        self.gas_used += tx_receipt.gasUsed
        return str(tx_event[0]['args']['contractAddress'])

    def refill_prescription(self, prescription_address, refill_count):
        """Updates the refill number for a specified prescription.

        :param prescription_address: Contract address of a deployed
            prescription.
        :type prescription_address: str
        :param refill_count: Updated number of prescription refills.
        :type refill_count: int
        """
        tx_hash = self.contract.functions.refillPrescription(
            prescription_address,
            refill_count
        ).transact(self.sender)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        prescription_address.refills = refill_count
        self.gas_used += tx_receipt.gasUsed

    def cancel_prescription(self, prescription_address):
        """Updates the refill number to 0 for a specified prescription.

        :param prescription_address: Contract address of a deployed
            prescription.
        :type prescription_address: str
        """
        self.refill_prescription(prescription_address, 0)


class Pharmacy(Provider):
    """Represents Solidity pharmacy role contract and allows pharmacy
    prescription actions to be performed via Web3. Inherits from
    :class:`Provider`.

    :param personal_address: A valid Ganache account address used to
        deploy a new pharmacy role contract.
    :type personal_address: str
    :param npi: National provider identifier of pharmacy.
    :type npi: int
    """

    def __init__(self, personal_address, npi):
        super().__init__(personal_address, npi)
        self.contract_address = Roles._registrar.new_pharmacy(
            self.personal_address,
            self.npi
        )
        self.contract = w3.eth.contract(
            address=self.contract_address,
            abi=bridge.PHARMACY_ABI
        )

    def __repr__(self):
        return f'Pharmacy(contract_address={self.contract_address})'

    def add_prescription(self, prescription_address):
        """Adds the specified prescription to the :class:`Pharmacy`'s
        list of prescriptions.

        :param prescription_address: Contract address of a deployed
            prescription.
        :type prescription_address: str
        """
        tx_hash = self.contract.functions.addPrescription(
            prescription_address
        ).transact(self.sender)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        self.gas_used += tx_receipt.gasUsed

    def fill_prescription(self, prescription_address, fill_count):
        """Fills the specified prescription.

        :param prescription_address: Contract address of a deployed
            prescription.
        :type prescription_address: str
        :param fill_count: Number to decrement from the deployed
            prescription contract's refills.
        :type fill_count: int
        """
        tx_hash = self.contract.functions.fillPrescription(
            prescription_address,
            fill_count
        ).transact(self.sender)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        self.gas_used += tx_receipt.gasUsed

    def request_refill(self, prescription_address):
        """Sets the request refill flag to true for the specified
        prescription.

        :param prescription_address: Contract address of a deployed
            prescription.
        :type prescription_address: str
        """
        tx_hash = self.contract.functions.requestRefill(
            prescription_address
        ).transact(self.sender)
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        self.gas_used += tx_receipt.gasUsed

// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "./Patient.sol";
import "./Prescription.sol";
import "./Registrar.sol";

/// @title Prescriber Role Contract
/// @author Austin Kugler, Alixandra Taylor
/// @notice The contract represents a prescriber in the system, creation new prescription
///         contracts and tracking the ones created
contract Prescriber {
    address owner;
    Registrar public registrarContract;

    uint40 public npi;
    address[] patients;
    mapping(address => address[]) public prescriptions;

    event NewAddress(address indexed contractAddress);

    constructor(address _prescriber, uint40 _npi) {
        owner = _prescriber;
        npi = _npi;
        registrarContract = Registrar(msg.sender);
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Error: Message sender is not owner");
        _;
    }

    function createPrescription(address patientContract, uint40 ndc, uint8 quantity, uint8 refills) external onlyOwner {
        Patient p = Patient(patientContract);
        require(p.isPermissioned(), "Error: Patient has not permissioned you to issue prescriptions for them");

        // If the owner is currently not set as patient, then push them to the enumerated list 
        if (prescriptions[patientContract].length == 0) {
            patients.push(patientContract);
        }

        // Create new prescription and add to mapping
        address newPrescription = address(new Prescription(patientContract, address(registrarContract), ndc, quantity, refills));
        prescriptions[patientContract].push(newPrescription);

        // Add new prescription in the patient's contract as well
        p.addPrescription(newPrescription);

        emit NewAddress(newPrescription);
    }

    function refillPrescription(address prescriptionContract, uint8 refillCount) external onlyOwner {
        Prescription(prescriptionContract).refillPrescription(refillCount);
    }
}

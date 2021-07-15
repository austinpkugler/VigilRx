// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "./Registrar.sol";
import "./Prescription.sol";

/// @title Pharmacy Role Contract
/// @author Austin Kugler, Alixandra Taylor
/// @notice The contract represents a pharmacist in the system, filling prescription
///         and passing along refill requests to a prescriber
contract Pharmacy {
    address owner;
    Registrar public registrar;

    uint40 public npi;

    address[] public patients;
    mapping(address => address[]) public prescriptions;

    constructor(address _pharmacy, uint40 _npi) {
        owner = _pharmacy;
        npi = _npi;
        registrar = Registrar(msg.sender);
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Pharmacy reverted: Requester is not owner");
        _;
    }

    function addPrescription(address prescriptionAddress) external onlyOwner {
        // Retrieve the owner's patient contract address from the prescription contract
        address patientContract = Prescription(prescriptionAddress).owner();

        if (prescriptions[patientContract].length == 0) {
            patients.push(patientContract);
        }

        // Either way, add the new prescription contract to the mapping
        prescriptions[patientContract].push(prescriptionAddress);
    }

    function fillPrescription(address contractAddress, uint8 fillCount) external onlyOwner {
        Prescription(contractAddress).fillPrescription(fillCount);
    }

    function requestRefill(address contractAddress) external onlyOwner {
        Prescription(contractAddress).requestRefill();
    }

    function getPatientList() external view returns(address [] memory) {
        return patients;
    }
    
    function getPrescriptionList(address patientAddress) external view returns(address [] memory) {
        return prescriptions[patientAddress];
    }
}

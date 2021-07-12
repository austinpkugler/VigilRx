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
    uint40 public npi;
    Registrar public registrarContract;

    address[] patients;
    mapping(address => address[]) prescriptions;

    constructor(address _pharmacy, uint40 _npi) {
        owner = _pharmacy;
        npi = _npi;
        registrarContract = Registrar(msg.sender);
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Error: Sender is not owner");
        _;
    }

    function addPrescription(address prescriptionAddress) external onlyOwner {

        // Retrieve the owner's patient contract address from the prescription contract
        address rxOwner = Prescription(prescriptionAddress).owner();

        // If the owner is currently not set as patient, then push them to the enumerated list
        if (prescriptions[rxOwner].length == 0) {
            patients.push(rxOwner);
        }

        // Either way, add the new prescription contract to the mapping
        prescriptions[rxOwner].push(prescriptionAddress);
    }

    function fillPrescription(address contractAddress, uint8 fillCount) external onlyOwner {
        Prescription(contractAddress).fillPrescription(fillCount);
    }

    // function requestRefill(address contractAddress, uint8 refillCount) external onlyOwner {
    //     Prescription(contractAddress).requestRefill(refillCount);
    // }
}

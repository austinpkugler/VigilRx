// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "./Prescription.sol";


contract Prescriber {

    uint40 public npi;
    address owner;
    address[] patients;
    mapping(address => address[]) prescriptions;

    constructor(address _prescriber, uint40 _npi) {
        owner = _prescriber;
        npi = _npi;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function newPrescription(address patientContract, uint40 ndc, uint32 quantity, uint32 refills) external onlyOwner returns(address) {
        address prescription = address(new Prescription(patientContract, ndc, quantity, refills));
        prescriptions[patientContract].push(prescription);
        return prescription;
    }

}

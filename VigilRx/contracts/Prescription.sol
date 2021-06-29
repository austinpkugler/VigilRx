// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;


contract Prescription {

    struct PrescriptionInfo {
        address prescriber;
        uint40 ndc;
        uint32 quantity;
        uint32 refills;
    }

    address owner;
    mapping(address => bool) permissioned;
    PrescriptionInfo public p;

    constructor(address _patientContract, uint40 _ndc, uint32 _quantity, uint32 _refills) {
        owner = _patientContract;
        p.prescriber = msg.sender;
        p.ndc = _ndc;
        p.quantity = _quantity;
        p.refills = _refills;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    modifier onlyPrescriber() {
        require(msg.sender == p.prescriber);
        _;
    }

    modifier onlyPermissioned {
        require(msg.sender == p.prescriber || permissioned[msg.sender] == true);
        _;
    }

    function refillPrescription(uint32 refillCount) external onlyPrescriber {
        p.refills = refillCount;
    }

    // function fillPrescription(uint256 refillCount) external onlyPharmacy {
        
    // }

}

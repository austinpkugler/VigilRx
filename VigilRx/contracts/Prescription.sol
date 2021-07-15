// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "./Registrar.sol";
import "./Patient.sol";

/// @title Prescription
/// @author Austin Kugler, Alixandra Taylor
/// @notice This contract represents a prescription within the system and tracks
///         fill and refill requests
contract Prescription {
    struct PrescriptionInfo {
        address prescriber;
        uint40 ndc;
        uint8 quantity;
        uint8 refills;
    }

    bool public fillSigRequired;
    bool public refillSigRequired;
    
    address public owner;
    Registrar public registrar;
    PrescriptionInfo public p;
    
    mapping(address => bool) permissioned;

    constructor(address _patientContract, address _registrarAddress, uint40 _ndc, uint8 _quantity, uint8 _refills) {
        owner = _patientContract;
        // Set global registry contract
        registrar = Registrar(_registrarAddress);

        p.ndc = _ndc;
        p.quantity = _quantity;
        p.refills = _refills;
        p.prescriber = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Prescription reverted: Requester is not owner");
        _;
    }

    modifier onlyPrescriber() {
        require(msg.sender == p.prescriber, "Prescription reverted: Requester is not prescriber");
        _;
    }

    modifier onlyPermissioned {
        require(permissioned[msg.sender] || msg.sender == p.prescriber , "Prescription reverted: Requester is not permissioned");
        _;
    }

    /// @notice Add a new permissioned party to this prescription (i.e. Pharmacist)
    function addPermissionedPrescriber(address party) external onlyOwner {
        require(permissioned[party] == false, "Prescription reverted: Requester is already permissioned");
        require(registrar.isPharmacy(party), "Prescription reverted: Address is not registered");

        permissioned[party] = true;
    }
    
        /// @notice Remove a permissioned party to this prescription (i.e. Pharmacist)
    function removePermissionedPrescriber(address party) external onlyOwner {
        require(permissioned[party] == true, "Prescription reverted: Requester is not permissioned");

        permissioned[party] = false;
    }

    /// Multi-Sig Phase 1
    function requestFill() external onlyOwner {
        require(!fillSigRequired, "Prescription reverted: Prescription already signed");

        // Set check signature notifier
        fillSigRequired = true;
    }

    /// Multi-Sig Phase 2 + Execution
    function fillPrescription(uint8 fillCount) external onlyPermissioned {
        require(fillCount <= p.refills, "Prescription reverted: Not enough refills");

        p.refills -= fillCount;

        // Reset check signature notifier
        fillSigRequired = false;
    }

    /// @notice Change the number of refills on this prescription
    function refillPrescription(uint8 refillCount) external onlyPrescriber {
        p.refills = refillCount;

        // Reset the flag
        refillSigRequired = false;
    }

    /// @notice Request refill (currently tabbed in)
    function requestRefill() external onlyPermissioned {
        require(!refillSigRequired, "Prescription reverted: Refill already signed");

        refillSigRequired = true;
    }
}

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

    address public owner;
    mapping(address => bool) permissioned;
    Registrar public registrarContract;
    PrescriptionInfo public p;

    bool public fillSigRequired;

    constructor(address _patientContract, address _registrarAddress, uint40 _ndc, uint8 _quantity, uint8 _refills) {
        owner = _patientContract;
        // Set global registry contract
        registrarContract = Registrar(_registrarAddress);

        p.ndc = _ndc;
        p.quantity = _quantity;
        p.refills = _refills;
        p.prescriber = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Requester is not owner.");
        _;
    }

    modifier onlyPrescriber() {
        require(msg.sender == p.prescriber, "Requester is not prescriber.");
        _;
    }

    modifier onlyPermissioned {
        require(msg.sender == p.prescriber || permissioned[msg.sender], "Requester is not permissioned.");
        _;
    }

    /// @notice Add a new permissioned party to this prescription (i.e. Pharmacist)
    function addPermissionedPrescribered(address party) external onlyOwner {
        require(permissioned[party] == false, "Error: Party already permissioned.");
        require(registrarContract.isPharmacy(party) || registrarContract.isPrescriber(party), "Address is not registered");

        permissioned[party] = true;
    }
    
        /// @notice Add a new permissioned part to this prescription (i.e. Pharmacist)
    function removePermissionedPrescribered(address party) external onlyOwner {
        require(permissioned[party] == true, "Error: Party is not permissioned.");

        permissioned[party] = false;
    }

    /// Multi-Sig Phase 1
    function requestFill() external onlyOwner {
        require(!fillSigRequired, "Error: Already signed, awaiting fill");

        // Set check signature notifier
        fillSigRequired = true;
    }

    /// Multi-Sig Phase 2 + Execution
    function fillPrescription(uint8 fillCount) external onlyPermissioned {
        require(registrarContract.isPharmacy(msg.sender), "Error: Only pharmacy may validate fill request");
        require(fillCount <= p.refills, "Error: Not enough refills available");

        p.refills -= fillCount;

        // Reset check signature notifier
        fillSigRequired = false;
    }

    /// @notice Change the number of refills on this prescription
    function refillPrescription(uint8 refillCount) external onlyPrescriber {
        p.refills = refillCount;
    }

    /// @notice Request refill (currently tabbed in)
    // function requestRefill(uint8 refillCount) external view onlyPermissioned {
    //     return;
    // }
}

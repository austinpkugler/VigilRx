// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "./Registrar.sol";
import "./Prescription.sol";

/// @title Patient Role Contract
/// @author Austin Kugler, Alixandra Taylor
/// @notice The contract represents a patient in the system, handling permissioning
///         checks and tracking assigned prescription contracts
contract Patient {
    /// @notice Contract owner and registrar contract addresses
    address owner;
    Registrar public registrar;
    mapping(address => bool) public permissioned; /// @notice Permissioned parties mapping, determines who is allowed certain actions
    address[] public prescriptions; /// @notice List of current prescription contracts

    /// @notice Set owner to the patient's address upon creation
    constructor(address _patient) {
        owner = _patient;
        registrar = Registrar(msg.sender);
    }

    /// @notice Only the owner may perform the action
    modifier onlyOwner() {
        require(msg.sender == owner, "Patient reverted: Requester is not owner");
        _;
    }

    /// @notice Only a permissioned party may perform the action
    modifier onlyPermissioned {
        require(permissioned[msg.sender] == true || msg.sender == owner, "Patient reverted: Requester is not permissioned");
        _;
    }

    function isPermissioned() external view returns(bool) {
        return permissioned[msg.sender];
    }

    function addPrescription(address contractAddress) external onlyPermissioned {
        require(registrar.isPrescriber(msg.sender), "Patient reverted: Requester is not prescriber");
        prescriptions.push(contractAddress);
    }

    function addPermissionedPrescriber(address party) external onlyOwner {
        require(permissioned[party] == false, "Patient reverted: Requester is already permissioned");
        permissioned[party] = true;
    }

    function removePermissionedPrescriber(address party) external onlyOwner {
        require(permissioned[party] == true, "Patient reverted: Requester is not permissioned");
        permissioned[party] = false;
    }

    function addPrescriptionPermissions(address prescriptionContract, address party) external onlyOwner {
        Prescription(prescriptionContract).addPermissionedPrescriber(party);
    }

    function removePrescriptionPermissions(address prescriptionContract, address party) external onlyOwner {
        Prescription(prescriptionContract).removePermissionedPrescriber(party);
    }

    function getPrescriptionList() external view returns(address [] memory) {
        return prescriptions;
    }

    function requestFill(address prescriptionContract) external onlyOwner {
        Prescription(prescriptionContract).requestFill();
    }
}


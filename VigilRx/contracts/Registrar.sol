// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "./Patient.sol";
import "./Prescriber.sol";
import "./Pharmacy.sol";

/// @title Global Registry contract
/// @author Austin Kugler, Alixandra Taylor
/// @notice The contract handles the creation of role contracts and validation of
///         contract address to specific roles
contract Registrar {
    address owner;

    // 1 == Patient, 2 == Prescriber, 3 == Pharmacy
    mapping(address => uint8) contractStatus;
    event NewAddress(address indexed contractAddress);

    constructor() {
        owner = msg.sender;
    }

    /// @notice Require that the sender of the transactions be the contract owner
    modifier onlyOwner() {
        require(msg.sender == owner, "Registrar reverted: Requester is not owner");
        _;
    }

    /// @notice Check if the given address corrosponds to a registered patient contract
    /// @param contractAddress The public address of the patient contract
    /// @return bool registry status
    function isPatient(address contractAddress) external view returns (bool) {
        if (contractStatus[contractAddress] == 1) {
            return true;
        }
        return false;
    }

    /// @notice Check if the given address corrosponds to a registered patient contract
    /// @param contractAddress The public address of the prescribercontract
    /// @return bool registry status
    function isPrescriber(address contractAddress) external view returns (bool) {
        if (contractStatus[contractAddress] == 2) {
            return true;
        }
        return false;
    }

    /// @notice Check if the given address corrosponds to a registered pharmacy contract
    /// @param contractAddress The public address of the pharmacy contract
    /// @return bool registry status
    function isPharmacy(address contractAddress) external view returns (bool) {
        if (contractStatus[contractAddress] == 3) {
            return true;
        }
        return false;
    }

    /// @notice Create a new patient contract
    /// @param patientAddress The public address of the new patient
    function createPatient(address patientAddress) external onlyOwner {
        Patient patient = new Patient(patientAddress);
        contractStatus[address(patient)] = 1;
        emit NewAddress(address(patient));
    }

    /// @notice Create a new prescriber contract
    /// @param prescriberAddress The public address of the new prescriber
    function createPrescriber(address prescriberAddress, uint40 npi) external onlyOwner {
        Prescriber prescriber = new Prescriber(prescriberAddress, npi);
        contractStatus[address(prescriber)] = 2;
        emit NewAddress(address(prescriber));
    }

    function createPharmacy(address pharmacyAddress, uint40 npi) external onlyOwner {
        Pharmacy pharmacy = new Pharmacy(pharmacyAddress, npi);
        contractStatus[address(pharmacy)] = 3;
        emit NewAddress(address(pharmacy));
    }
}

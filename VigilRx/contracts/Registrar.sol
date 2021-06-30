// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

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
    mapping (address => uint8) contractStatus;

    event NewAddress(address indexed contractAddress);

    constructor() {
        owner = msg.sender;
    }

    /// @notice Require that the sending of the transactions be the contract owner
    modifier onlyOwner() {
        assert(msg.sender == owner);
        _;
    }

    /// @notice Create a new patient contract
    /// @param patientAddress The public address of the new patient
    /// @return The address of the newly generated patient contract
    function createPatient(address patientAddress) external onlyOwner returns(address) {
        contractStatus[patientAddress] = 1;
        address patient = address(new Patient(patientAddress));
        emit NewAddress(patient);
        return patient;
    }

    /// @notice Create a new prescriber contract
    /// @param prescriberAddress The public address of the new prescriber
    /// @return The address of the newly generated prescriber contract
    function createPrescriber(address prescriberAddress, uint40 npi) external onlyOwner returns(address) {
        contractStatus[prescriberAddress] = 2;

        return address(new Prescriber(prescriberAddress, npi));
    }

    /// @notice Create a new pharmacy contract
    /// @param pharmacyAddress The public address of the new pharmacy
    /// @return The address of the newly generated pharmacy contract
    function createPharmacy(address pharmacyAddress, uint40 npi) external onlyOwner returns(address) {
        contractStatus[pharmacyAddress] = 3;

        return address(new Pharmacy(pharmacyAddress, npi));
    }

    /// @notice Create a new pharmacy contract
    /// @param contractAddress The public address of the new pharmacy
    /// @return The address of the newly generated pharmacy contract
    function isPatient(address contractAddress) external view returns(bool) {
        if(contractStatus[contractAddress] == 1) {
            return true;
        }

        return false;
    }

    function isPrescriber(address contractAddress) external view returns(bool) {
        if(contractStatus[contractAddress] == 2) {
            return true;
        }

        return false;
    }

    function isPharmacy(address contractAddress) external view returns(bool) {
        if(contractStatus[contractAddress] == 3) {
            return true;
        }

        return false;
    }
}

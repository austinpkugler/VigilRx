// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "./Registrar.sol";

/// @title Patient Role Contract
/// @author Austin Kugler, Alixandra Taylor
/// @notice The contract represents a patient in the system, handling permissioning
///         checks and tracking assigned prescription contracts
contract Patient {
    /// @notice Contract owner and registrar contract addresses
    address owner;
    Registrar public registrarContract;

    /// @notice Permissioned parties mapping, determines who is allowed certain actions
    mapping(address => bool) public permissioned;

    /// @notice List of current prescription contracts
    address[] public prescriptions;

    /// @notice Set owner to the patient's address upon creation
    constructor(address _patient) {
        owner = _patient;
        registrarContract = Registrar(msg.sender);
    }

    /// @notice Only the owner may perform the action
    modifier onlyOwner() {
        require(msg.sender == owner, "Request not sent by owner.");
        _;
    }

    /// @notice Only a permissioned party may perform the action
    modifier onlyPermissioned {
        require(msg.sender == owner || permissioned[msg.sender] == true, "Requester is not permissioned.");
        _;
    }

    function addPrescription(address contractAddress) public onlyPermissioned {
        require(registrarContract.isPrescriber(contractAddress), "Error: Requester is not registered as prescriber");
        prescriptions.push(contractAddress);
    }

    function addPermission(address party) public onlyOwner {
        if (permissioned[party] == false) {
            permissioned[party] = true;
        } else {
            revert();
        }
    }

    function removePermission(address party) public onlyOwner {
        if (permissioned[party] == true) {
            permissioned[party] = false;
        } else {
            revert();
        }
    }

    function isPermissioned() external view onlyPermissioned returns(bool) {
        return true;
    }
}

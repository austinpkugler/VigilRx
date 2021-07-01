// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;


contract Patient {

    address owner;
    mapping(address => bool) permissioned;
    address[] prescriptions;

    constructor(address _patient) {
        owner = _patient;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Request not sent by owner.");
        _;
    }

    modifier onlyPermissioned {
        require(msg.sender == owner || permissioned[msg.sender] == true, "Requester is not permissioned.");
        _;
    }

    function viewHistory() external view onlyPermissioned returns(address[] memory) {
        return prescriptions;
    }

    function addPrescription(address contractAddress) public onlyPermissioned {
        prescriptions.push(contractAddress);
    }

    function isPermissioned(address party) public view onlyPermissioned returns(bool) {
        return true;
    }

    function addPermissioned(address party) public onlyOwner {
        if (permissioned[party] == false) {
            permissioned[party] = true;
        } else {
            revert();
        }
    }

    function removePermissioned(address party) public onlyOwner {
        if (permissioned[party] == true) {
            permissioned[party] = false;
        } else {
            revert();
        }
    }

}

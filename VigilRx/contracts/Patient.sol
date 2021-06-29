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
        require(msg.sender == owner);
        _;
    }

    modifier onlyPermissioned {
        require(msg.sender == owner || permissioned[msg.sender] == true);
        _;
    }

    function viewHistory() external view onlyPermissioned returns(address[] memory) {
        return prescriptions;
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

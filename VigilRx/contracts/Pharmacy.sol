// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;


contract Pharmacy {

    uint40 public npi;
    address owner;
    address[] patients;
    mapping(address => address[]) prescriptions;

    constructor(address _pharmacy, uint40 _npi) {
        owner = _pharmacy;
        npi = _npi;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

}

// Title:           VigilRx Prescriber Contract
// Description:     This contract adds and tracks patient data, and allows the creation and editing of new Prescription contracts
// Author:          Alix Taylor, Austin Kugler
// Last Updated:    6/21/21
//
// Notes:   Handling of patient addresses is currently managed on-chain for practice. In final versions address and patient 
//          management will likely be handled off-chain for cost and performance reasons.

pragma solidity ^0.8.4;

// import prescription contract for creation
import "./Prescription.sol";

// This contract represents a validated Prescriber party
contract Prescriber{

    // State variables
    address owner;
    // National Provider Identifier [https://npiregistry.cms.hhs.gov/]
    uint32 public npi;

    // Maps prescriber-defined keys to lists of patient contract addresses
    mapping(bytes32 => address) _patientContracts;
    mapping(address => address []) _patientPrescriptions;

    // Temp Prescription contract handler
    Prescription private tempRx;

    // Only owner may execute
    modifier onlyOwner {
    require(msg.sender == owner);
    _;
    }

    // Initiate the contract with a given contract owner address and NPI
    constructor(address contractOwner, uint32 newNpi){
        owner = contractOwner;
        npi = newNpi;
    }

    // Add a new patient to the prescriber's list using a given key and address and create a new patient account
    function addPatient(bytes32 key, address pAddress) external onlyOwner{
        
        // If key doesn't already exist then create a new one
        require(_patientContracts[key] == address(0x0));
        _patientContracts[key] = pAddress;
    }

    // Modify the key assigned to a given patient in the mapping (per HIPAA requirement to be able to amend)
    function rekeyPatient(bytes32 oldKey, bytes32 newKey, address pAddress) external onlyOwner{
        
        // If the old key currently exists and the new one is empty then rekey the patient
        require(_patientContracts[oldKey] == pAddress);
        require(_patientContracts[newKey] == address(0x0));
        _patientContracts[newKey] = pAddress;
        _patientContracts[oldKey] = address(0x0);
    }

    // Create a new Prescription contract assigned to a given user.
    function newPrescription(bytes32 patientKey, uint32 _ndc, uint _quantity, uint _refills) external onlyOwner{
        // Make sure mapping is not currently empty
        require(_patientContracts[patientKey] != address(0x0));
        
        // Create the new prescription and store the address
        address newContract = address(new Prescription(
            address(this), 
            _patientContracts[patientKey],
            _ndc,
            _quantity,
            _refills));

        // Push the new address on to this patient's Rx contract list
        _patientPrescriptions[_patientContracts[patientKey]].push(newContract);
    }

    // Set the number of refills for a given prescription contract
    function setRefills(address rxAddress, uint refillCount) external onlyOwner{
        tempRx = Prescription(rxAddress);
        tempRx.setRefills(refillCount);
    }

    // View the status of a given prescription contract
    function viewRx(address rxAddress) external onlyOwner returns(PrescriptionInfo memory){
        tempRx = Prescription(rxAddress);
        tempRx.viewScript();
    }

    // View the history of a given patient contract if permissioned
    function viewHistory(bytes32 _patientKey) external onlyOwner view returns(address[] memory){
        return _patientPrescriptions[_patientContracts[_patientKey]];
    }
}
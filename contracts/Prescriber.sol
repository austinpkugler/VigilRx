pragma solidity ^0.8.4;

// import prescription contract for creation
import "./Prescription.sol";

contract Prescriber{

    // State variables
    address owner;
    uint32 public npi;

    // Maps prescriber-defined keys to patient contract addresses
    mapping(bytes32 => address) _patientContracts;
    mapping(address => address []) _patientPrescriptions;

    Prescription private newRx;

    modifier onlyOwner {
    require(msg.sender == owner);
    _;
    }

    constructor(address contractOwner, uint32 newNpi){
        owner = contractOwner;
        npi = newNpi;
    }

    // Add a new patient to the prescriber's list using a given key and address and create a new patient account
    // string key           Key for the new address
    // address pAddress     patient's address
    function addPatient(bytes32 key, address pAddress) external onlyOwner{
        
        // If key doesn't already exist then create a new one
        require(_patientContracts[key] == address(0x0));
        _patientContracts[key] = pAddress;
    }

    // Modify the key assigned to a given patient in the mapping
    function rekeyPatient(bytes32 oldKey, bytes32 newKey, address pAddress) external onlyOwner{
        
        // If the old key currently exists and the new one is empty then rekey the patient
        require(_patientContracts[oldKey] == pAddress);
        require(_patientContracts[newKey] == address(0x0));
        _patientContracts[newKey] = pAddress;
        _patientContracts[oldKey] = address(0x0);
    }

    function newPrescription(bytes32 patientKey, uint32 _ndc, uint _quantity, uint _refills) external onlyOwner{
        
        require(_patientContracts[patientKey] != address(0x0));
        
        address newContract = address(new Prescription(
            address(this), 
            _patientContracts[patientKey],
            _ndc,
            _quantity,
            _refills));

        _patientPrescriptions[_patientContracts[patientKey]].push(newContract);
    }

    // Set the number of refills for a given prescription contract
    function setRefills(address rxAddress, uint refillCount) external onlyOwner{

    }

    // View the status of a given prescription contract
    function viewRx(address rxAddress) external onlyOwner{
        
    }

    // View the history of a given patient contract if permissioned
    function viewHistory(bytes32 _patientKey) external onlyOwner view returns(address[] memory){
        return _patientPrescriptions[_patientContracts[_patientKey]];
    }
}
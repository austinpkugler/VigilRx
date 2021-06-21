// Title:           VigilRx Prescription Contract
// Description:     This contract maintains access and edit controls for the prescription's status and info
// Author:          Alix Taylor, Austin Kugler
// Last Updated:    6/21/21
//
// Notes:   This code is currently a dummy version for testing designed to be manipulated by the owner's address.
//          Final version will be interacted with indirectly thru a seperate Patient contract.

pragma solidity ^0.8.4;


// Public prescription storage standard
struct PrescriptionInfo {
    address prescriberAddress;      // Originating Prescriber contract
    uint32 ndc;                     // National Drug Code [https://www.accessdata.fda.gov/scripts/cder/ndc/index.cfm]
    uint quantity;                  // Total number for this prescription
    uint refills;                   // Refills remaining
}

// Prescription storage and access control script
contract Prescription {
    
    // Declare a new Rx data handler
    PrescriptionInfo p;

    address owner;                                  // Prescription owner address (patient)
    mapping(address => bool) _permissionedParties;  // Mapping for verifying permissioned parties by address

    constructor(address _patientAddress, uint32 _ndc, uint _quantity, uint _refills) {
        // Fill prescription struct fields
        p.prescriberAddress = msg.sender;
        p.ndc = _ndc;
        p.quantity = _quantity;
        p.refills = _refills;

        // Set Rx owner
        owner = _patientAddress;
    }

    // Only owner, prescriber, or permissioned parties may execute
    modifier onlyPermissioned {
        require(msg.sender == owner || _permissionedParties[msg.sender] == true || msg.sender == p.prescriberAddress);
        _;
    }

    // Only the prescriber originating the contract may execute
    modifier onlyPrescriber {
        require(msg.sender == p.prescriberAddress);
        _;
    }

    // Only the owner may execute
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    // Add new permissioned party
    function addPermission(address newPermission) public onlyOwner {
        if (_permissionedParties[newPermission] == false)
            _permissionedParties[newPermission] = true;
        else revert();
    }

    // Remove current permissioned party
    function removePermission(address newPermission) public onlyOwner {
        if (_permissionedParties[newPermission] == true)
            _permissionedParties[newPermission] = false;
        else revert();
    }

    // Set number of refills
    function setRefills(uint refillCount) external onlyPrescriber {
        p.refills = refillCount;
    }

    // Return current prescription status
    function viewScript() external view onlyPermissioned returns (PrescriptionInfo memory) {
        return p;
    }

    // Doesn't work as written, cannot iterate through a mapping
    //
    // function viewPermissions() external view onlyPermissioned returns (address[] memory) {
    //     address[] memory permList;

    //     for(uint i = 0; i < _permissionedParties.length; i++) {
    //         permList.push(_permissionedParties[i]);
    //     }

    //     return permList;
    // }
}

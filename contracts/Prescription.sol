pragma solidity ^0.8.4;

contract Prescription {
    struct PrescriptionInfo {
        address prescriberAddress;  
        uint32 ndc;
        uint quantity;
        uint refills;
    }

    // Prescription info struct
    PrescriptionInfo p;

    address owner;
    // List of permissioned contracts for interactions
    mapping(address => bool) _permissionedParties;

    constructor(address _prescriberAddress, address _patientAddress, uint32 _ndc, uint _quantity, uint _refills) {
        p.prescriberAddress = msg.sender;
        p.ndc = _ndc;
        p.quantity = _quantity;
        p.refills = _refills;

        owner = _patientAddress;
    }

    // Only availale to permissioned contracts
    modifier onlyPermissioned {
        require(msg.sender == owner || _permissionedParties[msg.sender] == true);
        _;
    }

    // Only available to the original Prescriber contract
    modifier onlyPrescriber {
        require(msg.sender == p.prescriberAddress);
        _;
    }

    // Only available to contract owner
    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    // Add permissioned party to the prescription
    function addPermission(address newPermission) public onlyOwner {
        if (_permissionedParties[newPermission] == false)
            _permissionedParties[newPermission] = true;
        else revert();
    }

    // Revoke permissions
    function removePermission(address newPermission) public onlyOwner {
        if (_permissionedParties[newPermission] == true)
            _permissionedParties[newPermission] = false;
        else revert();
    }

    // Change refills
    function setRefills(uint refillCount) external onlyPrescriber {
        p.refills = refillCount;
    }

    // View prescription contents and status
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

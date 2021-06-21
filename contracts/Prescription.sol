pragma solidity ^0.8.4;

contract Prescription {
    struct PrescriptionInfo {
        address prescriberAddress;  
        uint32 ndc;
        uint quantity;
        uint refills;
    }

    PrescriptionInfo p;

    address owner;
    mapping(address => bool) _permissionedParties;

    constructor(address _prescriberAddress, address _patientAddress, uint32 _ndc, uint _quantity, uint _refills) {
        p.prescriberAddress = msg.sender;
        p.ndc = _ndc;
        p.quantity = _quantity;
        p.refills = _refills;

        owner = _patientAddress;
    }

    modifier onlyPermissioned {
        require(msg.sender == owner || _permissionedParties[msg.sender] == true || msg.sender == p.prescriberAddress);
        _;
    }

    modifier onlyPrescriber {
        require(msg.sender == p.prescriberAddress);
        _;
    }

    modifier onlyOwner {
        require(msg.sender == owner);
        _;
    }

    function addPermission(address newPermission) public onlyOwner {
        if (_permissionedParties[newPermission] == false)
            _permissionedParties[newPermission] = true;
        else revert();
    }

    function removePermission(address newPermission) public onlyOwner {
        if (_permissionedParties[newPermission] == true)
            _permissionedParties[newPermission] = false;
        else revert();
    }

    function setRefills(uint refillCount) external onlyPrescriber {
        p.refills = refillCount;
    }

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

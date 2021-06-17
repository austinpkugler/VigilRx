pragma solidity ^0.8.0;

contract Prescription {
    struct prescriptionInfo {
        address prescriberAddress;
        address ownerAddress;
        uint32 ndc;
        uint256 quantity;
        uint256 refill;
    }
}

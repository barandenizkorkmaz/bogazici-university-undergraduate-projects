pragma solidity ^0.8.0;

// SPDX-License-Identifier: AGPL-3.0-only

contract hashHelper{
    constructor(){
        
    }
    
    fallback() external{
        revert();
    }
    
    function getHash(uint randomNumber) public view returns(bytes32 hashValue) {
      return keccak256(abi.encode(msg.sender, randomNumber));
    }
}

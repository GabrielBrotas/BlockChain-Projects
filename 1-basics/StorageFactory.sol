// SPDX-License_Identifier: MIT
pragma solidity ^0.6.0;

import "./SimpleStorage.sol"; // import the SimpleStorage code

// is = implements, now our StorageFactory wil inherit all the functions and variables from SimplStorage
contract StorageFactory is SimpleStorage {
    
    SimpleStorage[] public simpleStorageArray;
    
    function createSimpleStorageContract() public {
        // create a obj of type SimpleStorage class
        SimpleStorage simpleStorage = new SimpleStorage();
        
        simpleStorageArray.push(simpleStorage);
    }
    
    function sfStore(uint256 _simpleStorageIndex, uint _simpleStorageNumber) public {
        // in order to interact with one contract we need the Address and the ABI
        // Address we get from the array
        // we can get the ABI (Application Binary Interface) from the import 
        
        // access the address and from the Import get the contract we want to interact
        SimpleStorage simpleStorage = SimpleStorage(address(simpleStorageArray[_simpleStorageIndex]));
        
        simpleStorage.storeFavoriteNumber(_simpleStorageNumber);
    }
    
    function sfGet(uint256 _simpleStorageIndex) public view returns(uint256) {
        SimpleStorage simpleStorage = SimpleStorage(address(simpleStorageArray[_simpleStorageIndex]));
    
        return simpleStorage.retrieve();
        
    }
    
}
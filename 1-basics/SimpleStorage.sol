// SPDX-License-Identifier: MIT

// 1 - definin solidity version, use somethin between 0.6.0 and 0.9
pragma solidity >=0.6.0 <0.9.0;

// 2 - contract is a kind on Class in OOP language
contract SimpleStorage {
    
    uint256 favoriteNumber;
    bool favoriteBool;
    
    // create our own type
    struct People {
        uint256 favoriteNumber;
        string name;
    }

    // object
    People public person = People({favoriteNumber: 2, name: "Person 1"});
 
    // string to find someone favorite number  
    mapping( string => uint256) public nameToFavoriteNumber;
    
    // dynamic array, can have any size
    // if we want to limit the size of this array we can do People[2] for ex
    People[] public people;
    
    // there is 2 ways to store a variable
    // 1 - memory => data will only be stored during the execution of the function and delete after
    // 2 - storage => data will persist even after the function executes
    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        // way 1:
        // people.push(People({name: _name, favoriteNumber: _favoriteNumber}));
        // way 2:
        people.push(People( _favoriteNumber, _name));
        
        // the key is the name and the value the favorite number
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
    
    // functions
    function storeFavoriteNumber(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }
    
    // view => readOnly, read some state in the blockchain and not making a changing
    function retrieve() public view returns(uint256) {
        return favoriteNumber;
    }
}

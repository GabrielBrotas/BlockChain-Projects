// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 <0.9.0;

contract SimpleStorage {
    
    uint256 favoriteNumber;
    bool favoriteBool;
    
    struct People {
        uint256 favoriteNumber;
        string name;
    }

    People public person = People({favoriteNumber: 2, name: "Person 1"});
 
    mapping( string => uint256) public nameToFavoriteNumber;
    
    People[] public people;
    
    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People( _favoriteNumber, _name));
        
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
    
    function storeFavoriteNumber(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }
    
    function retrieve() public view returns(uint256) {
        return favoriteNumber;
    }
}
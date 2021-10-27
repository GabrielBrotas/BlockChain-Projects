// reward token we are going to give the users in platform
// contracts/BrottasToken.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract BrottasToken is ERC20 {
    constructor() ERC20("BrottasToken", "BTT") {
        _mint(msg.sender, 1000000000000000000000000); // 1M tokens, 1 000 000 * 10 **18
    }
}
// stake tokens => hold coins  to earn additional rewards
// unstake tokens
// issue tokens
// add allowed tokens
// get eth value
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol"; // permission check
import "@openzeppelin/contracts/token/ERC20/IERC20.sol"; // token interface to transfer tokens
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol"; // Price consumer

contract TokenFarm is Ownable {
    address[] public allowedTokens; //all allowed tokens

    // mapping token address => staker address => amount
    mapping(address => mapping(address => uint256)) public stakingBalance;
    mapping(address => uint256) public uniqueTokensStaked; // how many tokens each client hass in the farm
    address[] public stakers; // all stakers

    mapping(address => address) public tokenPriceFeedMapping; // mapping token address => price feed address

    IERC20 public brottasToken;

    constructor(address _brottasTokenAddress) public {
        brottasToken = IERC20(_brottasTokenAddress);    
    }

    function setPriceFeedContract(address _token, address _priceFeed) public onlyOwner {
        tokenPriceFeedMapping[_token] = _priceFeed;
    }

    // function that will hold client tokens, amount of tokens, and staker address
    function stakeTokens(uint256 _amount, address _token) public {
        // what tokens can they stake?
        // how much can they stake?
        require(_amount > 0, "Amount must be more than 0");
        require(tokenIsAllowed(_token), "Token is currently not allowed");

        // transfer => if we own the tokens
        // transferFrom => if we dont own the tokens and they have to call approve

        // give this token, from the sender to this farm and the specific amount
        IERC20(_token).transferFrom(msg.sender, address(this), _amount);

        updateUniqueTokensStaked(msg.sender, _token);

        // add to the staking balance the token => staker => amount
        stakingBalance[_token][msg.sender] =
            stakingBalance[_token][msg.sender] +
            _amount;

        // if this is his first unique token add him to the stakers
        if(uniqueTokensStaked[msg.sender] == 1) {
            stakers.push(msg.sender);
        }
    }

    // function that will unstake tokens from the clients
    function unstakeTokens(address _token) public {
        uint256 balance = stakingBalance[_token][msg.sender];

        require(balance > 0, "balance cannot be 0");

        IERC20(_token).transfer(msg.sender, balance);
        stakingBalance[_token][msg.sender] = 0;
        uniqueTokensStaked[msg.sender] = uniqueTokensStaked[msg.sender] - 1; 
    }

    function updateUniqueTokensStaked(address _user, address _token) internal {
        if (stakingBalance[_token][_user] <= 0) {
            uniqueTokensStaked[_user] = uniqueTokensStaked[_user] + 1;
        }
    }

    // function that will give rewards for the users
    function issueTokens() public onlyOwner {
        // issue tokens to all stakers
        for(uint256 stakersIndex = 0; stakersIndex < stakers.length; stakersIndex++) {
            address recipient = stakers[stakersIndex];

            // send them a token reward based on their total value locked
            uint256 usetTotalValue = getUserTotalValue(recipient);
            // brottasToken.transfer()
            brottasToken.transfer(recipient, usetTotalValue); // 1 <-> 1
        }

    }

    function getUserTotalValue(address _user) public view returns (uint256) {
        uint256 totalValue = 0;

        require(uniqueTokensStaked[_user] > 0, "User has no tokens to stake");

        for(uint256 tokenIndex = 0; tokenIndex < allowedTokens.length; tokenIndex++) {
            address token = allowedTokens[tokenIndex];
            totalValue = totalValue + getUserSingleTokenValue(_user, token);
        }
        return totalValue;
    }
    
    function getUserSingleTokenValue(address _user, address _token) public view returns (uint256) {
        if(uniqueTokensStaked[_user] <=0) {
            return 0;
        }

        // get price of the token * amount of tokens
        (uint256 price, uint256 decimals) = getTokenValue(_token);

        return (stakingBalance[_token][_user] * price / (10**decimals));
    }

    function getTokenValue(address _token) public view returns (uint256, uint256) {
        // price feed address
        address priceFeedAddress = tokenPriceFeedMapping[_token];

        AggregatorV3Interface priceFeed = AggregatorV3Interface(priceFeedAddress);
        (,int256 price,,,) =priceFeed.latestRoundData();
        uint256 decimals = uint256(priceFeed.decimals());

        return (uint256(price), decimals);
    }

    function addAllowedTokens(address _token) public onlyOwner {
        allowedTokens.push(_token);
    }

    function tokenIsAllowed(address _token) public returns (bool) {
        for (uint256 i = 0; i < allowedTokens.length; i++) {
            if (allowedTokens[i] == _token) {
                return true;
            }
        }
        return false;
    }
}

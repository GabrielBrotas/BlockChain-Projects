// SPDX-License-Identifier: MIT

pragma solidity >=0.6.0 < 0.9.0;

// importing from npm chainlink/contracts npm package
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
// interface compile down to an ABI, ABI tell solidity which function we can interact and use
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    using SafeMathChainlink for uint256; // this is no longer need in 0.8 and on
    
    mapping(address => uint) public addressToAmountFunded;
    address[] public funders;
    
    address owner;
    
    constructor() public {
        owner = msg.sender; // the owner of this contract is whoever deployed    
    }
    
    // when we difine a funcion as payable we say that this function
    // can be used to pay for things
    function fund() public payable {
        // greater than $50
        uint256 minimunUSD = 50 * 10 ** 18; // convert to gwei
        
        // make sure that match
         // it wil check the truthyness
        require(getConverstionRate(msg.value) >= minimunUSD, "You need to spend more ETH!");
        // if not true the user will get the money back
        
        
        // msg.sender and msg.value will exist in every transaction
        // msg.sender = sender of the function calldata
        // msg.value = how much they sent
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }
    
    function getVersion() public view returns(uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e); 
        return priceFeed.version();
    }
    
    function getPrice() public view returns(uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(0x8A753747A1Fa494EC906cE90E9f37563A8AF630e); 
        // (
        //   uint80 roundId,
        //   int256 answer,
        //   uint256 startedAt,
        //   uint256 updatedAt,
        //   uint80 answeredInRound
        // ) = priceFeed.latestRoundData();
        (, int256 answer, , ,) = priceFeed.latestRoundData();
        
        return uint256(answer * 10000000000); // convert in usd
    }
    
    function getConverstionRate(uint256 ethAmount) public view returns(uint256) {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        return ethAmountInUsd;
        
    }
    
    // modifier is a kind of middleware
    modifier onlyOwner {
        // before run the code, check this require
        require(msg.sender == owner);
        // and execute whathever the next code is
        _;
    }
    
    function withDraw() payable onlyOwner public {
        
        // require(msg.sender == owner) // just the owner can get the balance
        
        // send eth from one address to another
        // this is a keyword in solidity, is the contract we are interacting
        // address() => address of the contract we currently in
        // whoever call this function transfer all the money in this contract
        msg.sender.transfer(address(this).balance);
        
        for(uint256 i = 0; i < funders.length; i++) {
            address funder = funders[i];
            addressToAmountFunded[funder] = 0;
        }
        
        // reset the array
        funders = new address[](0);
    }
    
}
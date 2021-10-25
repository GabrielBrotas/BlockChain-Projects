// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract FundMe {
    using SafeMathChainlink for uint256; // this is no longer need in 0.8 and on

    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;

    address owner;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) public {
        owner = msg.sender; // the owner of this contract is whoever deployed
        priceFeed = AggregatorV3Interface(_priceFeed);
    }

    function fund() public payable {
        uint256 minimunUSD = 50 * 10**18; // convert to gwei

        require(
            getConverstionRate(msg.value) >= minimunUSD,
            "You need to spend more ETH!"
        );

        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
    }

    function getConverstionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        return ethAmountInUsd;
    }

    // modifier is a kind of middleware
    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function withDraw() public payable onlyOwner {
        msg.sender.transfer(address(this).balance);

        for (uint256 i = 0; i < funders.length; i++) {
            address funder = funders[i];
            addressToAmountFunded[funder] = 0;
        }

        // reset the array
        funders = new address[](0);
    }
    
    function getEntranceFee() public view returns (uint256) {
        // mimimumUSD
        uint256 mimimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (mimimumUSD * precision) / price;
    }
}

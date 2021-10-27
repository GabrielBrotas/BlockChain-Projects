// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Lottery is VRFConsumerBase, Ownable {
    address payable[] public players;
    address payable public recentWinner;
    uint256 public randomness;

    AggregatorV3Interface internal ethUsdPriceFeed;

    uint256 public usdEntryFee;

    // OPEN => 0, CLOSED => 1, CALCULATING_WINNER => 2
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lottery_state;

    event RequestedRandomness(bytes32 requestId);

    // in order to get a random number we need to use this variables
    uint256 public fee;
    bytes32 public keyhash;

    constructor(
        address _priceFeedAddress,
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyhash
    ) public VRFConsumerBase(_vrfCoordinator, _link) {
        usdEntryFee = 50 * (10**18);
        // converter of eth to the address we want ex: Mainnet eth=> usd, Rinkeby eth=>usd...
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;

        fee = _fee;
        keyhash = _keyhash;
    }

    function enter() public payable {
        require(lottery_state == LOTTERY_STATE.OPEN);
        // minimun $50

        require(msg.value >= getEntranceFee(), "Not enough eth!!");

        players.push(msg.sender);
    }

    function getEntranceFee() public view returns (uint256) {
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * 10**10; // by default Rinkeby network has 8 decimals so we will convert to 18 multipliying by 10**10

        uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice;
        return costToEnter;
    }

    function startLottery() public onlyOwner {
        require(
            lottery_state == LOTTERY_STATE.CLOSED,
            "can't start a new lottery yet!"
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        // randoness is insecurity in production so we'll never going to use

        // conver in a uint
        // uint256(
        // hashing algorithm
        //     keccack256(
        //         // global keyworkd
        //         abi.encodePacked(
        //             nonce, // predictable
        //             msg.sender, // predictable
        //             block.difficulty, // can be manipulated by the miners
        //             block.timestamp // predictable
        //         )
        //     )
        // ) % players.length; //
        // blockchain by itself is not able to generate a random number because every node needs the same value

        lottery_state = LOTTERY_STATE.CALCULATING_WINNER; // avoid others functions to be call

        // this func come from VRFConsumerBase interface
        bytes32 requestId = requestRandomness(keyhash, fee); // this func will request the randomness, the fulfillRandomness wil get the result
        emit RequestedRandomness(requestId);
    }

    // override means that we will override the original fulfillRandomness func from VRFConsumerBase
    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        require(
            lottery_state == LOTTERY_STATE.CALCULATING_WINNER,
            "you aren't there yet"
        );
        require(_randomness > 0, "random-not-found");

        uint256 indefOfWinner = _randomness % players.length;
        recentWinner = players[indefOfWinner];
        // 7 players
        // 22 random number
        // 22 / 7 => 1 is the remaining

        // give all money in this address to the winner
        recentWinner.transfer(address(this).balance);

        // reset array
        players = new address payable[](0);
        lottery_state == LOTTERY_STATE.CLOSED;
        randomness = _randomness;
    }
}

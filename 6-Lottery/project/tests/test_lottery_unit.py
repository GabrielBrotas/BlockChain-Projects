from brownie import Lottery, accounts, config, network, exceptions
from web3 import Web3
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_script import (
    LOCAL_BLOCKCHAIN_ENVIROMENTS,
    fund_with_link,
    get_account,
    get_contract,
)
import pytest

# 1 eth value = $4,215.42
# $50 dol to eth = 0.011861214 eth
# we expect to get 0.012 eth or 12000000000000000 wei
# def test_get_entrance_fee():
#     account = accounts[0]

#     ethToUsdAddress = config["networks"][network.show_active()]["eth_usd_price_feed"]
#     lottery = Lottery.deploy(ethToUsdAddress, {"from": account})

#     assert lottery.getEntranceFee() > Web3.toWei(0.011, "ether")
#     assert lottery.getEntranceFee() < Web3.toWei(0.014, "ether")


def test_get_entrance_fee():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip()
    lottery = deploy_lottery()

    # Act
    # 2000 eth /use
    # useEntryFee is 50
    # 2000/1 = 50 50/x = 0.025
    expected_entrance_fee = Web3.toWei(0.025, "ether")
    entrance_fee = lottery.getEntranceFee()

    # Assert
    assert expected_entrance_fee == entrance_fee


def test_cant_enter_unless_started():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip()
    lottery = deploy_lottery()

    # raises execption if try to enter in lottery closed
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})


def test_can_start_and_enter_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip()

    lottery = deploy_lottery()
    account = get_account()

    lottery.startLottery({"from": account})
    value = lottery.getEntranceFee() + 100000

    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    assert lottery.players(0) == account


def test_can_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip()

    lottery = deploy_lottery()
    account = get_account()

    lottery.startLottery({"from": account})
    value = lottery.getEntranceFee() + 100000

    lottery.enter({"from": account, "value": value})
    fund_with_link(lottery)

    lottery.endLottery({"from": account})

    assert lottery.lottery_state() == 2


def test_can_pick_winner_correctly():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip()

    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})

    value = lottery.getEntranceFee() + 100000

    lottery.enter({"from": account, "value": value})
    lottery.enter({"from": get_account(index=1), "value": value})
    lottery.enter({"from": get_account(index=2), "value": value})

    fund_with_link(lottery)

    transaction = lottery.endLottery({"from": account})

    # find inside the RequestRandomness the requestid passed
    request_id = transaction.events["RequestRandomness"]["requestId"]

    STATIC_RNG = 777
    # simulate call the callBackWithRandomness func from the vrf contact
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, STATIC_RNG, lottery.address, {"from": account}
    )

    starting_balance_of_account = account.balance()
    balance_of_lottery = lottery.balance()

    # 777 % 3 => 0
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == starting_balance_of_account + balance_of_lottery
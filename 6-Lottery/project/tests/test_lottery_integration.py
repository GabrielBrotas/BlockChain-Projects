# rinkeby as integration test
from brownie import network
import pytest
from scripts.deploy_lottery import deploy_lottery
from scripts.helpful_script import (
    LOCAL_BLOCKCHAIN_ENVIROMENTS,
    fund_with_link,
    get_account,
)
import time


def test_can_pick_winner():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        pytest.skip()

    lottery = deploy_lottery()
    account = get_account()

    lottery.startLottery({"from": account})

    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})

    fund_with_link(lottery)

    lottery.endLottery({"from": account})
    time.sleep(60)
    assert lottery.recentWinner() == account
    assert lottery.getBalance() == 0

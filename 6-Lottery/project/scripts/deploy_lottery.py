from brownie import Lottery, config, network
from scripts.helpful_script import get_account, get_contract, fund_with_link
import time


def deploy_lottery():
    # >brownie accouts list // to check the local accounts
    # account = get_account(id="gabriel-account")
    account = get_account()

    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        # get the verify key but if dont exists set to false
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print("Deployed lottery")
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]

    starting_transaction = lottery.startLottery({"from": account})
    starting_transaction.wait(1)
    print("lottery start")


def join_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    # .025000000000000000
    print(value)
    transaction = lottery.enter({"from": account, "value": value})
    transaction.wait(1)
    print("You entered in the lottery")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]

    # fund the contract to make the request in requestRandomness
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    print('funded')
    # then end the contract
    ending_transaction = lottery.endLottery({"from": account})
    ending_transaction.wait(1)
    time.sleep(60)
    print(f"{lottery.recentWinner()} is the new winner")


def main():
    deploy_lottery()
    start_lottery()
    join_lottery()
    end_lottery()

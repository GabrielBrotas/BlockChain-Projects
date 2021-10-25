from scripts.helpful_script import get_account, LOCAL_BLOCKCHAIN_ENVIROMENTS
from scripts.deploy import deploy_fund_me
from brownie import network, accounts, exceptions
import pytest


def test_can_fund_and_withdraw():
    account = get_account()
    fund_me = deploy_fund_me()
    entrance_fee = fund_me.getEntranceFee() + 100

    print({entrance_fee})
    transaction = fund_me.fund({"from": account, "value": entrance_fee})
    transaction.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee

    transaction2 = fund_me.fund({"from": account})
    transaction2.wait(1)

    assert fund_me.addressToAmountFunded(account.address) == 0


# >brownie test -k test_only_owner_can_withdraw --network rinkeby
# this will try run the tests with rinkeby network and not gonna execute the test below
def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        # pip install pytest
        pytest.skip("only for local test")

    fund_me = deploy_fund_me()

    bad_actor = accounts.add()

    # we expect this error
    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.withDraw({"from": bad_actor})

from brownie import network, exceptions
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    INITIAL_PRICE_FEED_VALUE,
    get_account,
    get_contract,
)
from scripts.deploy import deploy_token_farm_and_brottas_token
import pytest


def test_set_price_feed_contract():
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local test")

    account = get_account()
    non_owner = get_account(index=1)

    token_farm, btt_token = deploy_token_farm_and_brottas_token()

    # Act
    token_farm.setPriceFeedContract(
        btt_token.address, get_contract("eth_usd_price_feed"), {"from": account}
    )

    # Assert
    assert token_farm.tokenPriceFeedMapping(btt_token.address) == get_contract(
        "eth_usd_price_feed"
    )

    with pytest.raises(exceptions.VirtualMachineError):
        token_farm.setPriceFeedContract(
            btt_token.address, get_contract("eth_usd_price_feed"), {"from": non_owner}
        )


# the amount_staked value will come from conftest.py
def test_stake_tokens(amount_staked):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local test")

    account = get_account()
    token_farm, btt_token = deploy_token_farm_and_brottas_token()

    btt_token.approve(token_farm.address, amount_staked, {"from": account})
    token_farm.stakeTokens(amount_staked, btt_token.address, {"from": account})

    assert (
        token_farm.stakingBalance(btt_token.address, account.address) == amount_staked
    )
    assert token_farm.uniqueTokensStaked(account.address) == 1
    assert token_farm.stakers(0) == account.address
    return token_farm, btt_token


def test_issue_tokens(amount_staked):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local test")

    account = get_account()
    token_farm, btt_token = test_stake_tokens(amount_staked)

    starting_ballance = btt_token.balanceOf(account.address)

    # Act
    token_farm.issueTokens({"from": account})

    # Assert
    """
        we are staking 1btt_token == in price to 1 ETH
        we should get 2000btt token in reward
        since the price of eth is $2000
    """
    assert (
        btt_token.balanceOf(account.address)
        == starting_ballance + INITIAL_PRICE_FEED_VALUE
    )


def test_unstake_tokens(amount_staked):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local test")

    account = get_account()
    token_farm, btt_token = test_stake_tokens(amount_staked)

    # Act
    token_farm.unstakeTokens(btt_token.address, {"from": account})

    # Assert
    assert token_farm.stakingBalance(btt_token.address, account.address) == 0
    assert token_farm.uniqueTokensStaked(account.address) == 0


def test_get_user_total_value(amount_staked):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local test")

    account = get_account()
    token_farm, btt_token = test_stake_tokens(amount_staked)

    # print(amount_staked) => 1000000000000000000, amount * 2000 PRICE FEED VALUE
    assert token_farm.getUserTotalValue(account.address) == amount_staked * 2000 

def test_get_token_value(amount_staked):
    # Arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for local test")

    token_farm, btt_token = test_stake_tokens(amount_staked)
    
    assert token_farm.getTokenValue(btt_token.address) == (INITIAL_PRICE_FEED_VALUE, 18)

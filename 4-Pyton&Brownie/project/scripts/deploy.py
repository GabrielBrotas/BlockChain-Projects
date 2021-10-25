# import the Contracts direct
from brownie import accounts, config, network, SimpleStorage


def deploy_simple_storage():
    # account = accounts[0]
    # # account = accounts.load('gabriel-account')
    # account = accounts.add(config["wallets"]["from_key"])
    # print(account)
    account = get_account()
    simple_storage = SimpleStorage.deploy({"from": account})

    stored_value = (
        simple_storage.retrieve()
    )  # brownie knows if this is a call or transaction
    print(stored_value)

    # every time we do a transaction we need to pass a from parameter, which account is sending
    transaction = simple_storage.storeFavoriteNumber(15, {"from": account})
    transaction.wait(1)

    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()

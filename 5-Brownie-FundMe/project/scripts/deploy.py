from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_script import (
    LOCAL_BLOCKCHAIN_ENVIROMENTS,
    deploy_mocks,
    get_account,
)

def deploy_fund_me():
    account = get_account()

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        print('not local')
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        print('local')
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    # fund_me = FundMe.deploy(price_feed_address, {"from": account}, publish_source=True)
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"contract deployed to {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()
    pass

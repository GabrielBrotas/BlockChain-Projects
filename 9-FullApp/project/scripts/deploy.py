import os
from brownie import BrottasToken, TokenFarm, config, network
from scripts.helpful_scripts import get_account, get_contract
from web3 import Web3
import yaml
import json
import shutil

KEPT_BALANCE = Web3.toWei(100, "ether")


def deploy_token_farm_and_brottas_token(should_update_front_end=False):
    """
    Deploys the token farm and brottas token.
    """
    account = get_account()
    brottas_token = BrottasToken.deploy({"from": account})
    token_farm = TokenFarm.deploy(
        brottas_token.address,
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )

    # Give the token farm tokens to start with and keep some for testing
    transaction = brottas_token.transfer(
        token_farm.address,
        brottas_token.totalSupply() - KEPT_BALANCE,
        {"from": account},
    )
    transaction.wait(1)

    # brottas_token, weth_token, fau_token/dai
    weth_token = get_contract("weth_token")
    fau_token = get_contract("weth_token")

    dictonary_of_allowed_tokens = {
        brottas_token: get_contract("dai_usd_price_feed"),
        fau_token: get_contract("dai_usd_price_feed"),
        weth_token: get_contract("eth_usd_price_feed"),
    }
    add_allowed_tokens(token_farm, dictonary_of_allowed_tokens, account)
    
    if should_update_front_end:
        update_front_end()
    return token_farm, brottas_token

def add_allowed_tokens(token_farm, dictonary_of_allowed_tokens, account):
    for token in dictonary_of_allowed_tokens:
        add_tx = token_farm.addAllowedTokens(token.address, {"from": account})
        add_tx.wait(1)

        set_tx = token_farm.setPriceFeedContract(
            token.address, dictonary_of_allowed_tokens[token], {"from": account}
        )
        set_tx.wait(1)

    return token_farm

def update_front_end():
    # Send the build folder
    copy_folders_to_front_end('./build', './front_end/src/chain-info')
    
    # Sending the front end our config in JSON format
    with open("brownie-config.yaml", "r") as brownie_config:
        config_dict = yaml.load(brownie_config, Loader=yaml.FullLoader)
        
        with open("./front_end/src/brownie-config.json", "w") as brownie_config_json:
            json.dump(config_dict, brownie_config_json)

    print("Front end updated!")

def copy_folders_to_front_end(src, dest):
    if os.path.exists(dest):
        # if the folder exists we delete
        shutil.rmtree(dest)
    # and copy
    shutil.copytree(src, dest)

def main():
    deploy_token_farm_and_brottas_token(should_update_front_end=True)

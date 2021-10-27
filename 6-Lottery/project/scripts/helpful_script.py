from brownie import (
    network,
    accounts,
    config,
    MockV3Aggregator,
    Contract,
    VRFCoordinatorMock,
    LinkToken,
    interface
)


DECIMALS = 8
STARTING_PRICE = 200000000000

LOCAL_BLOCKCHAIN_ENVIROMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIROMENTS = ["mainnet-fork", "mainnet-fork-dev"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]

    if id:
        return accounts.load(id)

    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIROMENTS
        or network.show_active() in FORKED_LOCAL_ENVIROMENTS
    ):
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token":  LinkToken
}


def get_contract(contract_name):
    """this function will grab the contract addresses from the brownie config
    if defined, otherwise it will deploy a mock version of that contract and
    return that mock contract.

        Args:
            contract_name (string)

        Returns:
            brownie.network.contract.ProjectContract: The most recently deployed
            version of this contract.
            [-1]
    """
    contract_type = contract_to_mock[contract_name]

    # development
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIROMENTS:
        # MockV3Aggregator.length
        if len(contract_type) <= 0:
            deploy_mocks()

        # MockV3Aggregator[-1]
        contract = contract_type[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]

        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
        # MockV3Aggregator.abi, MockV3Aggregator._name

    return contract


def deploy_mocks(decimals=DECIMALS, initial_value=STARTING_PRICE):
    account = get_account()
    # MockV3Aggregator is a list of contracts address we deployed
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("mocks deployed")


def fund_with_link(contract_address, account=None, link_token=None, amount=100000000000000000): #0.1Link:
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    
    # 1 - manually
    # tx = link_token.transfer(contract_address, amount, {"from": account})
    
    # 2 - with interface, we dont need the ABI because brownie know that can compile to a abi
    link_token_contract = interface.LinkTokenInterface(link_token.address)

    tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    tx.wait(1)

    print("Fund contract!")
    return tx
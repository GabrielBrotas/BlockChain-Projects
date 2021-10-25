# read a contract that we deployed
from brownie import SimpleStorage, accounts, config


def read_contract():
    # SimpleStorage is a array, each index is a address of a deployment we've made.
    simple_storage = SimpleStorage[-1] # 0 is the first deploy and -1 the latest

    print(simple_storage.retrieve())
    pass


def main():
    read_contract()

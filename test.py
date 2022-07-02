#!/bin/python3
from pprint import pprint
from pyzil.zilliqa import chain
from pyzil.account import Account
from pyzil.contract import Contract
from pyzil.zilliqa.units import Zil, Qa

chain.set_active_chain(chain.LocalTestNet)


nodes_keys = [
    "9EDBE40B462AFD43E0CC7153E24589DFCCA01DDDD56CB5493ADE0A739BEF4FDB",
    "9FA927355DB62EE1C86820A9CC94876E0DF356F2970151304393568C8F726969",
    "8E8D36EE98D075BEF2D227E93F6613BFF0FC5599B08410F3A4D37F8076EB246A",
]

to_account = Account(private_key="05C3CF3387F31202CD0798B7AA882327A1BD365331F90954A58C18F61BD08FFC")
balance2 = to_account.get_balance_qa()
print("ToAccount balance: {}".format(balance2), to_account.address0x, to_account.public_key, to_account.bech32_address)



min_gas = Qa(chain.active_chain.api.GetMinimumGasPrice())
print("Min gas:{}".format(min_gas))

def get_zil_from_node(nodes_keys, to_account):
    txn_info_list = []
    for key in nodes_keys:
        if not key:
            continue
        account = Account(private_key=key)
        # send all zils
        balance = account.get_balance_qa()
        amount = (balance - min_gas * 2)/4
        if amount <= 0:
            continue
        
        print("Node balance:{}, transfer amount:{}".format(balance, amount))
        txn_info = account.transfer(to_addr=to_account.bech32_address, zils=(amount), gas_price=min_gas, gas_limit=50)
        pprint(txn_info)
        
        txn_info_list.append(txn_info)

    for txn_info in txn_info_list:   
        txn_details = chain.active_chain.wait_txn_confirm(txn_info["TranID"], timeout=300)
        pprint(txn_details)
        if txn_details and txn_details["receipt"]["success"]:
            print("Txn success")
        else:
            print("Txn failed")

    print("ToAccount balance: {}".format(to_account.get_balance_qa()))


#get_zil_from_node(nodes_keys, to_account)

def deploy_contract(to_account, scilla_file, init):
    code = open(scilla_file).read()
    contract = Contract.new_from_code(code)
    print( contract)

    # set account before deploy
    contract.account = to_account

    
    txn_details = contract.deploy(init_params=init, timeout=300, sleep=10, gas_price=min_gas, gas_limit=13000)
    pprint(txn_details)
    print(contract.status, contract.address)
    print("ToAccount balance: {}".format(to_account.get_balance_qa()))
    return contract

init = [
    Contract.value_dict("_scilla_version", "Uint32", "0"),
    #Contract.value_dict("initial_admin", "ByStr20", to_account.address0x)
    Contract.value_dict("owner", "ByStr20", to_account.address0x)
]
#deploy_contract(to_account, "HelloWorld.scilla", init)

def call_contract(to_account, contract_addr):
    contracts = to_account.get_contracts()
    pprint(contracts)
    #contract = Contract.load_from_address(contract_addr)
    for contract in contracts:
        if contract.address == contract_addr:  
            contract.account = to_account

            resp = contract.call(method="getHello", params=[])
            pprint(resp)

            resp = contract.call(method="setHello", params=[Contract.value_dict("msg", "String", "hi contract.")])
            pprint(resp)

            resp = contract.call(method="getHello", params=[])
            pprint(resp)
call_contract(to_account, '3e997163d8568bbf63ed246f0357031ef2efa96e')


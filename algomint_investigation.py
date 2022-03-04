import json
import requests

algomint_address = 'ETGSQKACKC56JWGMDAEP5S2JVQWRKTQUVKCZTMPNUGZLDVCWPY63LSI3H4'
goBTC = 386192725
goETH = 386195940

response = requests.get(f'https://api.algoexplorer.io/idx2/v2/accounts/{algomint_address}/transactions')
transaction_dict = response.json()

receiver_set = set()
goBTC_set = set()
goETH_set = set()

for tx in transaction_dict['transactions']:
    if 'asset-transfer-transaction' in tx:
        receiver = tx['asset-transfer-transaction']['receiver']
        asset = tx['asset-transfer-transaction']['asset-id']
        if receiver != algomint_address:
            receiver_set.add(receiver)
            if asset == goBTC:
                goBTC_set.add(receiver)
            if asset == goETH:
                goETH_set.add(receiver)

print(f'Total Mint Addresses From Algomint: {len(receiver_set)}')
print(f'Total goBTC Only Mint Addresses: {len((goBTC_set^goETH_set)&goBTC_set)}')
print(f'Total goETH Only Mint Addresses: {len((goETH_set^goBTC_set)&goETH_set)}')
print(f'Total Double Mint Addresses: {len(goBTC_set.intersection(goETH_set))}')
print(receiver_set)

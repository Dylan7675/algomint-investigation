import json
import requests

transaction_dict = {}
receiver_set = set()
goBTC_set = set()
goETH_set = set()

#Algomint Addess and Asset ID's
algomint_address = 'ETGSQKACKC56JWGMDAEP5S2JVQWRKTQUVKCZTMPNUGZLDVCWPY63LSI3H4'
goBTC = 386192725
goETH = 386195940

# For Paginated API Call Results. Max Limit 1,000 Transactions
next_token = ''

#Iterating over 10 pages of transactions
for i in range(9):
    response = requests.get(f'https://api.algoexplorer.io/idx2/v2/accounts/{algomint_address}/transactions?limit=1000&next={next_token}')
    if transaction_dict:
        transaction_dict['transactions'].extend(response.json()['transactions'])
    else:
        transaction_dict = response.json()
    next_token = response.json()['next-token']

#Identifying asset transfer transactions sent by Algomint and categorizing into goBTC/goETH sets
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

#Dump data to files
with open('mint_addresses.txt', 'w') as file:
    for item in receiver_set:
        file.write(item + '\n')
    print('Mint Receiving Addresses Dumped as mint_addresses.txt')

with open('mint_transactions.json', 'w') as file:
    json.dump(transaction_dict, file)
    print('Transactions Dumped as mint_transactions.json')


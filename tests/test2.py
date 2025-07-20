import requests
from stellar_sdk import Keypair, Server
import os
import json

# Stellar Testnet Account Creation Script
# This script loads a pre-existing keypair JSON file to fund an account on the Stellar Testnet.

KEYSTORE_DIR = "./keystore"

keypair_json = os.path.join(KEYSTORE_DIR, "GB5M7WXWUCQV4PE4XU6AP5DOONEZVNAXF47CKGAF6NZ4CJGU4AECD4F5_keystore.json")

with open(keypair_json, "r") as f:
    keypair_data = json.load(f)

keypair = Keypair.from_secret(keypair_data["secret"])

print("Public Key: " + keypair.public_key)
print("Secret Seed: " + keypair.secret)

server = Server("https://horizon-testnet.stellar.org")
# account = server.accounts().account_id("GDNTF4ASUK5BPAHTDF45OS5KF2HJ3JQKKACKN6QBZ6IZUZEY7K5B4HHO").call()

url = "https://friendbot.stellar.org"
response = requests.get(url, params={"addr": "GDNTF4ASUK5BPAHTDF45OS5KF2HJ3JQKKACKN6QBZ6IZUZEY7K5B4HHO"})
if response.status_code == 200:
    print(f"SUCCESS! You have a new account :)\n{response.text}")
else:
    print(f"ERROR! {response.status_code} {response.text}")

# for balance in account['balances']:
#     print(f"Type: {balance['asset_type']}, Balance: {balance['balance']}")




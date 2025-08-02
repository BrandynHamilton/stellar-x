import requests
from stellar_sdk import Keypair, Server
import os
import json

# Stellar Testnet Account Creation Script
# This script loads a pre-existing keypair JSON file to fund an account on the Stellar Testnet.

KEYSTORE_DIR = "./keystore"

def main(address):

    keypair_json = os.path.join(KEYSTORE_DIR, f"{address}_keystore.json")

    with open(keypair_json, "r") as f:
        keypair_data = json.load(f)

    keypair = Keypair.from_secret(keypair_data["secret"])

    print("Public Key: " + keypair.public_key)
    print("Secret Seed: " + keypair.secret)

    server = Server("https://horizon-testnet.stellar.org")

    try:
        account = server.accounts().account_id(keypair.public_key).call()
        for balance in account['balances']:
            print(f"Type: {balance['asset_type']}, Balance: {balance['balance']}")
        print("Account already exists.")
        return
    except Exception as e:
        print(f"Error fetching account: {e}")

        url = "https://friendbot.stellar.org"
        response = requests.get(url, params={"addr": keypair.public_key})
        if response.status_code == 200:
            print(f"SUCCESS! You have a new account :)\n{response.text}")
            account = server.accounts().account_id(keypair.public_key).call()
            for balance in account['balances']:
                print(f"Type: {balance['asset_type']}, Balance: {balance['balance']}")
            
            return
        else:
            print(f"ERROR! {response.status_code} {response.text}")
        
if __name__ == "__main__":
    public_key="GCEGI5E4ZLGZICOMV3IIA3DJPTU5XKWIFGXD4SZ5TVKGKRMSWLGYRUSW"

    if not os.path.exists(KEYSTORE_DIR):
        print(f"Keystore directory '{KEYSTORE_DIR}' does not exist. Please create it and add the keypair JSON file.")
    else:
        main(public_key)
from stellar_sdk import Server, Keypair
import os
import json

KEYSTORE_DIR = "./keystore"

def load_account(
        public_key="GB5M7WXWUCQV4PE4XU6AP5DOONEZVNAXF47CKGAF6NZ4CJGU4AECD4F5",
        testnet=False
    ):
    """
    Load an account using the provided public key and secret.
    """

    if testnet:
        horizon_url = "https://horizon-testnet.stellar.org"
    else:
        horizon_url = "https://horizon.stellar.org"

    keypair_json = os.path.join(KEYSTORE_DIR, f"{public_key}_keystore.json")

    with open(keypair_json, "r") as f:
        keypair_data = json.load(f)

    keypair = Keypair.from_secret(keypair_data["secret"])

    server = Server(horizon_url=horizon_url)
    account = server.accounts().account_id(keypair.public_key).call()
    
    print(f"Account loaded: {account['id']}")
    print(f"Balances: {account['balances']}")
    
    return account
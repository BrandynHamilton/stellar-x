"""
Stellar uses signatures as authorization. Transactions always need authorization
from at least one public key in order to be considered valid. Generally,
transactions only need authorization from the public key of the source account.

Transaction signatures are created by cryptographically signing the
transaction object contents with a secret key. Stellar currently uses the ed25519 signature
scheme, but there’s also a mechanism for adding additional types of public/private key schemes.
A transaction with an attached signature is considered to have authorization from that public key.

In two cases, a transaction may need more than one signature. If the transaction has
operations that affect more than one account, it will need authorization from every account
in question. A transaction will also need additional signatures if the account associated
with the transaction has multiple public keys.

See: https://developers.stellar.org/docs/glossary/multisig/
"""

from stellar_sdk import Asset, Keypair, Network, Server, Signer, TransactionBuilder
import os
from dotenv import load_dotenv
import requests
load_dotenv()

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
PRIVATE_KEY_2 = os.getenv("PRIVATE_KEY_2")

server = Server(horizon_url="https://horizon-testnet.stellar.org")
root_keypair = Keypair.from_secret(
    PRIVATE_KEY
)
root_account = server.load_account(account_id=root_keypair.public_key)
secondary_keypair = Keypair.from_secret(
    PRIVATE_KEY_2
)

secondary_signer = Signer.ed25519_public_key(
    account_id=secondary_keypair.public_key, weight=1
)

account_data = server.accounts().account_id(root_keypair.public_key).call()
print("Thresholds:", account_data["thresholds"])
print("Signers:", account_data["signers"])

transaction = (
    TransactionBuilder(
        source_account=root_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
    )
    .append_set_options_op(
        master_weight=1,  # set master key weight
        low_threshold=1,
        med_threshold=2,  # a payment is medium threshold
        high_threshold=2,  # make sure to have enough weight to add up to the high threshold!
        signer=secondary_signer,
    )
    .set_timeout(30)
    .build()
)

# only need to sign with the root signer as the 2nd signer won't
# be added to the account till after this transaction completes
print("Loaded account:", root_account.account)
print("Root pubkey:", root_keypair.public_key)

transaction.sign(root_keypair)
transaction.sign(secondary_keypair)
response = server.submit_transaction(transaction)
print(response)

root_account = server.load_account(account_id=root_keypair.public_key)

account_details = server.accounts().account_id(root_keypair.public_key).call()
print(account_details["signers"])

destination = "GB6NVEN5HSUBKMYCE5ZOWSK5K23TBWRUQLZY3KNMXUZ3AQ2ESC4MY4AQ"

url = "https://friendbot.stellar.org"
response = requests.get(url, params={"addr": destination})
if response.status_code == 200:
    print(f"SUCCESS! You have a new account :)\n{response.text}")
    account = server.accounts().account_id(destination).call()
    for balance in account['balances']:
        print(f"Type: {balance['asset_type']}, Balance: {balance['balance']}")

# now create a payment with the account that has two signers
transaction = (
    TransactionBuilder(
        source_account=root_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
    )
    .append_payment_op(destination=destination, amount="2000", asset=Asset.native())
    .set_timeout(30)
    .build()
)

# now we need to sign the transaction with both the root and the secondary_keypair
transaction.sign(root_keypair)
transaction.sign(secondary_keypair)
response = server.submit_transaction(transaction)
print(response)
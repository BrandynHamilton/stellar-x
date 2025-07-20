"""
This example demonstrates how to use TransactionBuilder
to quickly build a transaction. For a beginner,
most of the work can be done with TransactionBuilder.

See: https://stellar-sdk.readthedocs.io/en/latest/building_transactions.html#building-transactions
"""

import os
from dotenv import load_dotenv
from stellar_sdk import Account, Server, Asset, Keypair, Network, TransactionBuilder

load_dotenv()

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
if not PRIVATE_KEY:
    raise ValueError("PRIVATE_KEY environment variable is not set.")

server = Server(horizon_url="https://horizon-testnet.stellar.org")
source = Keypair.from_secret(PRIVATE_KEY)
# `account` can also be a muxed account
source_account = server.load_account(source.public_key)

print(f"Root account: {source_account.account}")
print(f"Root account sequence number: {source_account.sequence}")

transaction = (
    TransactionBuilder(
        source_account=source_account,
        # If you want to submit to pubnet, you need to change `network_passphrase` to `Network.PUBLIC_NETWORK_PASSPHRASE`
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
    )
    .add_text_memo("Happy birthday!")
    .append_payment_op(  # add a payment operation to the transaction
        destination="GDNTF4ASUK5BPAHTDF45OS5KF2HJ3JQKKACKN6QBZ6IZUZEY7K5B4HHO",
        asset=Asset.native(),
        amount="125.5",
    )
    .append_set_options_op(  # add a set options operation to the transaction
        home_domain="overcat.me"
    )
    .set_timeout(30)
    .build()
)  # mark this transaction as valid only for the next 30 seconds

print(f"Transaction built: {transaction}")
transaction.sign(source)

# Let's see the XDR (encoded in base64) of the transaction we just built
print(transaction.to_xdr())

response = server.submit_transaction(transaction)
print(response)
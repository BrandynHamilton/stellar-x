"""
A path payment sends an amount of a specific asset to a destination account through a path of offers.
Since the asset sent (e.g., 450 XLM) can be different from the asset received (e.g, 6 BTC),
path payments allow for the simultaneous transfer and conversion of currencies.

A Path Payment Strict Send allows a user to specify the amount of the asset to send.
The amount received will vary based on offers in the order books. If you would like to
instead specify the amount received, use the Path Payment Strict Receive operation.

See: https://developers.stellar.org/docs/start/list-of-operations/#path-payment-strict-send
See: https://youtu.be/KzlSgSPStz8
"""

import os
from dotenv import load_dotenv
from stellar_sdk import Account, Server, Asset, Keypair, Network, TransactionBuilder
from stellar_sdk import TransactionEnvelope
import time

load_dotenv()

PRIVATE_KEY = os.getenv("PRIVATE_KEY")
PRIVATE_KEY_2 = os.getenv("PRIVATE_KEY_2")
# RECIPIENT_ACCOUNT = "GCEGI5E4ZLGZICOMV3IIA3DJPTU5XKWIFGXD4SZ5TVKGKRMSWLGYRUSW"

server = Server(horizon_url="https://horizon-testnet.stellar.org")
source_keypair = Keypair.from_secret(
    PRIVATE_KEY
)

source_account = server.load_account(account_id=source_keypair.public_key)

destination_keypair = Keypair.from_secret(PRIVATE_KEY_2)
destination_account = server.load_account(destination_keypair.public_key)

trust_tx = (
    TransactionBuilder(destination_account, Network.TESTNET_NETWORK_PASSPHRASE, base_fee=100)
    .append_change_trust_op(
        asset=Asset("GBP", source_keypair.public_key),
    )
    .set_timeout(30)
    .build()
)
trust_tx.sign(destination_keypair)
server.submit_transaction(trust_tx)

offer_tx = (
    TransactionBuilder(source_account, Network.TESTNET_NETWORK_PASSPHRASE, base_fee=100)
    .append_manage_sell_offer_op(
        selling=Asset("USD", source_keypair.public_key),
        buying=Asset.native(),
        amount="1000",  # how much USD to sell
        price="1.2",    # USD/EUR rate
    )
    .set_timeout(30)
    .build()
)
offer_tx.sign(source_keypair)
server.submit_transaction(offer_tx)

time.sleep(5)

orderbook = server.orderbook(
    selling=Asset("USD", source_keypair.public_key),
    buying=Asset.native()
).call()

print(orderbook["bids"])
print(orderbook["asks"])

offer_tx = (
    TransactionBuilder(source_account, Network.TESTNET_NETWORK_PASSPHRASE, base_fee=100)
    .append_manage_sell_offer_op(
        selling=Asset("GBP", source_keypair.public_key),
        buying=Asset.native(),
        amount="1000",  # how much USD to sell
        price="1.2",    # USD/EUR rate
    )
    .set_timeout(30)
    .build()
)
offer_tx.sign(source_keypair)
server.submit_transaction(offer_tx)

time.sleep(5)

orderbook = server.orderbook(
    selling=Asset("GBP", source_keypair.public_key),
    buying=Asset.native()
).call()

print(orderbook["bids"])
print(orderbook["asks"])

# Add offer: USD → GBP
offer_tx = (
    TransactionBuilder(source_account, Network.TESTNET_NETWORK_PASSPHRASE, base_fee=100)
    .append_manage_sell_offer_op(
        selling=Asset("USD", source_keypair.public_key),
        buying=Asset("GBP", source_keypair.public_key),
        amount="1000",
        price="1.0",  # 1 USD = 1 GBP, adjust if needed
    )
    .set_timeout(30)
    .build()
)
offer_tx.sign(source_keypair)
server.submit_transaction(offer_tx)

orderbook = server.orderbook(
    selling=Asset("USD", source_keypair.public_key),
    buying=Asset("GBP", source_keypair.public_key),
).call()

print(orderbook["bids"])
print(orderbook["asks"])

# Create an offer: SELL XLM → BUY USD
offer_tx = (
    TransactionBuilder(source_account, Network.TESTNET_NETWORK_PASSPHRASE, base_fee=100)
    .append_manage_sell_offer_op(
        selling=Asset.native(),  # sell XLM
        buying=Asset("USD", source_keypair.public_key),  # receive USD
        amount="500",    # you decide
        price="0.83",    # for example, 1 XLM = 0.83 USD
    )
    .set_timeout(30)
    .build()
)
offer_tx.sign(source_keypair)
server.submit_transaction(offer_tx)

path = [
    Asset("USD", source_keypair.public_key),
]
transaction = (
    TransactionBuilder(
        source_account=source_account,
        network_passphrase=Network.TESTNET_NETWORK_PASSPHRASE,
        base_fee=100,
    )
    .append_path_payment_strict_receive_op(
        destination=destination_keypair.public_key,
        send_asset=Asset.native(),
        send_max="1000",
        dest_asset=Asset(
            "GBP", source_keypair.public_key
        ),
        dest_amount="5.50",
        path=path,
    )
    .set_timeout(30)
    .build()
)
transaction.sign(source_keypair)
response = server.submit_transaction(transaction)
xdr = response.get("extras").get("envelope_xdr")
result_codes = response.get("extras").get("result_codes")

print(result_codes)
print(xdr.to_xdr_object().to_xdr())
"""
See: https://stellar-sdk.readthedocs.io/en/latest/querying_horizon.html#streaming-requests
"""

from stellar_sdk import Server

server = Server(horizon_url="https://horizon-testnet.stellar.org")
account_id = "GB6NVEN5HSUBKMYCE5ZOWSK5K23TBWRUQLZY3KNMXUZ3AQ2ESC4MY4AQ"
last_cursor = "now"  # or load where you left off


def tx_handler(tx_response):
    print(tx_response)

for tx in server.transactions().for_account(account_id).cursor(last_cursor).stream():
    tx_handler(tx)
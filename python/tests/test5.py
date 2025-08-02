# Create asset instances using the Stellar SDK

from stellar_sdk import Asset
native = Asset.native()

test_asset = Asset("TEST", "GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB")
is_native = test_asset.is_native()  # False
# Creates Google stock asset issued by GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB
google_stock_asset = Asset('US38259P7069', 'GBBM6BKZPEHWYO3E3YKREDPQXMS4VK35YLNU7NFBRI26RAN7GI5POFBB')
google_stock_asset_type = google_stock_asset.type  # credit_alphanum12

print(f"Native Asset: {native}"
      f"\nTest Asset: {test_asset}\n"
      f"Is Native: {is_native}\n"
      f"Google Stock Asset: {google_stock_asset}\n"
      f"Google Stock Asset Type: {google_stock_asset_type}")
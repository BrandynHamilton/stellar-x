from stellar_sdk import Keypair
import json
import os

KEYSTORE_DIR = "./keystore"

os.makedirs(KEYSTORE_DIR, exist_ok=True)

# Generate Keypair From Mnemonic Phrase and Save to File

mnemonic_phrase = Keypair.generate_mnemonic_phrase()
print(f"Mnemonic phrase: {mnemonic_phrase}")
keypair = Keypair.from_mnemonic_phrase(mnemonic_phrase)
print(f"Public Key: {keypair.public_key}")
print(f"Secret Seed: {keypair.secret}")

output_file = os.path.join(KEYSTORE_DIR, f"{keypair.public_key}_keystore.json")

with open(output_file, "w") as f:
    json.dump({
        "public_key": keypair.public_key,
        "secret": keypair.secret,
        "mnemonic_phrase": mnemonic_phrase
    }, f)
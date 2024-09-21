import os
import random
import string
import json

# Function to generate random hexadecimal data
def random_hex(length=64):
    return ''.join(random.choice(string.hexdigits) for _ in range(length)).lower()

# Function to generate random key-value JSON data
def random_key_value_json(num_items=10):
    return json.dumps({f"key_{i}": random_hex(32) for i in range(num_items)}, indent=4)

# Function to generate random wallet data
def random_wallet_data():
    return {
        "wallet_address": random_hex(34),
        "balance": round(random.uniform(0.1, 10.0), 4),
        "transactions": [
            {"txid": random_hex(64), "amount": round(random.uniform(-1, 1), 4), "timestamp": random.randint(1500000000, 1700000000)}
            for _ in range(5)
        ]
    }

# Function to generate random binary data
def random_binary_data(length=256):
    return os.urandom(length)

# Function to simulate file content based on wallet name
def simulate_file_content(name):
    if name in ["Atomic", "Guarda"]:
        # Simulate LevelDB-like structure (JSON format)
        return random_key_value_json(), "ldb"
    elif name in ["Exodus", "Electrum", "Electrum-LTC", "Coinomi"]:
        # Simulate wallet-like data (JSON format)
        return json.dumps(random_wallet_data(), indent=4), "json"
    elif name == "Zcash" or name == "Armory":
        # Simulate encrypted/binary-like data (Binary format)
        return random_binary_data(), "bin"
    elif name == "Bytecoin":
        # Hexadecimal wallet data (txt format)
        return random_hex(128), "txt"
    elif name == "Jaxx":
        # Simulate LevelDB-like structure (JSON format)
        return random_key_value_json(), "ldb"
    elif name == "Etherium":
        # Simulate Ethereum keystore JSON
        return json.dumps({
            "address": random_hex(40),
            "crypto": {
                "ciphertext": random_hex(128),
                "cipherparams": {"iv": random_hex(32)},
                "kdf": "scrypt",
                "kdfparams": {
                    "dklen": 32,
                    "n": 262144,
                    "r": 8,
                    "p": 1,
                    "salt": random_hex(64)
                },
                "mac": random_hex(64)
            },
            "id": random_hex(36),
            "version": 3
        }, indent=4), "json"

# Define the list of wallet files with their names and paths
files = [
    {"name": "Atomic", "path": os.path.join("APPDATA", "atomic", "Local Storage", "leveldb")},
    {"name": "Exodus", "path": os.path.join("APPDATA", "Exodus", "exodus.wallet")},
    {"name": "Electrum", "path": os.path.join("APPDATA", "Electrum", "wallets")},
    {"name": "Electrum-LTC", "path": os.path.join("APPDATA", "Electrum-LTC", "wallets")},
    {"name": "Zcash", "path": os.path.join("APPDATA", "Zcash")},
    {"name": "Armory", "path": os.path.join("APPDATA", "Armory")},
    {"name": "Bytecoin", "path": os.path.join("APPDATA", "bytecoin")},
    {"name": "Jaxx", "path": os.path.join("APPDATA", "com.liberty.jaxx", "IndexedDB", "file__0.indexeddb.leveldb")},
    {"name": "Etherium", "path": os.path.join("APPDATA", "Ethereum", "keystore")},
    {"name": "Guarda", "path": os.path.join("APPDATA", "Guarda", "Local Storage", "leveldb")},
    {"name": "Coinomi", "path": os.path.join("APPDATA", "Coinomi", "Coinomi", "wallets")}
]

# Base folder to store all simulated data
base_folder = "wallet"

# Create the base folder if it doesn't exist
os.makedirs(base_folder, exist_ok=True)

# Iterate over the files and generate the appropriate content
for file in files:
    content, extension = simulate_file_content(file["name"])
    
    # Create a folder for each wallet name
    folder_path = os.path.join(base_folder, file["name"])
    os.makedirs(folder_path, exist_ok=True)
    
    # Save the content with the appropriate file extension
    file_path = os.path.join(folder_path, f"{file['name']}_test_file.{extension}")
    
    with open(file_path, 'wb' if extension == 'bin' else 'w') as f:
        if extension == "bin":
            f.write(content)  # Write binary data
        else:
            f.write(content)  # Write text data (JSON, txt, etc.)

    print(f"Generated and saved file for {file['name']} at {file_path}")


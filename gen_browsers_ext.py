import os
import random
import string
import json
import sys

# Function to generate random hexadecimal data
def random_hex(length=64):
    return ''.join(random.choice(string.hexdigits) for _ in range(length)).lower()

# Function to generate a random SQL injection
def random_sql_injection():
    injections = [
        "' OR '1'='1'; --",
        "'; DROP TABLE users; --",
        "' UNION SELECT * FROM users; --",
        "' OR '1'='1' /*",
        "'; SELECT username, password FROM users; --"
    ]
    return random.choice(injections)

# Function to generate random JSON data for browser extensions
def random_extension_data():
    data = {
        "extension_id": random_hex(16),
        "settings": {f"setting_{i}": random_hex(8) for i in range(5)},
        "data": {f"data_{i}": random_hex(32) for i in range(10)}
    }

    # 10% chance to insert a SQL injection string
    if random.random() < 0.1:
        data["sql_injection"] = random_sql_injection()

    return json.dumps(data, indent=4)

# List of Chromium browsers
CHROMIUM_BROWSERS = [
    {"name": "Google Chrome", "path": os.path.join("LOCALAPPDATA", "Google", "Chrome", "User Data"), "taskname": "chrome.exe"},
    {"name": "Microsoft Edge", "path": os.path.join("LOCALAPPDATA", "Microsoft", "Edge", "User Data"), "taskname": "msedge.exe"},
    {"name": "Opera", "path": os.path.join("APPDATA", "Opera Software", "Opera Stable"), "taskname": "opera.exe"},
    {"name": "Opera GX", "path": os.path.join("APPDATA", "Opera Software", "Opera GX Stable"), "taskname": "opera.exe"},
    {"name": "Brave", "path": os.path.join("LOCALAPPDATA", "BraveSoftware", "Brave-Browser", "User Data"), "taskname": "brave.exe"},
    {"name": "Yandex", "path": os.path.join("APPDATA", "Yandex", "YandexBrowser", "User Data"), "taskname": "yandex.exe"},
]

# List of subpaths (profiles)
CHROMIUM_SUBPATHS = [
    {"name": "None", "path": ""},
    {"name": "Default", "path": "Default"},
    {"name": "Profile 1", "path": "Profile 1"},
    {"name": "Profile 2", "path": "Profile 2"},
    {"name": "Profile 3", "path": "Profile 3"},
    {"name": "Profile 4", "path": "Profile 4"},
    {"name": "Profile 5", "path": "Profile 5"},
]

# List of browser extensions
BROWSER_EXTENSIONS = [
    {"name": "Authenticator", "path": "\\Local Extension Settings\\bhghoamapcdpbohphigoooaddinpkbai"},
    {"name": "Binance", "path": "\\Local Extension Settings\\fhbohimaelbohpjbbldcngcnapndodjp"},
    {"name": "Bitapp", "path": "\\Local Extension Settings\\fihkakfobkmkjojpchpfgcmhfjnmnfpi"},
    {"name": "BoltX", "path": "\\Local Extension Settings\\aodkkagnadcbobfpggfnjeongemjbjca"},
    {"name": "Coin98", "path": "\\Local Extension Settings\\aeachknmefphepccionboohckonoeemg"},
    {"name": "Coinbase", "path": "\\Local Extension Settings\\hnfanknocfeofbddgcijnmhnfnkdnaad"},
    {"name": "Metamask", "path": "\\Local Extension Settings\\nkbihfbeogaeaoehlefnkodbefgpgknn"},
    # Add other extensions...
]

# Base folder to store all simulated browser data
base_folder = "browser_ext"

# Create the base folder if it doesn't exist
os.makedirs(base_folder, exist_ok=True)

# Check for command line argument for how many times to randomize
if len(sys.argv) != 2:
    print("Usage: python script.py <number_of_randomizations>")
    sys.exit(1)

try:
    num_randomizations = int(sys.argv[1])
except ValueError:
    print("Please provide a valid integer.")
    sys.exit(1)

# Iterate over Chromium browsers
for browser in CHROMIUM_BROWSERS:
    browser_folder = os.path.join(base_folder, browser["name"])
    os.makedirs(browser_folder, exist_ok=True)

    # Iterate over subpaths (profiles)
    for subpath in CHROMIUM_SUBPATHS:
        profile_folder = os.path.join(browser_folder, subpath["name"])
        os.makedirs(profile_folder, exist_ok=True)

        # Generate random extension data for the specified number of times
        for _ in range(num_randomizations):
            for extension in BROWSER_EXTENSIONS:
                # Generate random extension data and save it in the appropriate folder
                extension_data = random_extension_data()
                extension_folder = os.path.join(profile_folder, extension["name"])
                os.makedirs(extension_folder, exist_ok=True)

                # Save the extension data as a .json file
                extension_file_path = os.path.join(extension_folder, f"{extension['name']}_data.json")
                with open(extension_file_path, 'w') as f:
                    f.write(extension_data)

                print(f"Generated and saved file for {extension['name']} in {extension_file_path}")


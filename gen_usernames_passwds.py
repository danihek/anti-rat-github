import os
import random
import string
import json
import sys

# Function to generate random strings
def random_string(length=12):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

# Function to generate random URL
def random_url():
    return f"https://{random_string(8)}.com"

# Function to generate random password
def random_password(length=16):
    return ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(length))

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

# List to store passwords
PASSWORDS = []

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

# Number of random password entries to generate
NUM_PASSWORDS = 1

if len(sys.argv) > 1:
    try:
        NUM_PASSWORDS = int(sys.argv[1])
    except ValueError:
        print("Invalid number provided, defaulting to 1")
        NUM_PASSWORDS = 1

# Generate random password entries
for browser in CHROMIUM_BROWSERS:
    for subpath in CHROMIUM_SUBPATHS:
        for _ in range(NUM_PASSWORDS):
            origin_url = random_url()
            username = random_string(8)
            password = random_password()

            # 10% chance to insert an SQL injection into the username or password
            if random.random() < 0.1:
                username = random_sql_injection()  # 10% chance for SQL injection in username
            if random.random() < 0.1:
                password = random_sql_injection()  # 10% chance for SQL injection in password

            PASSWORDS.append({
                "browser": browser["name"],
                "profile": subpath["name"],
                "url": origin_url,
                "username": username,
                "password": password
            })

# Convert PASSWORDS list to JSON format
password_json_data = json.dumps(PASSWORDS, indent=4)

# Save the password data to a JSON file
output_folder = "passwords"
os.makedirs(output_folder, exist_ok=True)
output_file_path = os.path.join(output_folder, "passwords.json")

with open(output_file_path, 'w') as f:
    f.write(password_json_data)

print(f"Generated and saved {len(PASSWORDS)} password entries in {output_file_path}")


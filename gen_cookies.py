import os
import json
import base64
import random
import string
import sys

# Default number of cookies
COOKIES_COUNT = 1

# Get the number of cookies from command line argument
if len(sys.argv) > 1:
    try:
        COOKIES_COUNT = int(sys.argv[1])
    except ValueError:
        print("Invalid number provided, defaulting to 1 cookie.")
        COOKIES_COUNT = 1

# Function to generate a random Base64-encoded cookie
def generate_random_cookie(length=16):
    random_data = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
    return base64.b64encode(random_data.encode()).decode()

# Function to decode Base64 cookies
def decode_cookie(cookie):
    try:
        return base64.b64decode(cookie).decode()
    except Exception as e:
        print(f"Error decoding cookie: {e}")
        return cookie  # Return original if decode fails

# File paths
cookies_file = '__cookies.txt'
output_folder = 'cookies'
web_data_file = os.path.join(output_folder, 'cookies.json')

# Ensure the cookies file exists or generate random cookies
if not os.path.exists(cookies_file):
    print(f"'{cookies_file}' not found. Generating {COOKIES_COUNT} random cookies.")
    original_cookies = [generate_random_cookie() for _ in range(COOKIES_COUNT)]
else:
    # Read cookies from file
    with open(cookies_file, 'r') as cf:
        original_cookies = [line.strip() for line in cf if line.strip()]

# List to store decoded cookies
WEB_DATA = []

# Decode cookies and store them
for cookie in original_cookies:
    decoded_cookie = decode_cookie(cookie)
    WEB_DATA.append({"cookie": decoded_cookie})

# Create output directory if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Save the web data to a JSON file
with open(web_data_file, 'w') as wdf:
    json.dump(WEB_DATA, wdf, indent=4)

print(f"Decoded cookies saved to {web_data_file}")


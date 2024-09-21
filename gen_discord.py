import os
import random
import string
import sys

# Function to generate random strings
def random_string(length=12):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

# Function to generate random email
def random_email():
    domains = ["example.com", "starmail.net", "mail.com", "gmail.com", "yahoo.com"]
    return f"{random_string(8)}@{random.choice(domains)}"

# Function to generate random phone number
def random_phone():
    return f"+49{random.randint(1000000000, 9999999999)}"

# Function to generate a random token
def random_token():
    return f"mfa.{random_string(16)}_authkey"

# Function to generate a random display name
def random_display_name():
    return random_string(6).capitalize()

# Generate a random entry
def generate_random_entry():
    return f"ID: {random.randint(10000000000000000, 99999999999999999)}\n" \
           f"USERNAME: {random_string(8)}\n" \
           f"DISPLAY NAME: {random_display_name()}\n" \
           f"EMAIL: {random_email()}\n" \
           f"PHONE: {random_phone()}\n" \
           f"TOKEN: {random_token()}\n"

# Check command line arguments for number of entries
try:
    NUM_ENTRIES = int(sys.argv[1]) if len(sys.argv) > 1 else 50
except ValueError:
    print("Invalid number provided, defaulting to 50.")
    NUM_ENTRIES = 50

# Generate a list of random entries
random_entries = [generate_random_entry() for _ in range(NUM_ENTRIES)]

# Save to a plain text file
output_folder = "discord"
os.makedirs(output_folder, exist_ok=True)
output_file_path = os.path.join(output_folder, "discord-tokens.txt")

with open(output_file_path, 'w') as f:
    f.write("\n".join(random_entries))

print(f"Generated and saved {NUM_ENTRIES} random entries in {output_file_path}")


import os
import random
import string
import sys
from datetime import datetime, timedelta

# Allowed extensions
ALLOWED_EXTENSIONS = [
    ".txt", ".log", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx",
    ".odt", ".pdf", ".rtf", ".json", ".csv", ".db", ".jpg", ".jpeg",
    ".png", ".gif", ".webp", ".mp4"
]

# Folder for generated files
OUTPUT_FOLDER = "sus_files"
CURSED_WORDS_FILE = os.path.join(OUTPUT_FOLDER, "cursed_words.txt")

# Expanded dictionary of words
WORDS = [
    "sensitive", "confidential", "breach", "malware", "attack",
    "phishing", "credentials", "login", "database", "unauthorized",
    "exfiltration", "spyware", "scam", "hack", "data_leak",
    "ransomware", "trojan", "vulnerability", "exploit", "threat",
    "encryption", "firewall", "security", "audit", "penetration_test",
    "malicious", "payload", "risk_assessment", "intrusion", "monitoring",
    "incident_response", "anomaly", "tracing", "suspicious_activity",
    "expose", "access_granted", "snoop", "rootkit", "cipher",
    "breach_report", "leak_report", "data_mining", "analytics"
]

# Generate random date within a given range
def generate_random_date(start_year=2000, end_year=2023):
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_date

# Generate random file name
def generate_random_filename():
    base_names = [
        "attack", "report", "divorce", "passwords", "saved_data", "invoice",
        "log", "credentials", "config", "sensitive_info", "backup",
        "financial_report", "user_data", "threat_analysis", "breach_notice",
        "phishing_attempt", "malware_report", "transaction_log", "suspicious_activity"
    ]
    
    random_base = random.choice(base_names)
    random_date = generate_random_date()
    date_str = random_date.strftime("%Y-%m")  # Format: YYYY-MM

    if random_base in ["attack", "report"]:
        return f"{random_base}[{date_str}]{random.choice(ALLOWED_EXTENSIONS)}"
    else:
        return f"{random_base}{random.choice(ALLOWED_EXTENSIONS)}"

# Generate random suspicious content
def generate_random_content():
    # Create a random paragraph with multiple words
    content_length = random.randint(5, 15)  # Number of words per line
    lines = []
    for _ in range(random.randint(3, 6)):  # Number of lines
        line = " ".join(random.choice(WORDS) for _ in range(content_length))
        lines.append(line)
    return "\n".join(lines)

# Generate and write suspicious files
def generate_and_write_files(num_files):
    for _ in range(num_files):
        filename = generate_random_filename()
        content = generate_random_content()
        
        # Create the file and write content in the output folder
        with open(os.path.join(OUTPUT_FOLDER, filename), "w") as f:
            f.write(content)
        print(f"Generated: {filename}")

# Write to cursed_words.txt
def write_to_cursed_words(filenames):
    with open(CURSED_WORDS_FILE, "w") as f:
        for filename in filenames:
            f.write(f"{filename}\n")
    print(f"Generated '{CURSED_WORDS_FILE}' with {len(filenames)} filenames.")

# Main function
if __name__ == "__main__":
    # Create output folder if it doesn't exist
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Check for command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python generate_suspicious_files.py <number_of_files>")
        sys.exit(1)
    
    try:
        NUM_FILES = int(sys.argv[1])
        if NUM_FILES <= 0:
            raise ValueError("Number of files must be positive.")
    except ValueError as e:
        print(f"Invalid input: {e}")
        sys.exit(1)

    suspicious_filenames = [generate_random_filename() for _ in range(NUM_FILES)]
    write_to_cursed_words(suspicious_filenames)
    
    # Generate and write suspicious content to files
    generate_and_write_files(NUM_FILES)


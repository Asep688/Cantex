import os
from dotenv import load_dotenv

load_dotenv()

ACCOUNTS = []

for key, value in os.environ.items():
    if key.startswith("KEY_") and value:
        ACCOUNTS.append({
            "name": key,
            "key": value
        })

print("✅ Accounts loaded:", len(ACCOUNTS))

import os
import time
import random
import requests
from dotenv import load_dotenv
import config
import accounts

load_dotenv()

BASE_URL = "https://api.cantex.io"  # sesuaikan kalau beda

running = False

def get_random_amount():
    return round(random.uniform(config.MIN_AMOUNT, config.MAX_AMOUNT), 2)

def get_quote(from_token, to_token, amount):
    url = f"{BASE_URL}/quote"
    payload = {
        "from": from_token,
        "to": to_token,
        "amount": amount
    }
    r = requests.post(url, json=payload)
    return r.json()

def execute_swap(account, from_token, to_token, amount):
    url = f"{BASE_URL}/swap"

    headers = {
        "Authorization": f"Bearer {account['key']}"
    }

    payload = {
        "from": from_token,
        "to": to_token,
        "amount": amount
    }

    r = requests.post(url, json=payload, headers=headers)
    return r.json()

def run_account(account, log):
    while running:
        try:
            amount = get_random_amount()

            quote = get_quote(config.FROM_TOKEN, config.TO_TOKEN, amount)

            fee = quote.get("fee", 0)
            price = quote.get("price", 0)

            log(f"[{account['name']}] Amount: {amount}")
            log(f"[{account['name']}] Price: {price}")
            log(f"[{account['name']}] Fee: {fee}")

            if fee <= config.MAX_FEE:
                log(f"[{account['name']}] ✅ SWAP")

                tx = execute_swap(
                    account,
                    config.FROM_TOKEN,
                    config.TO_TOKEN,
                    amount
                )

                log(f"[{account['name']}] TX: {tx}")

                time.sleep(config.COOLDOWN_AFTER_SWAP)
            else:
                log(f"[{account['name']}] ❌ Fee tinggi")

        except Exception as e:
            log(f"[{account['name']}] ERROR: {e}")

        time.sleep(config.DELAY)

def start_bot(log):
    global running
    running = True

    from threading import Thread

    for acc in accounts.ACCOUNTS:
        Thread(target=run_account, args=(acc, log)).start()

def stop_bot():
    global running
    running = False

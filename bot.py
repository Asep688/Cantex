import time
import random
from threading import Thread
from cantex_sdk import Client
import config
import accounts

running = False

def get_random_amount():
    return round(random.uniform(config.MIN_AMOUNT, config.MAX_AMOUNT), 2)

def run_account(account, log_callback):
    client = Client(intent_key=account["key"])

    while running:
        try:
            amount = get_random_amount()

            quote = client.get_swap_quote(
                from_token=config.FROM_TOKEN,
                to_token=config.TO_TOKEN,
                amount=amount
            )

            fee = quote.get("fee", 0)
            price = quote.get("price", 0)

            log_callback(f"[{account['name']}] Amount: {amount}")
            log_callback(f"[{account['name']}] Price: {price}")
            log_callback(f"[{account['name']}] Fee: {fee}")

            if fee <= config.MAX_FEE:
                log_callback(f"[{account['name']}] ✅ SWAP")

                tx = client.execute_swap(
                    from_token=config.FROM_TOKEN,
                    to_token=config.TO_TOKEN,
                    amount=amount,
                    slippage=config.SLIPPAGE
                )

                log_callback(f"[{account['name']}] TX: {tx}")

                time.sleep(config.COOLDOWN_AFTER_SWAP)
            else:
                log_callback(f"[{account['name']}] ❌ Fee tinggi")

        except Exception as e:
            log_callback(f"[{account['name']}] ERROR: {e}")

        time.sleep(config.DELAY)

def start_bot(log_callback):
    global running
    running = True

    for acc in accounts.ACCOUNTS:
        Thread(target=run_account, args=(acc, log_callback)).start()

def stop_bot():
    global running
    running = False

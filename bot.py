import os
import time
import random
from dotenv import load_dotenv
from cantex_sdk import Client
import config

load_dotenv()

client = Client(
    intent_key=os.getenv("TRADING_KEY")
)

running = False

def get_random_amount():
    return round(random.uniform(config.MIN_AMOUNT, config.MAX_AMOUNT), 2)

def run_bot(log_callback):
    global running
    running = True

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

            log_callback(f"Amount: {amount}")
            log_callback(f"Price: {price}")
            log_callback(f"Fee: {fee}")

            if fee <= config.MAX_FEE:
                log_callback("✅ Swap dieksekusi")

                tx = client.execute_swap(
                    from_token=config.FROM_TOKEN,
                    to_token=config.TO_TOKEN,
                    amount=amount,
                    slippage=config.SLIPPAGE
                )

                log_callback(f"TX: {tx}")
                time.sleep(10)
            else:
                log_callback("❌ Fee terlalu tinggi")

        except Exception as e:
            log_callback(f"ERROR: {e}")

        time.sleep(config.DELAY)

def stop_bot():
    global running
    running = False

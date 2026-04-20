import time
import random
import requests
import config
import accounts

print("🚀 BOT STARTED")

running = True

def get_random_amount():
    return round(random.uniform(config.MIN_AMOUNT, config.MAX_AMOUNT), 2)

def get_quote(amount):
    # ⚠️ endpoint dummy (nanti bisa kita ganti real)
    return {
        "price": round(random.uniform(0.1, 0.2), 4),
        "fee": round(random.uniform(0.05, 0.2), 4)
    }

def execute_swap(account, amount):
    # dummy swap (simulasi)
    return {"status": "success", "amount": amount}

if not accounts.ACCOUNTS:
    print("❌ TIDAK ADA AKUN TERDETEKSI!")
    exit()

while running:
    print("="*40)

    for acc in accounts.ACCOUNTS:
        try:
            amount = get_random_amount()

            quote = get_quote(amount)

            price = quote["price"]
            fee = quote["fee"]

            print(f"[{acc['name']}] Amount: {amount}")
            print(f"[{acc['name']}] Price: {price}")
            print(f"[{acc['name']}] Fee: {fee}")

            if fee <= config.MAX_FEE:
                print(f"[{acc['name']}] ✅ SWAP EXECUTED")

                tx = execute_swap(acc, amount)

                print(f"[{acc['name']}] TX:", tx)

                time.sleep(config.COOLDOWN_AFTER_SWAP)
            else:
                print(f"[{acc['name']}] ❌ Fee terlalu tinggi")

        except Exception as e:
            print(f"[{acc['name']}] ERROR:", e)

    time.sleep(config.DELAY)

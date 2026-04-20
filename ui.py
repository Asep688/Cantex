import tkinter as tk
from threading import Thread
import bot
import config
import accounts

def start():
    Thread(target=bot.start_bot, args=(log,)).start()
    log("🚀 Bot started")

def stop():
    bot.stop_bot()
    log("🛑 Bot stopped")

def log(message):
    text.insert(tk.END, message + "\n")
    text.see(tk.END)

def update_config():
    config.MAX_FEE = float(entry_fee.get())
    config.MIN_AMOUNT = float(entry_min.get())
    config.MAX_AMOUNT = float(entry_max.get())
    log("⚙️ Config updated")

root = tk.Tk()
root.title("Cantex Multi Account Bot")

# INFO AKUN
tk.Label(root, text=f"Akun terdeteksi: {len(accounts.ACCOUNTS)}").pack()

# CONFIG
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Max Fee").grid(row=0, column=0)
entry_fee = tk.Entry(frame)
entry_fee.insert(0, str(config.MAX_FEE))
entry_fee.grid(row=0, column=1)

tk.Label(frame, text="Min Amount").grid(row=1, column=0)
entry_min = tk.Entry(frame)
entry_min.insert(0, str(config.MIN_AMOUNT))
entry_min.grid(row=1, column=1)

tk.Label(frame, text="Max Amount").grid(row=2, column=0)
entry_max = tk.Entry(frame)
entry_max.insert(0, str(config.MAX_AMOUNT))
entry_max.grid(row=2, column=1)

tk.Button(frame, text="Update Config", command=update_config).grid(row=3, columnspan=2)

# BUTTON
tk.Button(root, text="▶ Start", command=start, bg="green").pack(pady=5)
tk.Button(root, text="■ Stop", command=stop, bg="red").pack(pady=5)

# LOG
text = tk.Text(root, height=20, width=70)
text.pack()

root.mainloop()

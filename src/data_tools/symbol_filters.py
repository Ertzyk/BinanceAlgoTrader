import os
from config import client

PAIR = os.getenv("TRADE_PAIR", "BTCUSDC")

try:
    exchange_info = client.get_symbol_info(PAIR)
    for f in exchange_info["filters"]:
        print(f"Filter Type: {f['filterType']}")
        print(f"Filter Data: {f}")
        print("---------------")
except Exception as e:
    print(f"An error occurred: {e}")
import os
from config import client
PAIR = os.getenv("TRADE_PAIR", "BTCUSDC")
PLN_AMOUNT = 38
order = client.order_market_buy(symbol = PAIR, quoteOrderQty = PLN_AMOUNT)
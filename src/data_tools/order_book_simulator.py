import os
from config import client
PAIR = os.getenv("TRADE_PAIR", "BTCUSDC")
PLN_AMOUNT = 100
try:
    order_book = client.get_order_book(symbol=PAIR)
    best_bid = float(order_book['bids'][0][0])
    best_ask = float(order_book['asks'][0][0])
    print(f"Order Book for {PAIR}:")
    print(f"Best Bid (Buy Price): {best_bid} PLN")
    print(f"Best Ask (Sell Price): {best_ask} PLN")
    print(f"\nSimulating market buy of {PLN_AMOUNT} USDT worth of BTC...")
    buy_quantity = PLN_AMOUNT/best_ask
    print(f"You would receive approximately {buy_quantity} BTC.")
    print(f"\nSimulating market sell of {buy_quantity} BTC...")
    sell_price = buy_quantity*best_bid
    print(f"You would receive approximately {sell_price} USDT.")
    loss = PLN_AMOUNT - sell_price
    print(f"\nEstimated loss due to spread: {loss} USDT")
except Exception as e:
    print(f"An error occurred: {e}")
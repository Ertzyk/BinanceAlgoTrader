import os, time, numpy as np
from config import client
from binance.client import Client

PAIR = os.getenv("TRADE_PAIR", "BTCUSDC")
QUOTE_ASSET = os.getenv("QUOTE_ASSET") or PAIR[len(PAIR)//2:]
SHORT_MA, LONG_MA = 20, 40
INTERVAL = Client.KLINE_INTERVAL_1MINUTE
holding_btc = False

def get_min_trade_amount():
    try:
        for f in client.get_symbol_info(PAIR)["filters"]:
            if f["filterType"] == "LOT_SIZE":
                return float(f["minQty"]), float(f["stepSize"])
    except Exception as e:
        print(f"Error fetching trading rules: {e}")
    return None, None

def fetch_prices():
    try:
        klines = client.get_klines(symbol = PAIR, interval = INTERVAL, limit = LONG_MA)
        return [float(kline[4]) for kline in klines]
    except Exception as e:
        print(f"Error fetching prices: {e}")
        return None

def calculate_moving_averages(prices):
    if len(prices) < LONG_MA:
        return None, None
    return (np.mean(prices[-SHORT_MA:]),
            np.mean(prices[-LONG_MA:]))

def place_order(side):
    global holding_btc
    min_qty, step = get_min_trade_amount()
    if min_qty is None: return None

    try:
        if side == "BUY" and not holding_btc:
            quote_bal = float(client.get_asset_balance(asset=QUOTE_ASSET)["free"])
            if quote_bal >= 10:                              # Binance min order
                print(f"BUY {quote_bal:.2f} {QUOTE_ASSET} → BTC …")
                order = client.order_market_buy(symbol=PAIR, quoteOrderQty=quote_bal)
                btc_amt = float(order["executedQty"])
                px = float(order["fills"][0]["price"])
                print(f"✅ Bought {btc_amt:.8f} BTC @ {px:.2f} {QUOTE_ASSET}.")
                holding_btc = True
                return px
            else:
                print("❌ Not enough balance to buy.")

        elif side == "SELL" and holding_btc:
            btc_bal = float(client.get_asset_balance(asset="BTC")["free"])
            if btc_bal >= min_qty:
                btc_bal = round(round(btc_bal / step) * step, 8)
                print(f"🔴 SELL {btc_bal:.8f} BTC …")
                order = client.order_market_sell(symbol=PAIR, quantity=btc_bal)
                proceeds = float(order["fills"][0]["price"]) * btc_bal
                print(f"✅ Sold for {proceeds:.2f} {QUOTE_ASSET}.")
                holding_btc = False
                return proceeds
            else:
                print(f"❌ Need ≥ {min_qty} BTC to sell.")
    except Exception as e:
        print(f"Order error: {e}")
    return None

def trade():
    print("Trading bot started on", PAIR)
    global holding_btc
    while True:
        prices = fetch_prices()
        if prices:
            sma, lma = calculate_moving_averages(prices)
            if sma and lma:
                print(f"SMA {sma:.2f} | LMA {lma:.2f} | Δ {sma-lma:.2f}")
                if sma > lma and not holding_btc:
                    place_order("BUY")
                elif sma < lma and holding_btc:
                    place_order("SELL")
        time.sleep(60)

if __name__ == "__main__":
    trade()
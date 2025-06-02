import os
from config import client

PAIR = os.getenv("TRADE_PAIR", "BTCUSDC")
PLN_AMOUNT = 30

try:
    account_info = client.get_account()
    balances = {asset['asset']: float(asset['free']) for asset in account_info['balances']}

    if 'PLN' not in balances or balances['PLN'] < PLN_AMOUNT:
        raise Exception("Insufficient PLN balance. Deposit PLN before running this test.")

    print(f"Placing market order to buy BTC with {PLN_AMOUNT} PLN...")
    order = client.order_market_buy(symbol = PAIR, quoteOrderQty = PLN_AMOUNT)

    executed_qty = float(order['fills'][0]['qty'])
    cummulative_quote_qty = float(order['cummulativeQuoteQty'])

    print(f"Order filled: Bought {executed_qty:.8f} BTC for {cummulative_quote_qty:.2f} PLN.")
    print(f"Effective BTC price: {cummulative_quote_qty / executed_qty:.2f} PLN per BTC.")

except Exception as e:
    print(f"Error: {e}")
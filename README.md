# BinanceAlgoTrader

Lightweight Binance trading & back-testing tools,  (default: **BTCUSDC**). All code lives in `src/` and runs with a single shared
`.env` file for credentials.

---

## ✨ What’s inside?
| Path                                     | Purpose                                                                                                                                         |
| ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `src/config.py`                          | Loads your `.env` keys once and exposes a ready-to-use `client` object for every script.                                                        |
| `src/data_tools/symbol_filters.py`       | Prints the full list of Binance filters (LOT\_SIZE, PRICE\_FILTER, etc.) for `TRADE_PAIR`.                                                      |
| `src/data_tools/order_book_simulator.py` | Fetches best bid/ask, simulates buying + selling a sample amount, and prints the estimated spread loss.                                         |
| `src/bots/moving_average_backtest.py`    | Loops through recent candles, calculates 10 / 30 simple moving averages, and logs crossovers for quick back-testing.                            |
| `src/bots/moving_average_trader.py`      | Live 20 / 40 SMA strategy: monitors the market each minute and places market BUY/SELL orders when crossovers occur (can be toggled to dry-run). |
| `src/bots/simple_market_buy.py`          | One-off market-buy script: buys `PLN_AMOUNT` worth of BTC (or whatever `TRADE_PAIR` points to).                                                 |
| `src/bots/market_buy_pln_test.py`        | Safety check: confirms PLN balance, places a small BTC buy in PLN, and prints effective price.                                                  |

---

## 🗂️ Repo layout
```text
crypto-algo-bot/
│
├── .env.example          # copy to .env and add your keys
├── requirements.txt
├── README.md
├── .gitignore
├── LICENSE
└── src/
    ├── config.py
    ├── data_tools/
    └── bots/

---

## 🚀 Quick start

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env             # add your BINANCE_API_* keys
export TRADE_PAIR=BTCUSDC        # or BTCEUR / BTCPLN etc.

python src/data_tools/symbol_filters.py
from dotenv import load_dotenv
import os
from binance.client import Client

load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

if not (API_KEY and API_SECRET):
    raise RuntimeError("Set BINANCE_API_KEY & BINANCE_API_SECRET in a .env file or your shell")

client = Client(API_KEY, API_SECRET)
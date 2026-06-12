"""Configuration loader from environment variables."""
import os
from dotenv import load_dotenv

load_dotenv()

DATA_DIR = os.getenv('DATA_DIR', './data')
SQLITE_DB = os.getenv('SQLITE_DB', './data/trading_bot.db')

ETORO_API_KEY = os.getenv('ETORO_API_KEY', '')
ETORO_USER_KEY = os.getenv('ETORO_USER_KEY', '')

KRAKEN_API_KEY = os.getenv('KRAKEN_API_KEY', '')
KRAKEN_SECRET_KEY = os.getenv('KRAKEN_SECRET_KEY', '')

COINBASE_API_KEY = os.getenv('COINBASE_API_KEY', '')
COINBASE_SECRET_KEY = os.getenv('COINBASE_SECRET_KEY', '')
COINBASE_PASSPHRASE = os.getenv('COINBASE_PASSPHRASE', '')

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

PAPER_TRADING = os.getenv('PAPER_TRADING', 'true').lower() == 'true'
INITIAL_CAPITAL_USD = float(os.getenv('INITIAL_CAPITAL_USD', '10000'))
DEFAULT_TICKERS = os.getenv('DEFAULT_TICKERS', 'BTC/USD,ETH/USD,SOL/USD').split(',')
HISTORY_DAYS = int(os.getenv('HISTORY_DAYS', '365'))

os.makedirs(DATA_DIR, exist_ok=True)

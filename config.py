# ===================================================
# MRCKODE TRADING PLATFORM - CONFIGURATION
# ===================================================

# ===== API CREDENTIALS =====
# Keep your keys from your existing config
import os
from dotenv import load_dotenv

# Load environment variables (secret keys)
load_dotenv()

# API Credentials (loaded from .env file locally, or Streamlit secrets online)
API_KEY = os.getenv("BYBIT_API_KEY", "")
API_SECRET = os.getenv("BYBIT_API_SECRET", "")

# Fallback for Streamlit Cloud
try:
    import streamlit as st
    if not API_KEY:
        API_KEY = st.secrets.get("BYBIT_API_KEY", "")
    if not API_SECRET:
        API_SECRET = st.secrets.get("BYBIT_API_SECRET", "")
except:
    pass

# ===== TRADING PAIRS AVAILABLE =====
AVAILABLE_SYMBOLS = [
    'BTC/USDT',
    'ETH/USDT',
    'SOL/USDT',
    'BNB/USDT',
    'XRP/USDT',
    'DOGE/USDT',
]

AVAILABLE_TIMEFRAMES = ['1m', '5m', '15m', '30m', '1h', '4h', '1d']

# ===== DEFAULT SETTINGS (Can be changed in UI) =====
DEFAULT_SYMBOL = 'BTC/USDT'
DEFAULT_TIMEFRAME = '15m'
CANDLE_LIMIT = 100
CHECK_INTERVAL = 30  # seconds

# ===== DEFAULT STRATEGY RULES =====
STARTING_BALANCE = 100.00       # $100 paper money
DEFAULT_POSITION_SIZE = 0.20    # 20% per trade
DEFAULT_TAKE_PROFIT = 0.02      # +2% profit target
DEFAULT_STOP_LOSS = 0.01        # -1% loss limit
DEFAULT_RSI_OVERBOUGHT = 70
DEFAULT_RSI_OVERSOLD = 30
RSI_PERIOD = 14
MA_SHORT = 20
MA_LONG = 50

# ===== FILES =====
TRADES_FILE = 'trades.csv'
STATE_FILE = 'bot_state.json'
SETTINGS_FILE = 'user_settings.json'

# ===== APP INFO =====
APP_NAME = "MrCKode Trading Platform"
APP_VERSION = "2.0"
APP_TAGLINE = "Professional Algorithmic Trading System"
import ccxt
import pandas as pd
import json
import os
import csv
from datetime import datetime
from config import *


class TradingBot:
    def __init__(self):
        # Public exchange for market data (uses testnet for global access)
        self.public_exchange = ccxt.bybit({
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot',
            }
        })
        self.public_exchange.set_sandbox_mode(True)  # Use testnet
        
        # Private exchange for account operations (uses your keys)
        self.private_exchange = ccxt.bybit({
            'apiKey': API_KEY,
            'secret': API_SECRET,
            'enableRateLimit': True,
            'options': {
                'defaultType': 'spot',
            }
        })
        self.private_exchange.set_sandbox_mode(True)  # Use testnet
        
        self.settings = self.load_settings()
        self.state = self.load_state()
    
    # ============================================
    # SETTINGS MANAGEMENT (User can change from UI)
    # ============================================
    def load_settings(self):
        """Load user settings from file"""
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        return {
            'symbol': DEFAULT_SYMBOL,
            'timeframe': DEFAULT_TIMEFRAME,
            'position_size': DEFAULT_POSITION_SIZE,
            'take_profit': DEFAULT_TAKE_PROFIT,
            'stop_loss': DEFAULT_STOP_LOSS,
            'rsi_overbought': DEFAULT_RSI_OVERBOUGHT,
        }
    
    def save_settings(self):
        """Save user settings to file"""
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(self.settings, f, indent=2)
    
    def update_setting(self, key, value):
        """Update a single setting"""
        self.settings[key] = value
        self.save_settings()
    
    # ============================================
    # STATE MANAGEMENT (Bot memory)
    # ============================================
    def load_state(self):
        """Load bot state from file"""
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        return self.get_default_state()
    
    def get_default_state(self):
        """Default state when reset"""
        return {
            'usdt_balance': STARTING_BALANCE,
            'btc_holding': 0,
            'in_position': False,
            'entry_price': 0,
            'position_size_usdt': 0,
            'total_trades': 0,
            'wins': 0,
            'losses': 0,
            'total_profit': 0,
            'bot_running': False,
            'last_action': 'Bot initialized',
            'last_update': datetime.now().isoformat()
        }
    
    def save_state(self):
        """Save bot state to file"""
        self.state['last_update'] = datetime.now().isoformat()
        with open(STATE_FILE, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def reset_bot(self):
        """Reset bot to starting state"""
        self.state = self.get_default_state()
        self.save_state()
    
    # ============================================
    # TECHNICAL INDICATORS
    # ============================================
    def calculate_rsi(self, prices, period=14):
        """Calculate RSI (Relative Strength Index)"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    # ============================================
    # MARKET DATA (Public - no API key needed)
    # ============================================
    def get_market_data(self):
        """Fetch candles and calculate indicators"""
        try:
            candles = self.public_exchange.fetch_ohlcv(
                self.settings['symbol'],
                self.settings['timeframe'],
                limit=CANDLE_LIMIT
            )
            df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df['ma_20'] = df['close'].rolling(window=MA_SHORT).mean()
            df['ma_50'] = df['close'].rolling(window=MA_LONG).mean()
            df['rsi'] = self.calculate_rsi(df['close'], RSI_PERIOD)
            return df
        except Exception as e:
            print(f"Market data error: {e}")
            return None
    
    def get_current_price(self):
        """Get live price"""
        try:
            ticker = self.public_exchange.fetch_ticker(self.settings['symbol'])
            return ticker['last']
        except Exception as e:
            print(f"Price fetch error: {e}")
            return None
    
    # ============================================
    # SIGNAL DETECTION
    # ============================================
    def check_signals(self, df):
        """Check for buy/sell signals"""
        if df is None or len(df) < MA_LONG:
            return None
        
        current_price = df['close'].iloc[-1]
        current_ma20 = df['ma_20'].iloc[-1]
        current_ma50 = df['ma_50'].iloc[-1]
        current_rsi = df['rsi'].iloc[-1]
        
        # Trend analysis
        trend_up = current_ma20 > current_ma50
        rsi_ok = current_rsi < self.settings['rsi_overbought']
        
        # Buy signal
        should_buy = trend_up and rsi_ok and not self.state['in_position']
        
        # Sell signal
        should_sell = False
        sell_reason = ""
        if self.state['in_position']:
            entry = self.state['entry_price']
            profit_pct = (current_price - entry) / entry
            
            if profit_pct >= self.settings['take_profit']:
                should_sell = True
                sell_reason = "TAKE PROFIT"
            elif profit_pct <= -self.settings['stop_loss']:
                should_sell = True
                sell_reason = "STOP LOSS"
        
        return {
            'price': current_price,
            'ma_20': current_ma20,
            'ma_50': current_ma50,
            'rsi': current_rsi,
            'trend_up': trend_up,
            'rsi_ok': rsi_ok,
            'should_buy': should_buy,
            'should_sell': should_sell,
            'sell_reason': sell_reason
        }
    
    # ============================================
    # TRADE EXECUTION (Paper Trading)
    # ============================================
    def execute_buy(self, price):
        """Simulate a buy order"""
        trade_amount = self.state['usdt_balance'] * self.settings['position_size']
        
        # Minimum trade check
        if trade_amount < 1:
            return False
        
        btc_amount = trade_amount / price
        
        self.state['btc_holding'] = btc_amount
        self.state['entry_price'] = price
        self.state['position_size_usdt'] = trade_amount
        self.state['usdt_balance'] -= trade_amount
        self.state['in_position'] = True
        self.state['total_trades'] += 1
        self.state['last_action'] = f"BUY @ ${price:,.2f}"
        
        self.log_trade('BUY', price, trade_amount, 0, 'Trend Up + RSI OK')
        self.save_state()
        return True
    
    def execute_sell(self, price, reason):
        """Simulate a sell order"""
        sell_value = self.state['btc_holding'] * price
        pnl = sell_value - self.state['position_size_usdt']
        
        self.state['usdt_balance'] += sell_value
        self.state['total_profit'] += pnl
        
        if pnl > 0:
            self.state['wins'] += 1
        else:
            self.state['losses'] += 1
        
        self.state['last_action'] = f"SELL @ ${price:,.2f} ({reason})"
        self.log_trade('SELL', price, sell_value, pnl, reason)
        
        # Reset position
        self.state['btc_holding'] = 0
        self.state['entry_price'] = 0
        self.state['position_size_usdt'] = 0
        self.state['in_position'] = False
        self.save_state()
        return True
    
    # ============================================
    # TRADE LOGGING
    # ============================================
    def log_trade(self, action, price, amount, pnl, reason):
        """Log every trade to CSV"""
        file_exists = os.path.isfile(TRADES_FILE)
        with open(TRADES_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(['Timestamp', 'Symbol', 'Action', 'Price', 'Amount_USDT', 'PnL', 'Balance', 'Reason'])
            writer.writerow([
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                self.settings['symbol'],
                action,
                f"{price:.2f}",
                f"{amount:.2f}",
                f"{pnl:.2f}",
                f"{self.state['usdt_balance']:.2f}",
                reason
            ])
    
    def get_trades_history(self):
        """Load trade history"""
        if os.path.exists(TRADES_FILE):
            try:
                return pd.read_csv(TRADES_FILE)
            except:
                return pd.DataFrame()
        return pd.DataFrame()
    
    # ============================================
    # MAIN TRADING CYCLE
    # ============================================
    def run_cycle(self):
        """One trading cycle"""
        if not self.state['bot_running']:
            return None, None
        
        df = self.get_market_data()
        if df is None:
            return None, None
        
        signals = self.check_signals(df)
        if signals is None:
            return df, None
        
        if signals['should_buy']:
            self.execute_buy(signals['price'])
        elif signals['should_sell']:
            self.execute_sell(signals['price'], signals['sell_reason'])
        
        return df, signals
    
    # ============================================
    # STATISTICS
    # ============================================
    def get_stats(self):
        """Calculate performance stats"""
        total_trades = self.state['total_trades']
        wins = self.state['wins']
        losses = self.state['losses']
        
        win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
        completed_trades = wins + losses
        
        return {
            'total_trades': total_trades,
            'completed_trades': completed_trades,
            'wins': wins,
            'losses': losses,
            'win_rate': win_rate,
            'total_profit': self.state['total_profit']
        }

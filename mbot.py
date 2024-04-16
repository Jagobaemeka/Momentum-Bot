#Momentum based trading bot
#Asset to be traded is btc/usdt
#Testnet server
#Atr and moving average 
#Emeka Adimora Date 16/04/2024


import pandas as pd
import numpy as np
import time
import datetime 
import sys
from binance.client import Client

#api keys 
api_key = 'VnRtCRT8xgyr18PoaN88ExGBfwZLwGuRDnoyEbvbdi9x4iI3fTP6MPJq1fDEaumg'
api_secret = 'wVUUQk3GHKNSchvwlbneKcex5vAt8L7TsSZLmCwDv8ljFW58UdXAPjb9Dd9zFs0X'

# Instantiate the Client
cli = Client(api_key, api_secret, testnet=True)

# Adjust time difference in client if necessary
# Note: This step might not be needed if the python-binance library handles it internally

asset = "BTCUSDT"
atr_entry = 30 # Example value for entry
atr_exit = 70 # Example value for exit

# Use `cli` for all API calls
balance = cli.get_asset_balance(asset="BTC")

def calculate_TR(klines):
    # Convert klines to DataFrame for easier manipulation
    df = pd.DataFrame(klines, columns=['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore'])
    df[['open', 'high', 'low', 'close', 'volume']] = df[['open', 'high', 'low', 'close', 'volume']].astype(float)
    
    # Calculate True Range (TR)
    df['previous_close'] = df['close'].shift(1)
    df['high_low'] = df['high'] - df['low']
    df['high_close'] = np.abs(df['high'] - df['previous_close'])
    df['low_close'] = np.abs(df['low'] - df['previous_close'])
    df['TR'] = df[['high_low', 'high_close', 'low_close']].max(axis=1)
    
    return df[['open_time', 'TR']]

# Fetch 1 minute klines for the last day up until now
klines = cli.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "1 day ago UTC")

# Calculate TR for each kline
tr_data = calculate_TR(klines)

print(tr_data)

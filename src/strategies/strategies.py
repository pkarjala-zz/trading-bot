"""Trading strategies for backtesting and paper trading."""
import pandas as pd
import numpy as np

def sma_strategy(df, short=20, long=50):
    """Simple Moving Average crossover strategy."""
    df = df.copy()
    df['sma_short'] = df['close'].rolling(short).mean()
    df['sma_long'] = df['close'].rolling(long).mean()
    df['signal'] = 0
    df.loc[df['sma_short'] > df['sma_long'], 'signal'] = 1  # buy
    df.loc[df['sma_short'] < df['sma_long'], 'signal'] = -1  # sell
    return df

def rsi_strategy(df, period=14, oversold=30, overbought=70):
    """RSI mean reversion strategy."""
    df = df.copy()
    delta = df['close'].diff()
    gain = delta.where(delta > 0, 0).rolling(period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(period).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    df['signal'] = 0
    df.loc[df['rsi'] < oversold, 'signal'] = 1   # buy oversold
    df.loc[df['rsi'] > overbought, 'signal'] = -1  # sell overbought
    return df

def momentum_strategy(df, lookback=14):
    """Momentum strategy: buy when price rises, sell when falls."""
    df = df.copy()
    df['momentum'] = df['close'].pct_change(lookback)
    df['signal'] = 0
    df.loc[df['momentum'] > 0.02, 'signal'] = 1
    df.loc[df['momentum'] < -0.02, 'signal'] = -1
    return df

def dca_strategy(df, interval_days=30, amount_usd=100):
    """Dollar-cost averaging: periodic fixed-amount buys."""
    df = df.copy()
    df['signal'] = 0
    # Simple: buy every interval_days days
    df['day_num'] = (df['timestamp'] - df['timestamp'].iloc[0]).dt.days
    df.loc[df['day_num'] % interval_days == 0, 'signal'] = 1
    return df

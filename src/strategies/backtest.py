"""Backtest engine."""
import pandas as pd
import numpy as np
from ..config import INITIAL_CAPITAL_USD

def backtest(df, strategy_fn, initial_capital=INITIAL_CAPITAL_USD, position_size=0.1):
    """Run backtest on a dataframe with given strategy."""
    df = strategy_fn(df)
    df = df.dropna()
    
    capital = initial_capital
    position = 0  # units held
    trades = []
    
    for i, row in df.iterrows():
        if row['signal'] == 1 and capital >= row['close'] * position_size * capital:
            # Buy
            units = (capital * position_size) / row['close']
            cost = units * row['close']
            capital -= cost
            position += units
            trades.append({'timestamp': row['timestamp'], 'type': 'buy', 'price': row['close'], 'units': units, 'cost': cost})
        elif row['signal'] == -1 and position > 0:
            # Sell
            proceeds = position * row['close']
            capital += proceeds
            trades.append({'timestamp': row['timestamp'], 'type': 'sell', 'price': row['close'], 'units': position, 'proceeds': proceeds})
            position = 0
    
    # Final portfolio value
    final_price = df['close'].iloc[-1]
    final_value = capital + position * final_price
    total_return = (final_value - initial_capital) / initial_capital * 100
    
    return {
        'initial_capital': initial_capital,
        'final_value': final_value,
        'total_return_pct': total_return,
        'num_trades': len(trades),
        'trades': trades,
        'final_position': position,
        'cash': capital
    }

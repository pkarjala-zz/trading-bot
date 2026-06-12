"""Tests for trading strategies."""
import pytest
import pandas as pd
import numpy as np
from src.strategies.strategies import sma_strategy, rsi_strategy, momentum_strategy

def make_test_df(prices):
    """Create test dataframe."""
    df = pd.DataFrame({'timestamp': pd.date_range('2023-01-01', periods=len(prices), freq='D')})
    df['open'] = prices
    df['high'] = prices * 1.02
    df['low'] = prices * 0.98
    df['close'] = prices
    df['volume'] = 1000
    return df

def test_sma_strategy():
    prices = [100] * 60 + [110] * 40
    df = make_test_df(prices)
    result = sma_strategy(df)
    assert 'sma_short' in result.columns
    assert 'sma_long' in result.columns
    assert 'signal' in result.columns

def test_rsi_strategy():
    prices = [100] * 20 + [80] * 10 + [100] * 10
    df = make_test_df(prices)
    result = rsi_strategy(df)
    assert 'rsi' in result.columns
    assert 'signal' in result.columns

def test_momentum_strategy():
    prices = [100] * 20 + [105] * 10
    df = make_test_df(prices)
    result = momentum_strategy(df)
    assert 'momentum' in result.columns
    assert 'signal' in result.columns

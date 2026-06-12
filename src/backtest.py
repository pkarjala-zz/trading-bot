"""CLI backtest runner."""
import sys
import argparse
from src.data.fetcher import fetch_ohlcv, save_to_sqlite, load_from_sqlite
from src.strategies.strategies import sma_strategy, rsi_strategy, momentum_strategy, dca_strategy
from src.strategies.backtest import backtest

STRATEGIES = {
    'sma': sma_strategy,
    'rsi': rsi_strategy,
    'momentum': momentum_strategy,
    'dca': dca_strategy,
}

def main():
    parser = argparse.ArgumentParser(description='Backtest trading strategies')
    parser.add_argument('symbol', help='Symbol, e.g. BTC/USD')
    parser.add_argument('--strategy', default='sma', choices=list(STRATEGIES.keys()))
    parser.add_argument('--days', type=int, default=365)
    parser.add_argument('--exchange', default='kraken')
    args = parser.parse_args()
    
    print(f'Loading data for {args.symbol}...')
    df = load_from_sqlite(args.symbol, args.exchange, days=args.days)
    if df.empty:
        print(f'No data for {args.symbol}, run data fetcher first.')
        return
    
    print(f'Running {args.strategy} backtest...')
    result = backtest(df, STRATEGIES[args.strategy])
    
    print(f'Initial capital: ${result["initial_capital"]:.2f}')
    print(f'Final value: ${result["final_value"]:.2f}')
    print(f'Total return: {result["total_return_pct"]:.2f}%')
    print(f'Number of trades: {result["num_trades"]}')

if __name__ == '__main__':
    main()

"""CLI: Fetch historical data from exchanges."""
import sys
import argparse
from src.data.fetcher import fetch_ohlcv, save_to_sqlite

def main():
    parser = argparse.ArgumentParser(description='Fetch historical OHLCV data')
    parser.add_argument('symbols', nargs='+', help='Symbols, e.g. BTC/USD ETH/USD')
    parser.add_argument('--exchange', default='kraken', choices=['kraken', 'coinbase'])
    parser.add_argument('--days', type=int, default=365)
    parser.add_argument('--timeframe', default='1d', choices=['1m', '5m', '15m', '1h', '4h', '1d'])
    args = parser.parse_args()
    
    for symbol in args.symbols:
        print(f'Fetching {symbol} from {args.exchange}...')
        df = fetch_ohlcv(args.exchange, symbol, days=args.days, timeframe=args.timeframe)
        save_to_sqlite(df)
        print(f'  Saved {len(df)} rows.')
    
    print('Done.')

if __name__ == '__main__':
    main()

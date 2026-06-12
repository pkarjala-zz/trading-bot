"""Main entry point."""
import argparse
import logging
from .telegram.bot import TradingBot
from .dashboard.app import run_dashboard
from .portfolio.paper_engine import PaperPortfolio

logging.basicConfig(level=logging.INFO)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode', choices=['telegram', 'dashboard', 'all'], default='all')
    args = parser.parse_args()
    
    portfolio = PaperPortfolio()
    
    if args.mode in ('telegram', 'all'):
        bot = TradingBot(portfolio_manager=portfolio)
        bot.run()
    
    if args.mode in ('dashboard', 'all'):
        run_dashboard()

if __name__ == '__main__':
    main()

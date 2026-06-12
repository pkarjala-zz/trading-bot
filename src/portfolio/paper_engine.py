"""Paper trading engine - mock orders, no real money."""
import sqlite3
from datetime import datetime
from ..config import SQLITE_DB, INITIAL_CAPITAL_USD

class PaperPortfolio:
    def __init__(self, initial_capital=INITIAL_CAPITAL_USD):
        self.initial_capital = initial_capital
        self.cash = initial_capital
        self.positions = {}  # {symbol: {'units': float, 'avg_price': float}}
        self.orders = []
        self._init_db()
    
    def _init_db(self):
        conn = sqlite3.connect(SQLITE_DB)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS paper_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                symbol TEXT,
                side TEXT,
                order_type TEXT,
                price REAL,
                units REAL,
                total REAL,
                status TEXT
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS paper_positions (
                symbol TEXT PRIMARY KEY,
                units REAL,
                avg_price REAL
            )
        ''')
        conn.commit()
        conn.close()
    
    def place_order(self, symbol, side, order_type, price, units):
        """Simulate order placement."""
        order = {
            'timestamp': datetime.now().isoformat(),
            'symbol': symbol,
            'side': side,
            'order_type': order_type,
            'price': price,
            'units': units,
            'total': price * units,
            'status': 'filled'
        }
        self.orders.append(order)
        
        conn = sqlite3.connect(SQLITE_DB)
        conn.execute('''
            INSERT INTO paper_orders (timestamp, symbol, side, order_type, price, units, total, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (order['timestamp'], order['symbol'], order['side'], order['order_type'],
              order['price'], order['units'], order['total'], order['status']))
        conn.commit()
        conn.close()
        
        if side == 'buy':
            self._apply_buy(symbol, price, units)
        elif side == 'sell':
            self._apply_sell(symbol, price, units)
        
        return order
    
    def _apply_buy(self, symbol, price, units):
        cost = price * units
        if self.cash >= cost:
            self.cash -= cost
            if symbol in self.positions:
                pos = self.positions[symbol]
                total_cost = pos['avg_price'] * pos['units'] + price * units
                pos['units'] += units
                pos['avg_price'] = total_cost / pos['units']
            else:
                self.positions[symbol] = {'units': units, 'avg_price': price}
            self._save_position(symbol)
    
    def _apply_sell(self, symbol, price, units):
        if symbol in self.positions and self.positions[symbol]['units'] >= units:
            self.cash += price * units
            self.positions[symbol]['units'] -= units
            if self.positions[symbol]['units'] == 0:
                del self.positions[symbol]
            self._save_position(symbol)
    
    def _save_position(self, symbol):
        conn = sqlite3.connect(SQLITE_DB)
        if symbol in self.positions:
            conn.execute('''
                INSERT OR REPLACE INTO paper_positions (symbol, units, avg_price)
                VALUES (?, ?, ?)
            ''', (symbol, self.positions[symbol]['units'], self.positions[symbol]['avg_price']))
        else:
            conn.execute('DELETE FROM paper_positions WHERE symbol = ?', (symbol,))
        conn.commit()
        conn.close()
    
    def get_portfolio_value(self, prices):
        """Calculate total portfolio value given current prices."""
        total = self.cash
        for symbol, pos in self.positions.items():
            if symbol in prices:
                total += pos['units'] * prices[symbol]
        return total
    
    def get_positions(self):
        return dict(self.positions)
    
    def get_cash(self):
        return self.cash

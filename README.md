# Trading Bot

Automaattinen paper trading -botti: ETrade + Kraken/Coinbase.

## Ominaisuudet

- **Historical data**: ccxt + SQLite (kerää kurssihistoriat talteen)
- **Backtest**: testaa strategioita historiatietoja vastaan
- **Paper trading**: mock-ordet, ei oikeita varoja
- **Salkun monitorointi**: P&L, hälytykset, positionit
- **Telegram**: komentorivi + hälytykset
- **Dashboard**: Streamlit UI

## Setup

```bash
cd trading-bot
cp .env.example .env
# Täytä .env tiedostoon API-keyt
pip install -r requirements.txt
```

## Käyttö

### 1. Historiadata (Kraken/Coinbase)

```bash
python -m src.fetch_data BTC/USD ETH/USD SOL/USD
```

### 2. Backtest

```bash
python -m src.backtest BTC/USD --strategy sma
python -m src.backtest BTC/USD --strategy rsi
python -m src.backtest BTC/USD --strategy momentum
```

### 3. Paper trading

```bash
python -m src.run --mode telegram
```

### 4. Dashboard

```bash
python -m src.run --mode dashboard
# Avaa http://localhost:8501
```

## Strategiat

| Strategia | Kuvaus |
|---|---|
| SMA | Moving average crossover |
| RSI | RSI mean reversion |
| Momentum | Price momentum |
| DCA | Dollar-cost averaging |

## Arkkitehtuuri

```
src/
  data/fetcher.py      # ccxt → SQLite
  strategies/
    strategies.py     # Strategiafunktiot
    backtest.py       # Backtest engine
  portfolio/
    paper_engine.py   # Paper trading engine
  telegram/bot.py     # Telegram bot
  dashboard/app.py   # Streamlit UI
```

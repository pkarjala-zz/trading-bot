# trading-bot

Automated trading bot for ETrade (USA) and cryptocurrency exchanges.

## Status

🚧 Alustavasti pystyssä — ei vielä toiminnallinen.

## Architecture

```
trading-bot/
├── etrade/          # ETrade API integration
├── exchange/        # Crypto exchange adapters (Kraken, Binance, etc.)
├── strategies/      # Trading strategies
├── core/            # Shared trading engine
└── README.md
```

## TODO

- [ ] ETrade API-yhteys ja auth
- [ ] Crypto exchange adapter (alustavasti Kraken)
- [ ] Perus momentum-strategia
- [ ] Risk management
- [ ] Backtesting framework
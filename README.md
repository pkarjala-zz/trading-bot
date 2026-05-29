# eToro Trading Bot

Automated trading bot for eToro (demo account).

## Setup

```bash
pip install requests websocket-client
export ETORO_API_KEY="your_public_api_key"
export ETORO_USER_KEY="your_user_key"
python test_etoro.py
```

## Structure

```
etoro_client.py   # eToro REST + WebSocket API client
test_etoro.py     # Connection test
requirements.txt  # Dependencies
.env.example      # Env template
```

## ⚠️ Demo Only

Demo account only — no real trades.

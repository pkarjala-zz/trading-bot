#!/usr/bin/env python3
"""eToro API Connection Test"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from etoro_client import EtoroClient

API_KEY = os.environ.get("ETORO_API_KEY")
USER_KEY = os.environ.get("ETORO_USER_KEY")

if not API_KEY or not USER_KEY:
    print("ERROR: Set ETORO_API_KEY and ETORO_USER_KEY env vars")
    sys.exit(1)

print(f"API Key: {API_KEY[:20]}...")
print(f"User Key: {USER_KEY[:30]}...")

client = EtoroClient(API_KEY, USER_KEY)
print("\n=== Testing REST API ===")

tests = [
    ("Watchlists", lambda: client.get_watchlists()),
    ("Positions", lambda: client.get_positions()),
    ("Balance", lambda: client.get_balance()),
]

for name, fn in tests:
    try:
        result = fn()
        print(f"  {name}: OK - {str(result)[:100]}")
    except Exception as e:
        print(f"  {name}: FAILED - {e}")
print("\nDone.")

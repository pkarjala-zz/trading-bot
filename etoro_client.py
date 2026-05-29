"""
eToro API Client
Documentation: https://api-portal.etoro.com/
WebSocket: wss://ws.etoro.com/ws

Usage:
    from etoro_client import EtoroClient
    client = EtoroClient(PUBLIC_API_KEY, USER_KEY)
    client.connect()
"""

import json
import requests
from typing import Optional, Dict, Any, Callable
import threading
import time

class EtoroClient:
    BASE_URL = "https://public-api.etoro.com/api/v1"
    WS_URL = "wss://ws.etoro.com/ws"
    
    def __init__(self, api_key: str, user_key: str):
        self.api_key = api_key
        self.user_key = user_key
        self._ws = None
        self._authenticated = False
        self._subscribers = {}
    
    def _headers(self) -> Dict[str, str]:
        return {
            "x-api-key": self.api_key,
            "x-user-key": self.user_key,
            "Content-Type": "application/json"
        }
    
    # ── REST API ────────────────────────────────────────────────
    
    def get_watchlists(self) -> Dict[str, Any]:
        """Get user watchlists"""
        return self._get("/watchlists")
    
    def get_instruments(self, instrument_ids: list = None) -> Dict[str, Any]:
        """Get instrument details by ID(s)"""
        if instrument_ids:
            ids = ",".join(str(i) for i in instrument_ids)
            return self._get(f"/instruments/{ids}")
        return self._get("/instruments")
    
    def get_quotes(self, instrument_ids: list) -> Dict[str, Any]:
        """Get real-time quotes for instruments"""
        ids = ",".join(str(i) for i in instrument_ids)
        return self._get(f"/quotes/{ids}")
    
    def get_positions(self) -> Dict[str, Any]:
        """Get open positions"""
        return self._get("/positions")
    
    def get_balance(self) -> Dict[str, Any]:
        """Get account balance"""
        return self._get("/account/balance")
    
    def _get(self, path: str) -> Dict[str, Any]:
        import uuid
        headers = self._headers()
        headers["x-request-id"] = str(uuid.uuid4())
        resp = requests.get(f"{self.BASE_URL}{path}", headers=headers, timeout=10)
        resp.raise_for_status()
        return resp.json()
    
    # ── WebSocket ────────────────────────────────────────────────
    
    def connect_ws(self):
        """Connect to WebSocket (for real-time data)"""
        # Note: Requires websocket-client package
        # pip install websocket-client
        try:
            import websocket
        except ImportError:
            raise ImportError("Run: pip install websocket-client")
        
        self._ws = websocket.WebSocketApp(
            self.WS_URL,
            on_message=self._on_ws_message,
            on_error=self._on_ws_error
        )
        thread = threading.Thread(target=self._ws.run_forever)
        thread.daemon = True
        thread.start()
        return self
    
    def authenticate_ws(self):
        """Send WebSocket authentication"""
        self._send({
            "id": str(uuid.uuid4()),
            "operation": "Authenticate",
            "data": {"userKey": self.user_key, "apiKey": self.api_key}
        })
    
    def subscribe(self, topic: str, callback: Callable):
        """Subscribe to a topic (e.g. 'instrument:100000')"""
        self._subscribers[topic] = callback
        self._send({
            "id": str(uuid.uuid4()),
            "operation": "Subscribe",
            "data": {"topics": [topic], "snapshot": False}
        })
    
    def _send(self, msg: dict):
        if self._ws:
            self._ws.send(json.dumps(msg))
    
    def _on_ws_message(self, ws, msg):
        data = json.loads(msg)
        op = data.get("operation", "")
        if op == "Authenticate":
            self._authenticated = data.get("data", {}).get("success", False)
            print(f"WS Auth: {self._authenticated}")
        elif op == "Subscribe":
            topic = data.get("data", {}).get("topic", "")
            if topic in self._subscribers:
                self._subscribers[topic](data)
    
    def _on_ws_error(self, ws, err):
        print(f"WS Error: {err}")
    
    def close_ws(self):
        if self._ws:
            self._ws.close()


if __name__ == "__main__":
    import os, sys
    
    API_KEY = os.environ.get("ETORO_API_KEY")
    USER_KEY = os.environ.get("ETORO_USER_KEY")
    
    if not API_KEY or not USER_KEY:
        print("Set ETORO_API_KEY and ETORO_USER_KEY env vars first")
        sys.exit(1)
    
    client = EtoroClient(API_KEY, USER_KEY)
    
    print("Testing REST API...")
    try:
        wl = client.get_watchlists()
        print(f"Watchlists: {wl}")
    except Exception as e:
        print(f"Watchlists failed: {e}")
    
    print("Done")

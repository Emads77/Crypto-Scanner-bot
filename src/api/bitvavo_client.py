## API wrapper for bitvavo 


import time
from typing import Any, Dict, List, Optional, Tuple
import httpx

BASE = "https://api.bitvavo.com/v2"

class BitvavoClient:
    def __init__(self, timeout=10.0):
        self._client = httpx.Client(timeout=timeout, headers={"User-Agent": "alt-surge-bot/1.0"})

    def close(self):
        self._client.close()

    def get_ticker_24h_all(self) -> List[Dict[str, Any]]:
        # GET /ticker/24h  (all markets) – public
        # Returns 24h stats incl. volume, last price, etc.
        # Weight: 25 for all markets (per docs)
        r = self._client.get(f"{BASE}/ticker/24h")
        r.raise_for_status()
        return r.json()

    def get_ticker_book(self, market: str) -> Dict[str, Any]:
        # GET /ticker/book?market=XYZ
        r = self._client.get(f"{BASE}/ticker/book", params={"market": market})
        r.raise_for_status()
        return r.json()

    def get_candles(self, market: str, interval: str = "1h", limit: int = 25) -> List[List[float]]:
        # GET /{market}/candles?interval=1h&limit=25  -> [[timestamp, open, high, low, close, volume], ...]
        # We fetch 25 last 1h candles (1 latest + 24 prior for RVOL baseline)
        r = self._client.get(f"{BASE}/{market}/candles", params={"interval": interval, "limit": limit})
        r.raise_for_status()
        return r.json()

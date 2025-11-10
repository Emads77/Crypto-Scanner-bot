

from typing import List
from .base_pattern import BasePattern
from ..domain.pattern_result import PatternResult


class ThreeGreenCandlesPattern(BasePattern):
    """Detects 3 consecutive green candles with decent body size."""
    
    def __init__(self, min_body_pct: float = 50.0):
        """python test_pattern.py

        Args:
            min_body_pct: Minimum body size as % of total candle range (default 50%)
        """
        self.min_body_pct = min_body_pct
    
    def detect(self, candles: List, market: str, timeframe: str) -> PatternResult:
        """Check for 3 consecutive green candles."""
        
        # Need at least 3 candles
        if len(candles) < 3:
            return PatternResult(detected=False)
        
        # Get last 3 candles (most recent)
        last_three = candles[:3]
        
        # Check each candle
        for candle in last_three:
            if not self._is_green_with_body(candle):
                return PatternResult(detected=False)
        
        # All 3 passed! Build details
        details = self._build_details(last_three)
        
        return PatternResult(
            detected=True,
            market=market,
            pattern_name="3 Green Candles",
            timeframe=timeframe,
            details=details
        )
    
    def _is_green_with_body(self, candle) -> bool:
        """Check if candle is green and has decent body."""
        # candle = [timestamp, open, high, low, close, volume]
        open_price = float(candle[1])
        high = float(candle[2])
        low = float(candle[3])
        close = float(candle[4])
        
        # Must be green
        if close <= open_price:
            return False
        
        # Calculate body ratio
        total_range = high - low
        if total_range == 0:                       
            return False
        
        body = close - open_price
        body_pct = (body / total_range) * 100
        
        return body_pct >= self.min_body_pct
    
    def _build_details(self, candles) -> dict:
        """Build detailed info about the 3 candles."""
        candle_info = []
        for i, candle in enumerate(candles, 1):
            open_price = float(candle[1])
            close = float(candle[4])
            volume = float(candle[5])
            gain_pct = ((close - open_price) / open_price) * 100
            
            candle_info.append({
                "number": i,
                "gain_pct": round(gain_pct, 2),
                "volume": int(volume)
            })
        
        return {"candles": candle_info}
from abc import ABC, abstractmethod
from typing import List
from ..domain.pattern_result import PatternResult

class BasePattern(ABC):
    """Abstract base class for all pattern detectors."""
    
    @abstractmethod
    def detect(self, candles: List, market: str, timeframe: str) -> PatternResult:
        """
        Analyze candles and detect if pattern exists.
        
        Args:
            candles: List of candle data [[timestamp, open, high, low, close, volume], ...]
            market: Market symbol (e.g., "ADA-EUR")
            timeframe: Candle interval (e.g., "15m", "1h")
        
        Returns:
            PatternResult with detection status and details
        """
        pass
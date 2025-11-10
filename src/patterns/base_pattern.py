from abc import ABC, abstractmethod
from ..domain.pattern_result import PatternResult
from typing import List, Dict, Any  # Add Dict and Any

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
    
    @abstractmethod
    def notificationFormatter(self,details:Dict[str,Any])-> str:
        """
        Format pattern details for alert message.
        
        Args:
            details: Dictionary with pattern-specific data
            
        Returns:
            Formatted string for Telegram alert
        """
        pass
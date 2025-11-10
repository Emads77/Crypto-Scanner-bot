
from typing import Dict, Any



class PatternResult:
    """Result of a pattern detection analysis."""
    
    def __init__(
        self,
        detected: bool,
        market: str = "",
        pattern_name: str = "",
        timeframe: str = "",
        details: Dict[str, Any] = None
    ):
        self.detected = detected
        self.market = market
        self.pattern_name = pattern_name
        self.timeframe = timeframe
        self.details = details or {}
    
    def __repr__(self):
        return f"PatternResult(detected={self.detected}, pattern={self.pattern_name})"
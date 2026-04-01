from typing import List
from .base_pattern import BasePattern
from ..domain.pattern_result import PatternResult


class LaunchpadBreakoutPattern(BasePattern):
    """
    Detects a 'sleeping coin waking up' breakout pattern.
    Conditions:
    1. Coin was quiet (low volatility) for several candles
    2. Volume suddenly spikes well above average
    3. Price breaks above the recent range high
    """

    def __init__(
        self,
        lookback_candles: int = 20,
        min_volume_multiplier: float = 3.0,
        min_breakout_pct: float = 0.04,
        min_sleep_candles: int = 10,
        max_sleep_volatility: float = 0.03
    ):
        self.lookback_candles = lookback_candles
        self.min_volume_multiplier = min_volume_multiplier
        self.min_breakout_pct = min_breakout_pct
        self.min_sleep_candles = min_sleep_candles
        self.max_sleep_volatility = max_sleep_volatility

    def detect(self, candles: List, market: str, timeframe: str) -> PatternResult:
        if timeframe != "4h":
            return PatternResult(detected=False)
        if len(candles) < self.lookback_candles + 2:
            return PatternResult(detected=False)

        current = candles[0]
        history = candles[1:self.lookback_candles + 1]

        # Step 1 - was coin sleeping?
        sleep_high = max(c[2] for c in history)
        sleep_low = min(c[3] for c in history)
        sleep_range = (sleep_high - sleep_low) / sleep_low
        if sleep_range > self.max_sleep_volatility:
            return PatternResult(detected=False)

        # Step 2 - is volume spiking?
        avg_volume = sum(c[5] for c in history) / len(history)
        vol_ratio = current[5] / avg_volume
        if vol_ratio < self.min_volume_multiplier:
            return PatternResult(detected=False)

        # Step 3 - is price breaking out?
        previous_high = max(c[2] for c in history)
        breakout_pct = (current[4] - previous_high) / previous_high
        if breakout_pct < self.min_breakout_pct:
            return PatternResult(detected=False)

        return PatternResult(
            detected=True,
            pattern=self,
            market=market,
            pattern_name="Launchpad Breakout",
            timeframe=timeframe,
            details={
                "breakout_pct": round(breakout_pct * 100, 2),
                "vol_ratio": round(vol_ratio, 2),
                "sleep_range": round(sleep_range * 100, 2),
                "current_close": current[4],
                "previous_high": previous_high,
            }
        )

    def notificationFormatter(self, details: dict) -> str:
        msg = ""
        msg += f"   Breakout: +{details['breakout_pct']}%\n"
        msg += f"   Volume:   {details['vol_ratio']}× average\n"
        msg += f"   Sleep range was: {details['sleep_range']}%\n"
        return msg
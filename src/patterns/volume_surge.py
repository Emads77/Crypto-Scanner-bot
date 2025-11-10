from typing import List
from .base_pattern import BasePattern
from ..domain.pattern_result import PatternResult


class BullishVolumeSurgePattern(BasePattern):
    """Detects when 24h volume doubles with bullish price action."""

    def __init__(self, min_volume_multiplier: float = 2.0):
        """
        Args:
            min_volume_multiplier: Minimum 24h volume increase (default 2.0 = doubled)
        """
        self.min_multiplier = min_volume_multiplier

    def detect(self, candles: List, market: str, timeframe: str) -> PatternResult:
        """Check for 24h volume surge with bullish price."""

        # Only check on daily timeframe
        if timeframe != "1d":
            return PatternResult(detected=False)

        # Need at least 2 days of data
        if len(candles) < 2:
            return PatternResult(detected=False)

        # Get today and yesterday candles (remember: newest first)
        today = candles[0]
        yesterday = candles[1]

        # Extract data
        today_open = float(today[1])
        today_close = float(today[4])
        today_volume = float(today[5])

        yesterday_volume = float(yesterday[5])

        # Check 1: Today must be green (bullish)
        if today_close <= today_open:
            return PatternResult(detected=False)

        # Check 2: Volume must have increased significantly
        if yesterday_volume == 0:
            return PatternResult(detected=False)

        volume_ratio = today_volume / yesterday_volume

        if volume_ratio >= self.min_multiplier:
            gain_pct = ((today_close - today_open) / today_open) * 100

            details = {
                "gain_pct": round(gain_pct, 2),
                "today_volume": int(today_volume),
                "yesterday_volume": int(yesterday_volume),
                "volume_ratio": round(volume_ratio, 2)
            }

            return PatternResult(
                detected=True,
                pattern=self,
                market=market,
                pattern_name="Bullish Volume Surge",
                timeframe=timeframe,
                details=details
            )

        return PatternResult(detected=False)

    def notificationFormatter(self, details):
        msg = ""
        msg += f"   Gain: +{details['gain_pct']}%\n"
        msg += f"   Today Vol: {details['today_volume']:,}\n"
        msg += (
            f"   Yesterday Vol: {details['yesterday_volume']:,}\n"
        )
        msg += f"   Volume Ratio: {details['volume_ratio']}×\n"
        return msg

    # #    msg += f"   Gain: +{result.details['gain_pct']}%\n"
    #             msg += f"   Today Vol: {result.details['today_volume']:,}\n"
    #             msg += (
    #                 f"   Yesterday Vol: {result.details['yesterday_volume']:,}\n"
    #             )
    #             msg += f"   Volume Ratio: {result.details['volume_ratio']}×\n"

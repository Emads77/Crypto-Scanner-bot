from typing import List
from .base_pattern import BasePattern
from ..domain.pattern_result import PatternResult




#It detects a bounce/reversal setup using 3 candles:
# Hammer candle — long lower shadow (price was rejected downward), small upper shadow
# Green confirmation candle — strong bullish candle with volume higher than the hammer
# Current candle — holds above the green candle's close


class TwoCandleBullishReversalPattern(BasePattern):

    def __init__(self, min_lower_shadow_ratio=2.5, max_upper_shadow_ratio=0.3, min_green_body_pct=70.0, min_volume_multiplier=1.05):
        self.min_lower_shadow_ratio = min_lower_shadow_ratio
        self.max_upper_shadow_ratio = max_upper_shadow_ratio
        self.min_green_body_pct = min_green_body_pct
        self.min_volume_multiplier = min_volume_multiplier

    def detect(self, candles: List, market: str, timeframe: str) -> PatternResult:
        

        if timeframe != "4h":
          
            return PatternResult(detected=False)

        if len(candles) < 3:
         
            return PatternResult(detected=False)

        current_candle = candles[0]
        green_candle = candles[1]
        tail_candle = candles[2]
        
        
        # Tail candle measurements
        tail_body = abs(tail_candle[4] - tail_candle[1])  # abs(close - open)
        tail_lower_shadow = min(tail_candle[1], tail_candle[4]) - tail_candle[3]  # min(open, close) - low
        tail_upper_shadow = tail_candle[2] - max(tail_candle[1], tail_candle[4])  # high - max(open, close)
        
        
                
        
        # Check tail shadow ratios
        if tail_body == 0:  # Avoid division by zero
          
            return PatternResult(detected=False)
            
        if tail_lower_shadow < self.min_lower_shadow_ratio * tail_body:
           
            return PatternResult(detected=False)
            
        if tail_upper_shadow > self.max_upper_shadow_ratio * tail_body:
            return PatternResult(detected=False)
        
        # Green candle must be bullish
        if green_candle[4] <= green_candle[1]:  # close <= open
            
            return PatternResult(detected=False)
        
        
        
        # Green candle body check
        green_body = green_candle[4] - green_candle[1]  # close - open
        green_range = green_candle[2] - green_candle[3]  # high - low

        if green_range == 0:
           
            return PatternResult(detected=False)
            
        green_body_pct = (green_body / green_range) * 100

        if green_body_pct < self.min_green_body_pct:
           
            return PatternResult(detected=False)
        
        
        
        # Volume check
        if green_candle[5] < tail_candle[5] * self.min_volume_multiplier:
            
            return PatternResult(detected=False)
        
        # Current candle must not close below green candle
        if current_candle[4] < green_candle[4]:  # current close < green close
           
            return PatternResult(detected=False)
        
        # Pattern detected!
       
        gain_pct = ((green_candle[4] - green_candle[1]) / green_candle[1]) * 100

        return PatternResult(
            detected=True,
            pattern=self,
            market=market,
            pattern_name="Two-Candle Bullish Reversal",
            timeframe=timeframe,
            details={
                "tail_lower_shadow_ratio": round(tail_lower_shadow / tail_body, 2),
                "green_gain_pct": round(gain_pct, 2),
                "green_volume": int(green_candle[5]),
                "volume_increase": round(green_candle[5] / tail_candle[5], 2)
            }
        )
        
        
        
    def notificationFormatter(self, details):
        
        msg = ""
        msg += f"   Green Gain: +{details['green_gain_pct']}%\n"
        msg += f"   Volume Increase: {details['volume_increase']}×\n"
        return msg
            

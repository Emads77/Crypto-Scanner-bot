from src.patterns.two_candle_bullish_reversal import TwoCandleBullishReversalPattern

# [timestamp, open, high, low, close, volume]
candles = [
    [3000, 325.66, 335.76, 320.92, 335.76, 3010],  # Current: holds above green close
    [2000, 310.91, 331.84, 310.78, 327.19, 3290],  # Green: strong body, volume 1.15x  
 [1000, 314.38, 314.47, 298.99, 311.21, 3080]# Hammer: tiny body, huge lower shadow
]

pattern = TwoCandleBullishReversalPattern()
result = pattern.detect(candles, "TEST-EUR", "4h")

print(f"Detected: {result.detected}")
print(f"Details: {result.details}")


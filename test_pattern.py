from src.patterns.three_green import ThreeGreenCandlesPattern

# from src.patterns.three_green import ThreeGreenCandlesPattern

# Fake candle data: [timestamp, open, high, low, close, volume]
# Let's create 3 green candles with good bodies

fake_candles = [
    [1000, 1.00, 1.10, 0.95, 1.08, 50000],  # Green, body = 0.08, range = 0.15, ratio = 53%
    [2000, 1.08, 1.20, 1.05, 1.18, 55000],  # Green, body = 0.10, range = 0.15, ratio = 67%
    [3000, 1.18, 1.30, 1.15, 1.28, 60000],  # Green, body = 0.10, range = 0.15, ratio = 67%
]

# Create pattern detector
pattern = ThreeGreenCandlesPattern(min_body_pct=50.0)

# Test detection
result = pattern.detect(fake_candles, market="TEST-EUR", timeframe="30m")

# Print results
print(f"Detected: {result.detected}")
print(f"Market: {result.market}")
print(f"Pattern: {result.pattern_name}")
print(f"Timeframe: {result.timeframe}")
print(f"Details: {result.details}") 
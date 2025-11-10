from src.api.bitvavo_client import BitvavoClient

api = BitvavoClient()

# Get 5 candles for BTC-EUR on 1h
candles = api.get_candles("BTC-EUR", interval="1h", limit=5)

print("Candle timestamps (first to last in array):")
for i, candle in enumerate(candles):
    timestamp = candle[0]
    print(f"  Index {i}: timestamp = {timestamp}")

print(f"\nFirst timestamp: {candles[0][0]}")
print(f"Last timestamp: {candles[-1][0]}")

if candles[0][0] < candles[-1][0]:
    print("\n✓ Array order: OLDEST → NEWEST")
    print("  candles[-3:] gets the 3 most recent ✓")
else:
    print("\n✗ Array order: NEWEST → OLDEST") 
    print("  candles[-3:] is WRONG - we need candles[:3]!")

api.close()
import logging
from src.api.bitvavo_client import BitvavoClient
from src.notifications.telegram import TelegramNotifier
from src.patterns.three_green import ThreeGreenCandlesPattern
from src.scanner.market_scanner import MarketScanner
from src.utils.config import load_config
from src.patterns.volume_surge import BullishVolumeSurgePattern
from src.patterns.two_candle_bullish_reversal import TwoCandleBullishReversalPattern
from src.patterns.launchpad_breakout import LaunchpadBreakoutPattern



# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)

# Load config
config = load_config()

# Initialize
api = BitvavoClient(timeout=10.0)
notifier = TelegramNotifier(
    bot_token=config["telegram"]["bot_token"], chat_id=config["telegram"]["chat_id"]
)

patterns = [
    ThreeGreenCandlesPattern(min_body_pct=50.0),
    BullishVolumeSurgePattern(min_volume_multiplier=2.0),
    TwoCandleBullishReversalPattern(),
      LaunchpadBreakoutPattern(
        lookback_candles=20,
        min_volume_multiplier=3.0,
        min_breakout_pct=0.04,
        max_sleep_volatility=0.15  # loosened from 3% to 15%
    )
    
]
timeframes = ["15m","1h","4h","1d"]  

scanner = MarketScanner(
    api_client=api,
    notifier=notifier,
    patterns=patterns,
    timeframes=timeframes,
    min_volume_eur=500000,
    max_spread_pct=2.0,
)

# Run ONE scan
print("\n" + "=" * 60)
print("Running test scan...")
print("=" * 60 + "\n")

scanner.scan()

api.close()
print("\nTest complete!")

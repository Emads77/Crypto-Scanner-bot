import logging
from src.api.bitvavo_client import BitvavoClient
from src.notifications.telegram import TelegramNotifier
from src.patterns.three_green import ThreeGreenCandlesPattern
from src.scanner.market_scanner import MarketScanner
from src.scanner.scheduler import ScanScheduler
from src.utils.config import load_config


def main():
    # Load configuration
    config = load_config()
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    logging.info("Starting Crypto Scanner Bot...")
    
    # Initialize components
    api_client = BitvavoClient(timeout=10.0)
    
    notifier = TelegramNotifier(
        bot_token=config["telegram"]["bot_token"],
        chat_id=config["telegram"]["chat_id"]
    )
    
    # Define patterns to check
    patterns = [
        ThreeGreenCandlesPattern(min_body_pct=50.0)
        # Add more patterns here later
    ]
    
    # Define timeframes
    timeframes = [ "4h"]
    # ,"15m", "1h", "1d", "1w"
    
    # Create scanner
    scanner = MarketScanner(
        api_client=api_client,
        notifier=notifier,
        patterns=patterns,
        timeframes=timeframes,
        min_volume_eur=50000,
        max_spread_pct=2.0
    )
    
    # Create scheduler
    scheduler = ScanScheduler(
        scan_function=scanner.scan,
        interval_minutes=15
    )
    
    # Start scanning!
    try:
        scheduler.start()
    finally:
        api_client.close()
        logging.info("Bot shutdown complete")


if __name__ == "__main__":
    main()
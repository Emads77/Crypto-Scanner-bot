import logging
from typing import List, Dict
from ..api.bitvavo_client import BitvavoClient
from ..patterns.base_pattern import BasePattern
from ..notifications.telegram import TelegramNotifier
from ..domain.pattern_result import PatternResult


class MarketScanner:
    """Scans markets for pattern detections across multiple timeframes."""

    def __init__(
        self,
        api_client: BitvavoClient,
        notifier: TelegramNotifier,
        patterns: List[BasePattern],
        timeframes: List[str],
        min_volume_eur: float = 50000,
        max_spread_pct: float = 2.0,
    ):
        self.api = api_client
        self.notifier = notifier
        self.patterns = patterns
        self.timeframes = timeframes
        self.min_volume = min_volume_eur
        self.max_spread = max_spread_pct
        self.cooldowns = {}  # {(market, timeframe, pattern): timestamp}

        logging.info(
            f"Scanner initialized: {len(patterns)} patterns, "
            f"{len(timeframes)} timeframes, min vol €{min_volume_eur:,.0f}"
        )

    def scan(self):
        """Run a full scan of all markets."""
        logging.info("=" * 50)
        logging.info("Starting market scan...")

        try:
            # Get all markets with 24h data
            all_tickers = self.api.get_ticker_24h_all()
            eur_markets = [
                t for t in all_tickers if t.get("market", "").endswith("-EUR")
            ]

            logging.info(f"Found {len(eur_markets)} EUR markets")

            # Apply filters
            filtered = self._apply_filters(eur_markets)
            logging.info(f"{len(filtered)} markets passed filters")

            # Collect all detections (don't send immediately)
            detections = []

            for market_data in filtered:
                market = market_data["market"]
                market_detections = self._scan_market(market)
                detections.extend(market_detections)

            # Send one batched message
            if detections:
                self._send_batch_alert(detections)
                logging.info(
                    f"Scan complete. {len(detections)} patterns detected.")
            else:
                logging.info("Scan complete. No patterns detected.")

        except Exception as e:
            logging.exception(f"Scan failed: {e}")

    def _apply_filters(self, tickers: List[Dict]) -> List[Dict]:
        """Filter markets by volume and spread."""
        passed = []

        for ticker in tickers:
            market = ticker.get("market")
            volume_quote = float(ticker.get("volumeQuote") or 0)

            # Volume filter
            if volume_quote < self.min_volume:
                logging.debug(f"{market}: Low volume €{volume_quote:,.0f}")
                continue

            # Spread filter
            try:
                book = self.api.get_ticker_book(market)
                bid = float(book.get("bid", 0))
                ask = float(book.get("ask", 0))

                if bid <= 0 or ask <= 0:
                    logging.debug(f"{market}: Invalid bid/ask")
                    continue

                spread = self._calc_spread_pct(ask, bid)
                if spread > self.max_spread:
                    logging.debug(f"{market}: Wide spread {spread:.2f}%")
                    continue

                passed.append(ticker)

            except Exception as e:
                logging.debug(f"{market}: Error checking spread - {e}")
                continue

        return passed

    def _scan_market(self, market: str) -> List[PatternResult]:
        """Scan one market across all timeframes and patterns. Returns detections."""
        detections = []

        for timeframe in self.timeframes:
            try:
                # Fetch candles
                candles = self.api.get_candles(
                    market, interval=timeframe, limit=50)

                if len(candles) < 3:
                    continue

                # Check all patterns
                for pattern in self.patterns:
                    result = pattern.detect(candles, market, timeframe)

                    if result.detected:
                        if self._can_alert(market, timeframe, result.pattern_name):
                            detections.append(result)
                            self._mark_alerted(
                                market, timeframe, result.pattern_name)
                            logging.info(
                                f"DETECTED: {market} {timeframe} - {result.pattern_name}"
                            )
                        else:
                            logging.debug(
                                f"{market} {timeframe} {result.pattern_name}: In cooldown"
                            )

            except Exception as e:
                logging.debug(f"{market} {timeframe}: Error - {e}")

        return detections

    def _can_alert(self, market: str, timeframe: str, pattern_name: str) -> bool:
        """Check if we can send alert (cooldown check)."""
        import time

        key = (market, timeframe, pattern_name)
        last_alert = self.cooldowns.get(key, 0)

        # Calculate cooldown based on timeframe (3× the interval)
        cooldown_seconds = self._get_cooldown_seconds(timeframe)

        now = time.time()
        return (now - last_alert) >= cooldown_seconds

    def _mark_alerted(self, market: str, timeframe: str, pattern_name: str):
        """Mark that we sent an alert."""
        import time

        key = (market, timeframe, pattern_name)
        self.cooldowns[key] = time.time()

    def _get_cooldown_seconds(self, timeframe: str) -> int:
        """Get cooldown duration (3× the timeframe)."""
        mapping = {
            "15m": 45 * 60,  # 45 minutes
            "1h": 3 * 3600,  # 3 hours
            "4h": 12 * 3600,  # 12 hours
            "1d": 3 * 86400,  # 3 days
            "1w": 3 * 7 * 86400,  # 3 weeks
        }
        return mapping.get(timeframe, 3600)  # Default 1 hour

    def _send_batch_alert(self, detections: List[PatternResult]):
        """Send one message with all detections."""
        if not detections:
            return

        # Header
        msg = f"🚨 <b>Scan Alert - {len(detections)} Pattern(s) Detected</b>\n\n"

        # List each detection
        for i, result in enumerate(detections, 1):
            # TradingView web link
            tv_symbol = result.market.replace("-", "")
            tv_link = (
                f"https://www.tradingview.com/chart/?symbol=BITVAVO:{tv_symbol}"
            )

            msg += f"{i}. <b>{result.market}</b> - {result.pattern_name} ({result.timeframe})\n"
            msg += result.pattern.notificationFormatter(result.details)
            msg += f"   {tv_link}\n\n"  # Add this line!

        self.notifier.send(msg)

    def _calc_spread_pct(self, ask: float, bid: float) -> float:
        """Calculate spread percentage."""
        if ask <= 0 or bid <= 0:
            return 100.0
        mid = (ask + bid) / 2
        return ((ask - bid) / mid) * 100

import time
import logging
from typing import Callable
from datetime import datetime


class ScanScheduler:
    """Runs market scans at regular intervals."""
    
    def __init__(self, scan_function: Callable, interval_minutes: int = 15):
        """
        Args:
            scan_function: Function to call (usually scanner.scan)
            interval_minutes: How often to run (default 15 min)
        """
        self.scan_function = scan_function
        self.interval_seconds = interval_minutes * 60
        self.running = False
        
        logging.info(f"Scheduler initialized: running every {interval_minutes} minutes")
    
    def start(self):
        """Start the scheduler loop."""
        self.running = True
        logging.info("Scheduler started")
        
        try:
            while self.running:
                self._run_scan()
                self._wait_for_next_interval()
        
        except KeyboardInterrupt:
            logging.info("Scheduler stopped by user (Ctrl+C)")
            self.running = False
        
        except Exception as e:
            logging.exception(f"Scheduler crashed: {e}")
            self.running = False
    
    def stop(self):
        """Stop the scheduler."""
        self.running = False
        logging.info("Scheduler stopped")
    
    def _run_scan(self):
        """Execute one scan."""
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logging.info(f"\n{'='*60}")
            logging.info(f"Scan triggered at {now}")
            logging.info(f"{'='*60}\n")
            
            self.scan_function()
            
        except Exception as e:
            logging.exception(f"Scan execution failed: {e}")
    
    def _wait_for_next_interval(self):
        """Wait until next scheduled run."""
        next_run = time.time() + self.interval_seconds
        next_run_time = datetime.fromtimestamp(next_run).strftime("%H:%M:%S")
        
        logging.info(f"Next scan at {next_run_time}")
        logging.info(f"Sleeping for {self.interval_seconds / 60:.0f} minutes...\n")
        
        time.sleep(self.interval_seconds)
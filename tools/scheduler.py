"""
Scheduler
Runs the scraper orchestrator every 24 hours.
Can also be triggered manually.

Usage:
  python tools/scheduler.py          # Run once then schedule every 24h
  python tools/scheduler.py --once   # Run once and exit
"""

import sys
import time
import threading
from datetime import datetime, timezone

INTERVAL_HOURS = 24
INTERVAL_SECONDS = INTERVAL_HOURS * 3600


def run_scrapers():
    """Import and run the scraper orchestrator."""
    import os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from run_scrapers import run
    run()


def schedule_loop():
    """Run scrapers on a fixed interval."""
    print(f"\nScheduler started. Will run every {INTERVAL_HOURS} hours.")
    print("Press Ctrl+C to stop.\n")

    while True:
        print(f"\n--- Scheduled run at {datetime.now(timezone.utc).isoformat()} ---\n")
        try:
            run_scrapers()
        except Exception as e:
            print(f"[SCHEDULER ERROR] {type(e).__name__}: {e}", file=sys.stderr)

        print(f"\nNext run in {INTERVAL_HOURS} hours...")
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    if "--once" in sys.argv:
        run_scrapers()
    else:
        # Run immediately, then schedule
        run_scrapers()
        schedule_loop()

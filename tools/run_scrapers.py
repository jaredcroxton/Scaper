"""
Scraper Orchestrator
Runs all scrapers, merges results, deduplicates, and writes the final payload.
"""

import json
import os
import sys
from datetime import datetime, timezone

# Add tools directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scrape_reddit import scrape as scrape_reddit
from scrape_bens_bites import scrape as scrape_bens_bites
from scrape_rundown import scrape as scrape_rundown

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
OUTPUT_FILE = os.path.join(DATA_DIR, "articles.json")
ERROR_LOG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".tmp", "scraper_errors.log")


def deduplicate(articles: list[dict]) -> list[dict]:
    """Remove duplicate articles by URL."""
    seen_urls = set()
    unique = []
    for article in articles:
        url = article.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique.append(article)
    return unique


def log_error(source: str, error: str):
    """Log errors to .tmp/scraper_errors.log."""
    os.makedirs(os.path.dirname(ERROR_LOG), exist_ok=True)
    timestamp = datetime.now(timezone.utc).isoformat()
    with open(ERROR_LOG, "a") as f:
        f.write(f"[{timestamp}] [{source}] {error}\n")


def run():
    """Run all scrapers and produce the final payload."""
    print("=" * 60)
    print("SCAPER - AI Article Aggregator")
    print(f"Run started: {datetime.now(timezone.utc).isoformat()}")
    print("=" * 60)

    all_articles = []
    sources_scraped = []

    # Run each scraper with error isolation
    scrapers = [
        ("Reddit", scrape_reddit),
        ("Ben's Bites", scrape_bens_bites),
        ("The Rundown AI", scrape_rundown),
    ]

    for name, scraper_fn in scrapers:
        print(f"\n[{name}]")
        try:
            articles = scraper_fn()
            all_articles.extend(articles)
            sources_scraped.append(name)
            print(f"  -> {len(articles)} articles collected")
        except Exception as e:
            error_msg = f"{type(e).__name__}: {e}"
            print(f"  -> FAILED: {error_msg}", file=sys.stderr)
            log_error(name, error_msg)

    # Deduplicate
    before_dedup = len(all_articles)
    all_articles = deduplicate(all_articles)
    after_dedup = len(all_articles)
    if before_dedup != after_dedup:
        print(f"\nDeduplication: {before_dedup} -> {after_dedup} articles")

    # Sort by published_at descending (newest first)
    all_articles.sort(key=lambda a: a.get("published_at", ""), reverse=True)

    # Check if we have new data
    if not all_articles:
        print("\nNo new articles found. Keeping existing data file.")
        return

    # Build payload
    payload = {
        "last_updated": datetime.now(timezone.utc).isoformat(),
        "total_articles": len(all_articles),
        "sources_scraped": sources_scraped,
        "articles": all_articles,
    }

    # Write output
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"\n{'=' * 60}")
    print(f"COMPLETE: {len(all_articles)} articles written to data/articles.json")
    print(f"Sources: {', '.join(sources_scraped)}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    run()

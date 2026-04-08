# SOP: Article Scraping System

## Goal
Collect AI-related articles from the last 24 hours across multiple sources and output a unified JSON payload.

## Inputs
- Source configurations (URLs, types)
- Time window: 24 hours from execution time

## Outputs
- `data/articles.json` — Unified article payload (see gemini.md for schema)

## Tool Logic

### 1. Reddit Scraper (`tools/scrape_reddit.py`)
- **Endpoint:** `https://www.reddit.com/r/{subreddit}/new.json?limit=100`
- **Subreddits:** artificial, MachineLearning, singularity, ChatGPT, LocalLLaMA
- **Headers:** Custom User-Agent `ScaperBot/1.0`
- **Rate Limit:** 2-second delay between subreddit requests
- **Filter:** `created_utc` within last 86400 seconds
- **Dedup:** By URL
- **Output:** List of Article objects

### 2. Ben's Bites Scraper (`tools/scrape_bens_bites.py`)
- **Endpoint:** RSS feed `https://bensbites.substack.com/feed`
- **Parser:** `feedparser` library
- **Filter:** `published_parsed` within last 24 hours
- **Output:** List of Article objects

### 3. The Rundown AI Scraper (`tools/scrape_rundown.py`)
- **Endpoint:** RSS feed `https://rss.beehiiv.com/feeds/2R3C6Bt5wj.xml`
- **Parser:** `feedparser` library
- **Filter:** `published_parsed` within last 24 hours
- **Output:** List of Article objects

### 4. Orchestrator (`tools/run_scrapers.py`)
- Calls each scraper sequentially
- Merges all article lists
- Deduplicates by URL (keeps first occurrence)
- Sorts by `published_at` descending (newest first)
- Writes to `data/articles.json`
- If no new articles found and file exists, does not overwrite

## Edge Cases
- If a source fails, log the error and continue with remaining sources
- If RSS returns items older than 24h, filter them out client-side
- Reddit self-posts: use `selftext` (truncated) as summary
- Missing summaries: use title as fallback
- Empty thumbnail: set to null

## Error Handling
- Network errors: log and skip source
- Parse errors: log and skip individual article
- All errors written to `.tmp/scraper_errors.log`

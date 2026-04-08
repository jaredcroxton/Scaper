"""
Reddit AI Scraper
Scrapes recent AI-related posts from multiple subreddits using Reddit's public JSON API.
"""

import hashlib
import json
import time
import sys
import os
from datetime import datetime, timezone
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

SUBREDDITS = [
    "artificial",
    "MachineLearning",
    "singularity",
    "ChatGPT",
    "LocalLLaMA",
]

USER_AGENT = "ScaperBot/1.0"
RATE_LIMIT_DELAY = 2  # seconds between requests
HOURS_WINDOW = 24
MAX_POSTS_PER_SUB = 100


def make_article_id(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:16]


def fetch_subreddit(subreddit: str) -> list[dict]:
    """Fetch recent posts from a subreddit."""
    url = f"https://www.reddit.com/r/{subreddit}/new.json?limit={MAX_POSTS_PER_SUB}"
    req = Request(url, headers={"User-Agent": USER_AGENT})

    try:
        with urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
    except (URLError, HTTPError) as e:
        print(f"  [ERROR] Failed to fetch r/{subreddit}: {e}", file=sys.stderr)
        return []

    now = datetime.now(timezone.utc)
    cutoff = now.timestamp() - (HOURS_WINDOW * 3600)
    articles = []

    for child in data.get("data", {}).get("children", []):
        post = child.get("data", {})
        created = post.get("created_utc", 0)

        if created < cutoff:
            continue

        # Build article URL
        if post.get("is_self"):
            article_url = f"https://www.reddit.com{post.get('permalink', '')}"
        else:
            article_url = post.get("url", "")

        if not article_url:
            continue

        # Build summary
        summary = post.get("selftext", "")[:300] if post.get("selftext") else ""
        if not summary:
            summary = post.get("title", "")[:300]

        # Thumbnail
        thumbnail = post.get("thumbnail", "")
        if thumbnail in ("self", "default", "nsfw", "spoiler", "image", ""):
            thumbnail = None

        articles.append({
            "id": make_article_id(article_url),
            "title": post.get("title", ""),
            "url": article_url,
            "summary": summary,
            "source": f"r/{subreddit}",
            "source_type": "reddit",
            "author": post.get("author"),
            "published_at": datetime.fromtimestamp(created, tz=timezone.utc).isoformat(),
            "scraped_at": now.isoformat(),
            "score": post.get("score", 0),
            "comments_count": post.get("num_comments", 0),
            "thumbnail": thumbnail,
            "tags": [subreddit, "reddit"],
        })

    return articles


def scrape() -> list[dict]:
    """Scrape all configured subreddits."""
    all_articles = []

    for i, sub in enumerate(SUBREDDITS):
        print(f"  Scraping r/{sub}...")
        articles = fetch_subreddit(sub)
        all_articles.extend(articles)
        print(f"  Found {len(articles)} articles from r/{sub}")

        # Rate limit (skip delay after last request)
        if i < len(SUBREDDITS) - 1:
            time.sleep(RATE_LIMIT_DELAY)

    return all_articles


if __name__ == "__main__":
    print("Reddit Scraper - Starting...")
    results = scrape()
    print(f"Total Reddit articles: {len(results)}")

    # Write to tmp for testing
    os.makedirs(".tmp", exist_ok=True)
    with open(".tmp/reddit_articles.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Written to .tmp/reddit_articles.json")

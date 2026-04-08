"""
The Rundown AI Scraper
Scrapes recent articles from The Rundown AI newsletter via Beehiiv RSS feed.
"""

import hashlib
import json
import os
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from email.utils import parsedate_to_datetime
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from html import unescape
import re

RSS_FEED_URL = "https://rss.beehiiv.com/feeds/2R3C6Bt5wj.xml"
USER_AGENT = "ScaperBot/1.0"
HOURS_WINDOW = 24
SOURCE_NAME = "The Rundown AI"


def make_article_id(url: str) -> str:
    return hashlib.sha256(url.encode()).hexdigest()[:16]


def strip_html(text: str) -> str:
    """Remove HTML tags and decode entities."""
    clean = re.sub(r"<[^>]+>", "", text)
    return unescape(clean).strip()


def parse_date(date_str: str) -> datetime | None:
    """Parse RFC 2822 date string."""
    try:
        return parsedate_to_datetime(date_str)
    except Exception:
        try:
            return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        except Exception:
            return None


def fetch_rss() -> list[dict]:
    """Fetch and parse the RSS feed."""
    req = Request(RSS_FEED_URL, headers={
        "User-Agent": USER_AGENT,
        "Accept": "application/rss+xml, application/xml, text/xml",
    })

    try:
        with urlopen(req, timeout=20) as resp:
            xml_data = resp.read().decode()
    except (URLError, HTTPError) as e:
        print(f"  [ERROR] Failed to fetch Rundown AI RSS: {e}", file=sys.stderr)
        return []

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=HOURS_WINDOW)
    articles = []

    try:
        root = ET.fromstring(xml_data)
    except ET.ParseError as e:
        print(f"  [ERROR] Failed to parse RSS XML: {e}", file=sys.stderr)
        return []

    # Handle RSS 2.0 format
    channel = root.find("channel")
    if channel is None:
        # Try Atom format
        ns = {"atom": "http://www.w3.org/2005/Atom"}
        entries = root.findall("atom:entry", ns)
        for entry in entries:
            title = entry.findtext("atom:title", "", ns)
            link_el = entry.find("atom:link", ns)
            link = link_el.get("href", "") if link_el is not None else ""
            summary = strip_html(entry.findtext("atom:summary", "", ns) or entry.findtext("atom:content", "", ns) or "")
            pub_date = parse_date(entry.findtext("atom:published", "", ns) or entry.findtext("atom:updated", "", ns) or "")

            if pub_date and pub_date < cutoff:
                continue

            articles.append({
                "id": make_article_id(link),
                "title": title,
                "url": link,
                "summary": summary[:300],
                "source": SOURCE_NAME,
                "source_type": "newsletter",
                "author": "The Rundown AI",
                "published_at": pub_date.isoformat() if pub_date else now.isoformat(),
                "scraped_at": now.isoformat(),
                "score": None,
                "comments_count": None,
                "thumbnail": None,
                "tags": ["rundown-ai", "newsletter", "ai"],
            })
        return articles

    # RSS 2.0
    items = channel.findall("item")
    for item in items:
        title = item.findtext("title", "")
        link = item.findtext("link", "")
        description = strip_html(item.findtext("description", "") or "")
        pub_date_str = item.findtext("pubDate", "")
        author = item.findtext("author", "") or item.findtext("{http://purl.org/dc/elements/1.1/}creator", "")

        pub_date = parse_date(pub_date_str) if pub_date_str else None

        if pub_date and pub_date < cutoff:
            continue

        # Try to extract thumbnail from description HTML
        thumbnail = None
        raw_desc = item.findtext("description", "")
        img_match = re.search(r'<img[^>]+src="([^"]+)"', raw_desc or "")
        if img_match:
            thumbnail = img_match.group(1)

        articles.append({
            "id": make_article_id(link),
            "title": title,
            "url": link,
            "summary": description[:300] if description else title[:300],
            "source": SOURCE_NAME,
            "source_type": "newsletter",
            "author": author or "The Rundown AI",
            "published_at": pub_date.isoformat() if pub_date else now.isoformat(),
            "scraped_at": now.isoformat(),
            "score": None,
            "comments_count": None,
            "thumbnail": thumbnail,
            "tags": ["rundown-ai", "newsletter", "ai"],
        })

    return articles


def scrape() -> list[dict]:
    """Main scrape function."""
    print(f"  Fetching RSS from {RSS_FEED_URL}...")
    articles = fetch_rss()
    print(f"  Found {len(articles)} articles from {SOURCE_NAME}")
    return articles


if __name__ == "__main__":
    print("The Rundown AI Scraper - Starting...")
    results = scrape()
    print(f"Total Rundown AI articles: {len(results)}")

    os.makedirs(".tmp", exist_ok=True)
    with open(".tmp/rundown_articles.json", "w") as f:
        json.dump(results, f, indent=2)
    print("Written to .tmp/rundown_articles.json")

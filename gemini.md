# gemini.md - Data Schema & System Law

## Status: SCHEMA APPROVED - BUILD AUTHORIZED

---

## Sources

| Source | Method | Endpoint |
|---|---|---|
| Ben's Bites | Substack RSS | `https://bensbites.substack.com/feed` |
| The Rundown AI | Beehiiv RSS | `https://rss.beehiiv.com/feeds/2R3C6Bt5wj.xml` |
| Reddit (r/artificial) | JSON API | `https://www.reddit.com/r/artificial/new.json?limit=50` |
| Reddit (r/MachineLearning) | JSON API | `https://www.reddit.com/r/MachineLearning/new.json?limit=50` |
| Reddit (r/singularity) | JSON API | `https://www.reddit.com/r/singularity/new.json?limit=50` |
| Reddit (r/ChatGPT) | JSON API | `https://www.reddit.com/r/ChatGPT/new.json?limit=50` |
| Reddit (r/LocalLLaMA) | JSON API | `https://www.reddit.com/r/LocalLLaMA/new.json?limit=50` |

---

## Article Schema (Single Article)

```json
{
  "id": "string (sha256 hash of url)",
  "title": "string",
  "url": "string",
  "summary": "string (max 300 chars)",
  "source": "string (e.g. 'Ben\\'s Bites', 'The Rundown AI', 'r/artificial')",
  "source_type": "string ('newsletter' | 'reddit')",
  "author": "string | null",
  "published_at": "string (ISO 8601)",
  "scraped_at": "string (ISO 8601)",
  "score": "number | null (Reddit upvotes, null for newsletters)",
  "comments_count": "number | null",
  "thumbnail": "string | null (image URL)",
  "tags": ["string"]
}
```

## Output File (Delivery Payload)

```json
{
  "last_updated": "string (ISO 8601)",
  "total_articles": "number",
  "sources_scraped": ["string"],
  "articles": [
    { "...Article Schema..." }
  ]
}
```

## Saved Articles (localStorage → Supabase later)

```json
{
  "saved_articles": [
    {
      "id": "string (article id)",
      "saved_at": "string (ISO 8601)"
    }
  ]
}
```

---

## Behavioral Rules

1. **24-Hour Window:** Only collect articles published within the last 24 hours.
2. **Deduplication:** Deduplicate by URL. If the same URL appears from multiple sources, keep the first occurrence.
3. **No Empty Runs:** If no new articles are found, do not overwrite the existing data file.
4. **Rate Limiting:** Wait 2 seconds between Reddit API calls. Max 10 requests/minute.
5. **Graceful Failure:** If one source fails, continue scraping others. Log the error.
6. **User-Agent:** Always send a custom User-Agent header: `ScaperBot/1.0`.
7. **Data File:** Scrapers write to `data/articles.json`. Dashboard reads from it.
8. **Save Persistence:** Saved articles stored in localStorage (migrate to Supabase later).
9. **Schedule:** Run scrapers every 24 hours via cron or scheduler.
10. **Extensibility:** New sources can be added by creating a new scraper in `tools/` and registering it in the orchestrator.

---

## Architectural Invariants

- Scrapers are atomic: one file per source.
- All scrapers return a list of Article Schema objects.
- The orchestrator merges, deduplicates, and writes the final payload.
- The dashboard is a static site that reads `data/articles.json`.
- `.tmp/` is used for intermediate scraper outputs.

---

## Maintenance Log
_To be populated during Trigger phase._

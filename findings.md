# Findings

## Research & Discoveries

---

### Initial State
- Repository: `jaredcroxton/Scaper`
- Starting state: Empty repository
- Date initialized: 2026-04-08

---

## Source Research (2026-04-08)

### Ben's Bites
- Newsletter on Beehiiv platform (formerly Substack)
- RSS feed available at: `https://bensbites.beehiiv.com/feed`
- Alternative: `https://rss.beehiiv.com/feeds/` (need exact feed ID)
- Bot protection on main site; RSS is the reliable path
- Returns XML with title, link, pubDate, description

### The Rundown AI
- Newsletter on Beehiiv platform
- RSS feed: `https://rss.beehiiv.com/feeds/2R3C6Bt5wj.xml`
- Archive at: `https://www.therundown.ai/archive/`
- Sub-publications exist (aiuniversity, robotnews, tech)
- RSS is the best approach - structured XML, no auth needed

### Reddit
- Best AI subreddits: r/artificial, r/MachineLearning, r/singularity, r/ChatGPT, r/LocalLLaMA
- Public JSON API: append `.json` to any URL
- Use `new.json?limit=100` and filter by `created_utc`
- Or use `top.json?t=day` for Reddit's top-of-day sort
- Custom User-Agent header required to avoid 429 errors
- Rate limit: ~10 req/min unauthenticated
- Response structure: `data.children[].data` contains title, url, permalink, score, created_utc, etc.

## Constraints
- Beehiiv/Substack sites have bot protection on HTML pages; use RSS feeds
- Reddit requires custom User-Agent header
- Reddit rate limit: 2s delay between requests recommended
- All sources are public, no API keys needed for initial version

## Edge Cases
- RSS feeds may return items older than 24h; filter client-side by date
- Reddit posts may link to external articles or be self-posts
- Some articles may lack summaries; use title as fallback

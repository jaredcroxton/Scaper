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
- Newsletter on **Substack** platform (custom domain: bensbites.com)
- RSS feed: `https://bensbites.substack.com/feed` (RSS 2.0)
- Substack API also available: `https://bensbites.substack.com/api/v1/archive?sort=new&limit=12`
- **Important:** Must use `bensbites.substack.com` subdomain, not `bensbites.com` (403 block)
- Additional resources: `news.bensbites.com` (community-voted links), `catalog.bensbites.com` (tools directory)
- Returns XML with title, link, pubDate, description, content:encoded

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

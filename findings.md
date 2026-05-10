# Findings - DIY Space Transformer

## Research and Discoveries

---

### Project Context
- **Market:** Australian homeowners doing DIY renovations
- **Primary retailer:** Bunnings (68% market share)
- **Secondary retailers:** Mitre 10, Beaumont Tiles, Total Tools
- **Currency:** AUD only

---

## Technical Decisions

### Stack
| Layer | Choice | Reason |
|-------|--------|--------|
| Frontend | Next.js (App Router) | SSR, API routes, Vercel deploy |
| Auth/DB/Storage | Supabase | All-in-one, RLS, real-time |
| Image Transform | OpenAI GPT-Image-1 | Best quality for room transformations |
| Photo Analysis | Google Gemini Vision | Material identification, spatial understanding |
| Hosting | Vercel | Native Next.js support |

### Pricing Data Approach (PENDING DECISION)
- **Option A:** Live scraping via Firecrawl (user leaning this way)
  - Pro: Real-time accuracy, always current pricing
  - Con: Fragile if retailer sites change, rate limiting, legal grey area
- **Option B:** Static Supabase product database, seeded manually, refreshed weekly
  - Pro: Reliable, fast, no scraping risk
  - Con: Prices may drift between refreshes

### Monetisation Model
| Tier | Scans/Month | Price |
|------|-------------|-------|
| Free | 3 | $0 |
| Pro | 20 | $9.95/month |
- Reset: 1st of each calendar month
- Gate triggers after free scans consumed

---

## Constraints

### Refused Project Types (Safety/Legal)
- Structural modifications
- Electrical work
- Gas fitting
- Plumbing behind walls
- Asbestos removal
- Anything requiring a licensed tradesperson in Australia

### Input Validation
- Description: min 15 chars, max 500 chars
- If no room keyword detected: soft prompt asking which room
- Tip card (dismissable): describe space, mention materials, note what to keep/remove, add budget

### Design Constraints
- Dark theme
- Mobile first
- No em dashes (anywhere, including code comments)
- Single monolithic file pattern (no componentisation)
- Soft delete only

---

## API Behaviours
_To be populated during Link phase after key verification._

## Edge Cases
_To be populated during Architect phase._

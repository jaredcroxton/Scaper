# Project Constitution - DIY Space Transformer

## Identity
A web app where Australian homeowners upload a photo of a room or outdoor space, describe what they want to change, and receive an AI-generated before/after transformation visual plus an itemised pricing guide with direct buy links to Australian retailers.

## Protocol: B.L.A.S.T.
## Architecture: A.N.T. 3-Layer
## Stack: Next.js (App Router) + Supabase + Vercel + OpenAI GPT-Image-1 + Google Gemini Vision

---

## Architectural Invariants

1. No application code until this schema is confirmed.
2. Single monolithic file pattern for page components. Never componentise.
3. No em dashes anywhere including code comments.
4. Soft delete only. Never hard delete user records.
5. AUD pricing only. Always show $ sign.
6. Mobile first. Dark theme.
7. Retailer priority: Bunnings > Mitre 10 > Beaumont Tiles > Total Tools.
8. Refused projects (structural, electrical, gas, plumbing behind walls, asbestos) must be blocked with a friendly message directing to a licensed professional.
9. Scan counts reset on the 1st of each calendar month.
10. Free tier: 3 scans/month. Pro tier: 20 scans/month at $9.95/month.

---

## Data Schema

### Table: users

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | uuid | PK, default gen_random_uuid() | Maps to Supabase auth.users.id |
| email | text | NOT NULL, UNIQUE | From auth provider |
| display_name | text | NULL | Optional |
| avatar_url | text | NULL | Optional |
| tier | text | NOT NULL, default 'free' | 'free' or 'pro' |
| scans_used_this_month | integer | NOT NULL, default 0 | Resets on 1st of month |
| scan_reset_date | date | NOT NULL | 1st of current month |
| created_at | timestamptz | NOT NULL, default now() | |
| updated_at | timestamptz | NOT NULL, default now() | |
| deleted_at | timestamptz | NULL | Soft delete |

### Table: scans

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | uuid | PK, default gen_random_uuid() | |
| user_id | uuid | FK -> users.id, NOT NULL | |
| original_photo_url | text | NOT NULL | Supabase Storage path |
| transformed_photo_url | text | NULL | Set after AI completes |
| description | text | NOT NULL | Min 15, max 500 chars |
| room_type | text | NULL | kitchen, bathroom, bedroom, living, outdoor, garage, laundry, other |
| budget_range | text | NULL | 'under_500', '500_2000', '2000_5000', '5000_plus' |
| outcome_type | text | NULL | 'refresh', 'renovation', 'style_change', 'repair' |
| gemini_analysis | jsonb | NULL | Raw Gemini Vision response |
| status | text | NOT NULL, default 'pending' | pending, analysing, transforming, pricing, complete, failed |
| error_message | text | NULL | If status is 'failed' |
| created_at | timestamptz | NOT NULL, default now() | |
| completed_at | timestamptz | NULL | When status becomes 'complete' |
| deleted_at | timestamptz | NULL | Soft delete |

### Table: scan_products

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | uuid | PK, default gen_random_uuid() | |
| scan_id | uuid | FK -> scans.id, NOT NULL | |
| product_name | text | NOT NULL | |
| category | text | NOT NULL | paint, tile, fixture, hardware, timber, lighting, flooring, other |
| estimated_price_aud | numeric(10,2) | NOT NULL | |
| retailer | text | NOT NULL | bunnings, mitre_10, beaumont_tiles, total_tools |
| buy_url | text | NULL | Direct link to product page |
| quantity | integer | NOT NULL, default 1 | |
| unit | text | NULL | each, sqm, lineal_m, litre, pack |
| sort_order | integer | NOT NULL, default 0 | Display order in pricing table |
| created_at | timestamptz | NOT NULL, default now() | |

### Table: subscriptions

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | uuid | PK, default gen_random_uuid() | |
| user_id | uuid | FK -> users.id, NOT NULL, UNIQUE | One active sub per user |
| tier | text | NOT NULL | 'pro' |
| status | text | NOT NULL, default 'active' | active, cancelled, expired |
| price_aud | numeric(10,2) | NOT NULL, default 9.95 | |
| current_period_start | timestamptz | NOT NULL | |
| current_period_end | timestamptz | NOT NULL | |
| cancel_at_period_end | boolean | NOT NULL, default false | |
| payment_provider | text | NULL | stripe, manual |
| payment_provider_id | text | NULL | External subscription ID |
| created_at | timestamptz | NOT NULL, default now() | |
| updated_at | timestamptz | NOT NULL, default now() | |
| deleted_at | timestamptz | NULL | Soft delete |

### Table: products (Static Product Catalogue - if Option B chosen)

| Column | Type | Constraints | Notes |
|--------|------|-------------|-------|
| id | uuid | PK, default gen_random_uuid() | |
| name | text | NOT NULL | |
| category | text | NOT NULL | paint, tile, fixture, hardware, timber, lighting, flooring, other |
| retailer | text | NOT NULL | bunnings, mitre_10, beaumont_tiles, total_tools |
| price_aud | numeric(10,2) | NOT NULL | |
| url | text | NULL | Product page URL |
| sku | text | NULL | Retailer SKU |
| unit | text | NULL | each, sqm, lineal_m, litre, pack |
| in_stock | boolean | NOT NULL, default true | |
| last_verified_at | timestamptz | NULL | When price was last checked |
| created_at | timestamptz | NOT NULL, default now() | |
| updated_at | timestamptz | NOT NULL, default now() | |

---

## Behavioural Rules

### Input Validation
- Description field: min 15 characters, max 500 characters
- If no room keyword detected in description, surface soft prompt asking which room
- Show dismissable tip card on input screen:
  - Describe the space
  - Mention materials you like
  - Note what to keep or remove
  - Add budget if known

### Output Format
- Before/after images displayed side by side
- Pricing table columns: Product Name | Est. Price (AUD) | Retailer | Buy Now
- Retailer priority order: Bunnings first, then Mitre 10, Beaumont Tiles, Total Tools

### Scan Gating
- Free tier: 3 scans per calendar month
- Pro tier: 20 scans per calendar month
- Gate triggers on submit (after auth, before AI processing)
- Scan count resets on the 1st of each month
- Reset logic: compare scan_reset_date to current month; if different, reset scans_used_this_month to 0 and update scan_reset_date

### Refused Projects
Surface a friendly message and do NOT process if the description indicates:
- Structural modifications
- Electrical work
- Gas fitting
- Plumbing behind walls
- Asbestos removal
- Any work requiring a licensed tradesperson in Australia

Message: "This project sounds like it may require a licensed professional. For your safety, we recommend contacting a qualified tradesperson for structural, electrical, gas, or plumbing work."

---

## User Flow

1. Homepage (hero + upload CTA)
2. Upload photo of space
3. Describe desired changes (free text + optional guided rails)
4. Click Continue
5. Sign in / sign up (Supabase auth)
6. AI pipeline runs: Gemini analyses photo -> GPT-Image-1 generates transformation
7. Output screen: before/after + itemised pricing table with buy links
8. Freemium gate enforced at step 6 (before AI processing)

---

## Directory Map

```
.
├── claude.md              # Project Constitution (this file)
├── task_plan.md           # BLAST phase checklist
├── findings.md            # Research, decisions, constraints
├── progress.md            # Action log
├── .env.example           # Required environment variables
├── architecture/          # Layer 1: SOPs
├── tools/                 # Layer 3: Utility scripts
└── .tmp/                  # Temporary workbench
```

---

## Status
- **Current Phase:** 1 - Blueprint
- **Blocking:** Awaiting user confirmation of this data schema
- **Decision Pending:** Pricing data approach (Option A: live scraping vs Option B: static database)

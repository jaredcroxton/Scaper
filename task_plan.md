# Task Plan - DIY Space Transformer

## Status: Phase 1 - Blueprint (Scaffolding)

---

## Phases

### Phase 0: Initialization
- [x] Create `task_plan.md`
- [x] Create `findings.md`
- [x] Create `progress.md`
- [x] Create `claude.md` (Project Constitution + Data Schema)
- [x] Create `architecture/` folder
- [x] Create `tools/` folder
- [x] Create `.tmp/` folder
- [x] Create `.env.example`
- [ ] Data schema confirmed by user

### Phase 1: Blueprint (Vision and Logic)
- [x] North Star defined
- [x] Integrations identified (Supabase, OpenAI, Gemini, Vercel)
- [x] Source of Truth established (Supabase)
- [x] Delivery Payload confirmed (web app with before/after + pricing table)
- [x] Behavioral Rules documented
- [x] Monetisation model defined (Free 3/month, Pro 20/month $9.95)
- [x] Refused project types listed
- [ ] Pricing data approach confirmed (Option A vs B)
- [ ] Schema approved

### Phase 2: Link (Connectivity)
- [ ] Supabase project created and credentials verified
- [ ] OpenAI API key tested (GPT-Image-1 access confirmed)
- [ ] Google Gemini API key tested
- [ ] Next.js project initialised
- [ ] Supabase tables created from schema
- [ ] Auth flow verified (sign up, sign in, session)
- [ ] Storage bucket created for photo uploads

### Phase 3: Architect (3-Layer Build)
- [ ] Architecture SOPs written
- [ ] Supabase schema migration script
- [ ] Photo upload and storage flow
- [ ] Gemini Vision analysis pipeline
- [ ] GPT-Image-1 transformation pipeline
- [ ] Pricing data layer (pending Option A/B decision)
- [ ] Scan count enforcement (free/pro gates)
- [ ] Subscription management (Stripe or manual)
- [ ] Output rendering (before/after + pricing table)

### Phase 4: Stylize (Refinement)
- [ ] Dark theme applied
- [ ] Mobile-first responsive layout
- [ ] Premium feel (typography, spacing, transitions)
- [ ] Tip card UI for description input
- [ ] Before/after side-by-side component
- [ ] Pricing table with Buy Now links
- [ ] Error states and refused-project messaging
- [ ] User feedback collected

### Phase 5: Trigger (Deployment)
- [ ] Vercel deployment configured
- [ ] Environment variables set in Vercel
- [ ] Supabase Row Level Security policies applied
- [ ] Domain connected
- [ ] Monitoring and error tracking
- [ ] Maintenance log finalised

---

## Notes
- No application code until schema is confirmed
- Single monolithic file pattern for page components
- No componentisation
- No em dashes anywhere including comments
- Soft delete only, never hard delete user records
- AUD pricing only

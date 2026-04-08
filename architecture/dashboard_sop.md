# SOP: Interactive Dashboard

## Goal
Display scraped articles in a gorgeous, interactive web dashboard with save functionality.

## Design System
- **Theme:** Light (white background)
- **Primary:** #2814FF (deep indigo)
- **Secondary:** #A537B4 (purple)
- **Accent:** #2814FF
- **Background:** #FFFFFF
- **Text Primary:** #1A1A1A
- **Link Color:** #6C757D
- **Font Primary:** Montserrat (headings)
- **Font Body:** Roboto
- **h1:** 48px, **h2:** 40px, **body:** 13px
- **Base Spacing Unit:** 4px
- **Border Radius:** 39px (pill-shaped)
- **Tone:** Professional, medium energy

## Layout (Inspired by Relatewise Dashboard)
- **Sidebar:** Collapsible nav with source filters
- **Header:** Search bar, stats overview
- **Main Area:** Article cards in responsive grid
- **Stats Bar:** Total articles, sources active, last updated
- **Card Design:** Clean white cards with subtle shadows, source badges, save button

## Features
1. **Article Cards:** Title, summary, source badge, timestamp, save button
2. **Source Filtering:** Filter by source (Reddit, Ben's Bites, Rundown AI)
3. **Search:** Real-time text search across titles and summaries
4. **Save Articles:** Click to save, persists in localStorage
5. **Saved View:** Toggle to show only saved articles
6. **Responsive:** Works on desktop and tablet
7. **Auto-refresh indicator:** Shows when data was last scraped

## Data Flow
- Dashboard reads `data/articles.json` via fetch
- Saved articles stored in `localStorage` under key `scaper_saved_articles`
- On page load: fetch articles, merge with saved state, render

## Technology
- Pure HTML/CSS/JS (no framework dependency)
- Google Fonts (Montserrat + Roboto)
- CSS Grid for layout, Flexbox for cards

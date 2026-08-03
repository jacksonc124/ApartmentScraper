# ApartmentScraper

Finds available 2bd/2ba apartments in **River North, Old Town, and Gold Coast**
(Chicago) for a commute to Willis Tower — free, small-scale, no paid APIs required.

## How it works

- **RentCast** (`scrapers/rentcast.py`) — the real data source. Free tier
  (50 calls/month). Does one lat/long+radius search per neighborhood (3 calls
  per run), since RentCast has no "neighborhood" field to filter on directly.
  Requires a free `RENTCAST_API_KEY` — nothing will show up without it.
- **Craigslist RSS** (`scrapers/craigslist.py`) — attempted but currently
  **non-functional**: Craigslist actively blocks this endpoint at the
  network level (confirmed 403 "Your request has been blocked," even from a
  real browser session, not just scripted requests). It's left in as
  best-effort — it fails silently and returns no results rather than
  crashing the run — in case that changes later, but don't rely on it.
- Commute time to Willis Tower is a hardcoded estimate per neighborhood
  (`config.py`) rather than a paid distance-matrix API call, since the search
  is locked to exactly three known areas.
- Results are stored in a local SQLite file (`data/listings.db`) and rendered
  to a static page (`static/index.html`) — no server, no hosting cost.

## Setup

```bash
pip install -r requirements.txt
cp .env.example .env
# add your free key from https://app.rentcast.io — required, see note above
```

## Run

```bash
python main.py
```

Open `static/index.html` in a browser to see current listings, sorted by price.

## Scheduling it for free

`.github/workflows/scrape.yml` runs the scraper Mondays and Thursdays via
GitHub Actions (free for public repos) — 6 RentCast calls/week, ~26/month,
safely under the 50/month free-tier cap — and publishes `static/index.html`
to GitHub Pages. To enable:

1. Push this repo to GitHub.
2. Repo Settings → Pages → set source to "GitHub Actions".
3. (Optional) Repo Settings → Secrets → add `RENTCAST_API_KEY`.

## Adjusting criteria

All search parameters live in `config.py`: target neighborhoods, bed/bath
counts, and commute estimates.

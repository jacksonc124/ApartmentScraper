"""Free, key-less source: Craigslist Chicago apartment search RSS feed."""

import hashlib
import re

import feedparser
import requests

from config import (
    BATHS_MIN,
    BEDS_REQUIRED,
    COMMUTE_TO_WILLIS_TOWER_MIN,
    CRAIGSLIST_RSS_URL,
    MAX_PRICE,
    NEIGHBORHOOD_KEYWORDS,
)

PRICE_RE = re.compile(r"\$([\d,]+)")
USER_AGENT = "Mozilla/5.0 (compatible; ApartmentScraper/1.0; personal use)"


def _match_neighborhood(text: str):
    text = text.lower()
    for neighborhood, keywords in NEIGHBORHOOD_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return neighborhood
    return None


def _make_id(url: str) -> str:
    return hashlib.sha1(url.encode()).hexdigest()[:16]


def fetch():
    """Return a list of listing dicts matching our neighborhoods, ready for storage.

    Best-effort only: Craigslist blocks scripted requests to this endpoint
    (confirmed 403 "Your request has been blocked" even with browser headers,
    from a real browser session). This silently returns [] on failure rather
    than crashing the whole run — RentCast is the reliable source.
    """
    url = CRAIGSLIST_RSS_URL.format(beds=BEDS_REQUIRED, baths_min=BATHS_MIN, max_price=MAX_PRICE)
    try:
        resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=20)
        resp.raise_for_status()
    except requests.RequestException as e:
        print(f"[craigslist] skipped, request blocked or failed: {e}")
        return []

    feed = feedparser.parse(resp.content)
    results = []

    for entry in feed.entries:
        title = getattr(entry, "title", "")
        summary = getattr(entry, "summary", "")
        combined = f"{title} {summary}"

        neighborhood = _match_neighborhood(combined)
        if not neighborhood:
            continue  # not one of our target neighborhoods

        price_match = PRICE_RE.search(title)
        price = int(price_match.group(1).replace(",", "")) if price_match else None

        commute = COMMUTE_TO_WILLIS_TOWER_MIN.get(neighborhood, {})

        results.append(
            {
                "id": _make_id(entry.link),
                "source": "craigslist",
                "title": title,
                "url": entry.link,
                "neighborhood": neighborhood,
                "price": price,
                "beds": BEDS_REQUIRED,
                "baths": None,  # Craigslist's title/RSS doesn't reliably state exact bath count
                "walk_min": commute.get("walk"),
                "transit_min": commute.get("transit"),
                "posted_at": getattr(entry, "published", None),
            }
        )

    return results

"""Optional supplemental source: RentCast API (free tier, 50 calls/month).

Requires RENTCAST_API_KEY env var. Skipped silently if not set, so the
scraper works out of the box with zero signup via Craigslist alone.
"""

import os
from urllib.parse import quote_plus

import requests

from config import (
    BATHS_MIN,
    BEDS_REQUIRED,
    COMMUTE_TO_WILLIS_TOWER_MIN,
    MAX_PRICE,
    NEIGHBORHOOD_GEO,
)

API_URL = "https://api.rentcast.io/v1/listings/rental/long-term"


def _listing_url(item: dict) -> str:
    """RentCast's response has no direct listing-page URL field (verified
    against their schema docs). Prefer the listing agent's own site if
    given; otherwise fall back to a Google search on the exact address,
    which reliably surfaces wherever the unit is actually syndicated
    (Zillow, Apartments.com, etc.)."""
    agent_site = (item.get("listingAgent") or {}).get("website")
    if agent_site:
        return agent_site
    address = item.get("formattedAddress", "")
    return f"https://www.google.com/search?q={quote_plus(address + ' apartment for rent')}"


def fetch():
    """One lat/long+radius call per neighborhood (3 calls/run for the
    current Old Town / Lakeview / Lincoln Park set).

    RentCast has no neighborhood field to filter on, so geo search is the
    only reliable way to target these areas specifically. At 3 calls/run,
    stay at run frequency <= weekly to remain comfortably under the free
    tier's 50 calls/month.
    """
    api_key = os.environ.get("RENTCAST_API_KEY")
    if not api_key:
        return []

    results = []
    for neighborhood, geo in NEIGHBORHOOD_GEO.items():
        resp = requests.get(
            API_URL,
            headers={"X-Api-Key": api_key},
            params={
                "latitude": geo["lat"],
                "longitude": geo["lon"],
                "radius": geo["radius"],
                "bedrooms": BEDS_REQUIRED,
                "bathrooms": f"{BATHS_MIN}:*",  # open-ended min range per RentCast's numeric range syntax
                "price": f"*:{MAX_PRICE}",  # open-ended max range, same syntax
                "status": "Active",
                "limit": 500,
            },
            timeout=20,
        )
        if resp.status_code != 200:
            print(f"[rentcast] {neighborhood} request failed: {resp.status_code} {resp.text[:200]}")
            continue

        commute = COMMUTE_TO_WILLIS_TOWER_MIN.get(neighborhood, {})
        for item in resp.json():
            results.append(
                {
                    "id": f"rentcast-{item.get('id')}",
                    "source": "rentcast",
                    "title": item.get("formattedAddress", ""),
                    "url": _listing_url(item),
                    "neighborhood": neighborhood,
                    "price": item.get("price"),
                    "beds": item.get("bedrooms"),
                    "baths": item.get("bathrooms"),
                    "walk_min": commute.get("walk"),
                    "transit_min": commute.get("transit"),
                    "posted_at": item.get("listedDate"),
                }
            )

    return results

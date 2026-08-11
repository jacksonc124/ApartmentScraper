"""Static configuration: target neighborhoods, search criteria, commute estimates."""

# "Loop and North" neighborhoods for this search
NEIGHBORHOODS = [
    "Old Town",
    "Lakeview",
    "Lincoln Park",
]

# Craigslist neighborhood/area query terms (used to filter listing titles/body)
NEIGHBORHOOD_KEYWORDS = {
    "Old Town": ["old town", "oldtown"],
    "Lakeview": ["lakeview", "lake view", "wrigleyville"],
    "Lincoln Park": ["lincoln park", "lincolnpark"],
}

# Approximate neighborhood centers + search radius (miles), used for RentCast's
# lat/long+radius search — RentCast has no "neighborhood" field, and street
# addresses don't contain neighborhood names, so geo search is the only way
# to target these areas specifically. Borders are fuzzy; tune radius if
# you're getting bleed into adjacent areas.
NEIGHBORHOOD_GEO = {
    "Old Town": {"lat": 41.9087, "lon": -87.6386, "radius": 0.5},
    "Lakeview": {"lat": 41.9403, "lon": -87.6538, "radius": 0.9},
    "Lincoln Park": {"lat": 41.9250, "lon": -87.6450, "radius": 0.8},
}

# Rough commute time (minutes, one-way) from neighborhood center to Willis Tower.
# Hardcoded instead of calling a paid distance-matrix API, since the search
# is locked to a fixed, known set of neighborhoods.
COMMUTE_TO_WILLIS_TOWER_MIN = {
    "Old Town": {"walk": 40, "transit": 20},
    "Lakeview": {"walk": 130, "transit": 32},
    "Lincoln Park": {"walk": 55, "transit": 25},
}

BEDS_REQUIRED = 2  # exact match
BATHS_MIN = 1  # 1 or more, not exact — see NEIGHBORHOOD_GEO's use of RentCast's open-ended range syntax
MAX_PRICE = 3200  # total monthly rent, not per-person

# Chicago Craigslist search RSS feed for apartments, filtered server-side
# where possible (bedrooms/price), neighborhood/bath filtering happens client-side.
CRAIGSLIST_RSS_URL = (
    "https://chicago.craigslist.org/search/apa"
    "?min_bedrooms={beds}"
    "&min_bathrooms={baths_min}"
    "&max_price={max_price}"
    "&availabilityMode=0"
    "&format=rss"
)

DB_PATH = "data/listings.db"
SITE_OUTPUT_PATH = "static/index.html"

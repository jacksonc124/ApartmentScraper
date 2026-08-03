"""Static configuration: target neighborhoods, search criteria, commute estimates."""

# "Loop and North" neighborhoods for this search
NEIGHBORHOODS = [
    "River North",
    "Old Town",
    "Gold Coast",
    "West Loop",
    "Streeterville",
    "Lincoln Park",
]

# Craigslist neighborhood/area query terms (used to filter listing titles/body)
NEIGHBORHOOD_KEYWORDS = {
    "River North": ["river north", "rivernorth", "river-north"],
    "Old Town": ["old town", "oldtown"],
    "Gold Coast": ["gold coast", "goldcoast"],
    "West Loop": ["west loop", "westloop", "fulton market"],
    "Streeterville": ["streeterville"],
    "Lincoln Park": ["lincoln park", "lincolnpark"],
}

# Approximate neighborhood centers + search radius (miles), used for RentCast's
# lat/long+radius search — RentCast has no "neighborhood" field, and street
# addresses don't contain neighborhood names, so geo search is the only way
# to target these areas specifically. Borders are fuzzy; tune radius if
# you're getting bleed into adjacent areas.
NEIGHBORHOOD_GEO = {
    "River North": {"lat": 41.8925, "lon": -87.6350, "radius": 0.6},
    "Old Town": {"lat": 41.9087, "lon": -87.6386, "radius": 0.5},
    "Gold Coast": {"lat": 41.9048, "lon": -87.6263, "radius": 0.5},
    "West Loop": {"lat": 41.8825, "lon": -87.6510, "radius": 0.7},
    "Streeterville": {"lat": 41.8925, "lon": -87.6220, "radius": 0.4},
    "Lincoln Park": {"lat": 41.9250, "lon": -87.6450, "radius": 0.8},
}

# Rough commute time (minutes, one-way) from neighborhood center to Willis Tower.
# Hardcoded instead of calling a paid distance-matrix API, since the search
# is locked to a fixed, known set of neighborhoods.
COMMUTE_TO_WILLIS_TOWER_MIN = {
    "River North": {"walk": 25, "transit": 12},
    "Old Town": {"walk": 40, "transit": 20},
    "Gold Coast": {"walk": 35, "transit": 18},
    "West Loop": {"walk": 15, "transit": 8},
    "Streeterville": {"walk": 30, "transit": 15},
    "Lincoln Park": {"walk": 55, "transit": 25},
}

BEDS_REQUIRED = 2
BATHS_REQUIRED = 2

# Chicago Craigslist search RSS feed for apartments, filtered server-side
# where possible (bedrooms), neighborhood/bath filtering happens client-side.
CRAIGSLIST_RSS_URL = (
    "https://chicago.craigslist.org/search/apa"
    "?min_bedrooms={beds}"
    "&min_bathrooms={baths}"
    "&availabilityMode=0"
    "&format=rss"
)

DB_PATH = "data/listings.db"
SITE_OUTPUT_PATH = "static/index.html"

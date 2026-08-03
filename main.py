"""Run all scrapers, store results, regenerate the static site."""

from generate_site import generate
from scrapers import craigslist, rentcast
from storage import get_db, upsert_listing


def run():
    listings = []
    listings += craigslist.fetch()
    listings += rentcast.fetch()

    with get_db() as conn:
        for listing in listings:
            upsert_listing(conn, listing)

    generate()
    print(f"Stored/updated {len(listings)} listings. Site regenerated at static/index.html")


if __name__ == "__main__":
    run()

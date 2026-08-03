"""Run all scrapers, store results, regenerate the static site."""

from dotenv import load_dotenv

load_dotenv()

from generate_site import generate
from scrapers import craigslist, rentcast
from storage import get_db, prune_missing, upsert_listing


def run():
    listings = []
    listings += craigslist.fetch()
    listings += rentcast.fetch()

    unique_ids = {listing["id"] for listing in listings}
    with get_db() as conn:
        for listing in listings:
            upsert_listing(conn, listing)
        prune_missing(conn, unique_ids)

    generate()
    print(f"Stored {len(unique_ids)} unique listings. Site regenerated at static/index.html")


if __name__ == "__main__":
    run()

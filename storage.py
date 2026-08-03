import sqlite3
from contextlib import contextmanager

from config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS listings (
    id TEXT PRIMARY KEY,
    source TEXT NOT NULL,
    title TEXT NOT NULL,
    url TEXT NOT NULL,
    neighborhood TEXT,
    price INTEGER,
    beds REAL,
    baths REAL,
    walk_min INTEGER,
    transit_min INTEGER,
    posted_at TEXT,
    first_seen TEXT DEFAULT CURRENT_TIMESTAMP,
    last_seen TEXT DEFAULT CURRENT_TIMESTAMP
);
"""


@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute(SCHEMA)
        yield conn
        conn.commit()
    finally:
        conn.close()


def upsert_listing(conn, listing: dict):
    existing = conn.execute(
        "SELECT id FROM listings WHERE id = ?", (listing["id"],)
    ).fetchone()
    if existing:
        conn.execute(
            """UPDATE listings SET price=?, title=?, last_seen=CURRENT_TIMESTAMP
               WHERE id=?""",
            (listing["price"], listing["title"], listing["id"]),
        )
    else:
        conn.execute(
            """INSERT INTO listings
               (id, source, title, url, neighborhood, price, beds, baths,
                walk_min, transit_min, posted_at)
               VALUES (:id, :source, :title, :url, :neighborhood, :price,
                       :beds, :baths, :walk_min, :transit_min, :posted_at)""",
            listing,
        )


def all_listings(conn):
    return conn.execute(
        "SELECT * FROM listings ORDER BY price ASC"
    ).fetchall()

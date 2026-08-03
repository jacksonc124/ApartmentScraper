"""Builds a static HTML page from the SQLite listings table. No server needed."""

import os
from datetime import datetime, timezone

from config import NEIGHBORHOODS, SITE_OUTPUT_PATH
from storage import all_listings, get_db

ROW_TEMPLATE = """
<tr>
  <td>{neighborhood}</td>
  <td>${price}</td>
  <td>{beds}bd / {baths}ba</td>
  <td>{walk_min} min walk / {transit_min} min transit to Willis Tower</td>
  <td>{source}</td>
  <td><a href="{url}" target="_blank" rel="noopener">view listing</a></td>
</tr>
"""

PAGE_TEMPLATE = """<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>ApartmentScraper — {neighborhood_list}</title>
<style>
  body {{ font-family: system-ui, sans-serif; margin: 2rem; background: #111; color: #eee; }}
  h1 {{ font-size: 1.4rem; }}
  table {{ border-collapse: collapse; width: 100%; }}
  th, td {{ text-align: left; padding: 0.5rem 0.75rem; border-bottom: 1px solid #333; }}
  th {{ cursor: pointer; color: #9cf; }}
  a {{ color: #9cf; }}
  .meta {{ color: #888; font-size: 0.85rem; margin-bottom: 1rem; }}
</style>
</head>
<body>
<h1>2bd/2ba — {neighborhood_list}</h1>
<div class="meta">{count} listings · last updated {updated}</div>
<table>
<thead>
<tr><th>Neighborhood</th><th>Price</th><th>Beds/Baths</th><th>Commute to Willis Tower</th><th>Source</th><th>Link</th></tr>
</thead>
<tbody>
{rows}
</tbody>
</table>
</body>
</html>
"""


def generate():
    with get_db() as conn:
        rows = all_listings(conn)

    rows_html = "\n".join(
        ROW_TEMPLATE.format(
            neighborhood=r["neighborhood"] or "?",
            price=r["price"] if r["price"] is not None else "?",
            beds=r["beds"] if r["beds"] is not None else "?",
            baths=r["baths"] if r["baths"] is not None else "?",
            walk_min=r["walk_min"] if r["walk_min"] is not None else "?",
            transit_min=r["transit_min"] if r["transit_min"] is not None else "?",
            source=r["source"],
            url=r["url"],
        )
        for r in rows
    )

    html = PAGE_TEMPLATE.format(
        neighborhood_list=" / ".join(NEIGHBORHOODS),
        count=len(rows),
        updated=datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        rows=rows_html or "<tr><td colspan='6'>No listings yet — run main.py</td></tr>",
    )

    os.makedirs(os.path.dirname(SITE_OUTPUT_PATH), exist_ok=True)
    with open(SITE_OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html)


if __name__ == "__main__":
    generate()

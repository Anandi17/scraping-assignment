"""Basic schema and value checks."""
from urllib.parse import urlparse
VALID_SOURCES = {"Books to Scrape", "Quotes to Scrape"}

def validate_record(rec):
    problems = []
    if rec.get("source") not in VALID_SOURCES: problems.append("unknown_source")
    if not rec.get("name_or_title"): problems.append("missing_name")
    url = urlparse(str(rec.get("source_url") or ""))
    if url.scheme not in ("http", "https") or not url.netloc: problems.append("invalid_url")
    price = rec.get("price")
    if price is not None and (not isinstance(price, (int, float)) or price < 0): problems.append("invalid_price")
    rating = rec.get("rating")
    if rating is not None and (not isinstance(rating, int) or rating not in range(1, 6)): problems.append("invalid_rating")
    if rec.get("source") == "Quotes to Scrape" and not rec.get("author"): problems.append("missing_author")
    return problems

"""Pure data-cleaning helpers."""
import re
from urllib.parse import urlparse

RATING_MAP = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}

def clean_text(value):
    if value is None: return None
    result = " ".join(str(value).replace("\xa0", " ").split())
    return result or None

def clean_price(value):
    if value is None or not str(value).strip(): return None
    match = re.search(r"\d+(?:,\d{3})*(?:\.\d+)?", str(value).replace(",", ""))
    return float(match.group()) if match else None

def clean_rating(value):
    if value is None: return None
    for part in str(value).lower().split():
        if part in RATING_MAP: return RATING_MAP[part]
    try:
        number = int(value)
        return number if 1 <= number <= 5 else None
    except (TypeError, ValueError):
        return None

def clean_tags(value):
    if not value: return None
    values = value if isinstance(value, (list, tuple, set)) else str(value).split(";")
    cleaned = sorted({text.lower() for item in values if (text := clean_text(item))})
    return ";".join(cleaned) if cleaned else None

def normalize_url(value):
    value = clean_text(value)
    if not value: return None
    parsed = urlparse(value)
    return value if parsed.scheme in ("http", "https") and parsed.netloc else None

def clean_record(raw, scraped_at):
    return {"source": clean_text(raw.get("source")),
            "source_url": normalize_url(raw.get("source_url")),
            "name_or_title": clean_text(raw.get("name_or_title")),
            "category": clean_text(raw.get("category")),
            "price": clean_price(raw.get("price")),
            "rating": clean_rating(raw.get("rating")),
            "author": clean_text(raw.get("author")),
            "tags": clean_tags(raw.get("tags")),
            "description": clean_text(raw.get("description")),
            "scraped_at": scraped_at}

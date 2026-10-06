"""Stable, source-specific duplicate fingerprints."""
import hashlib
import re

def _normalize(value):
    value = (value or "").lower()
    value = re.sub(r"[^\w\s]", "", value, flags=re.UNICODE)
    return " ".join(value.split())

def make_fingerprint(rec):
    source = rec.get("source", "")
    if source == "Books to Scrape":
        key = f"{source} {_normalize(rec.get('name_or_title'))}"
    else:
        key = f"{source} {_normalize(rec.get('author'))} {_normalize(rec.get('name_or_title'))[:50]}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()

def find_duplicates(records):
    seen, unique, duplicates = set(), [], []
    for rec in records:
        fingerprint = make_fingerprint(rec)
        if fingerprint in seen: duplicates.append(rec)
        else: unique.append(rec)
        seen.add(fingerprint)
    return unique, duplicates

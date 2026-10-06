"""Run the complete two-source scraping and consolidation pipeline."""
import csv
import json
import logging
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from processing.cleaning import clean_record
from processing.validation import validate_record
from processing.deduplication import find_duplicates
from scrapers.books_scraper import BooksScraper
from scrapers.quotes_scraper import QuotesScraper

ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "output"
LOGS = ROOT / "logs"
FIELDS = ["source", "source_url", "name_or_title", "category", "price", "rating", "author", "tags", "description", "scraped_at"]

def configure_logging():
    LOGS.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[logging.FileHandler(LOGS / "scraper.log", encoding="utf-8"), logging.StreamHandler()],
        force=True)

def run():
    configure_logging()
    logger = logging.getLogger("pipeline")
    started_clock = time.monotonic()
    started_at = datetime.now(timezone.utc)
    raw_by_source = {}
    for name, cls in (("Books to Scrape", BooksScraper), ("Quotes to Scrape", QuotesScraper)):
        scraper = cls()
        try:
            raw_by_source[name] = scraper.scrape()
        except Exception:
            logger.exception("Unexpected failure scraping %s", name)
            raw_by_source[name] = []
        finally:
            scraper.close()

    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    valid, rejected = [], Counter()
    cleaned_by_source = Counter()
    for source, raw_records in raw_by_source.items():
        for raw in raw_records:
            try:
                rec = clean_record(raw, stamp)
                cleaned_by_source[source] += 1
                problems = validate_record(rec)
                if problems:
                    for problem in problems: rejected[problem] += 1
                    logger.warning("Rejected record from %s: %s", source, ",".join(problems))
                else: valid.append(rec)
            except Exception:
                rejected["processing_error"] += 1
                logger.exception("Record processing failed for %s", source)
    unique, duplicates = find_duplicates(valid)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    with (OUTPUT / "final_dataset.csv").open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(unique)
    ended_at = datetime.now(timezone.utc)
    summary = {
        "started_at": started_at.isoformat(timespec="seconds"),
        "ended_at": ended_at.isoformat(timespec="seconds"),
        "duration_seconds": round(time.monotonic() - started_clock, 3),
        "collected_per_source": {name: len(raw_by_source.get(name, [])) for name in ("Books to Scrape", "Quotes to Scrape")},
        "cleaned_per_source": {name: cleaned_by_source[name] for name in ("Books to Scrape", "Quotes to Scrape")},
        "rejected_by_reason": dict(sorted(rejected.items())),
        "duplicates_detected_and_removed": len(duplicates),
        "final_record_count": len(unique),
        "outputs": {"dataset": "output/final_dataset.csv", "summary": "output/summary_report.json", "log": "logs/scraper.log"},
    }
    with (OUTPUT / "summary_report.json").open("w", encoding="utf-8") as handle:
        json.dump(summary, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
    logger.info("Finished: %d valid unique records; %d duplicates removed", len(unique), len(duplicates))
    return summary

if __name__ == "__main__":
    run()

# Multi-source web scraping and data consolidation

A small, reproducible Python ETL project that scrapes the public Books to Scrape and Quotes to Scrape practice sites, cleans and validates their records, removes duplicates, and writes a shared CSV plus a JSON run summary.

## Requirements and setup

- Python 3.10–3.12 and an internet connection.
- Windows PowerShell:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

On macOS/Linux, activate with `source .venv/bin/activate`. To run the offline unit tests, use `python -m pytest`.\n\nTo publish with GitHub, create an empty repository on GitHub, then open this folder in VS Code, use Source Control to initialize Git, commit the project, add the repository URL as `origin`, and push the `main` branch. Do not commit `.venv`; it is excluded by `.gitignore`.

## Project structure

`scrapers/` contains the shared HTTP helper and one source scraper per site. `processing/` contains pure cleaning, validation, and deduplication logic. `main.py` runs the pipeline. Generated data goes to `output/`; logs go to `logs/`; unit tests are in `tests/`.

## Source observations and pagination

Books use `article.product_pod`; the full title is in `h3 > a[title]`, price in `p.price_color`, rating in the `p.star-rating` class, and the product detail URL in the link. Quotes use `div.quote`, `span.text`, `small.author`, and `a.tag`. Both sites expose `li.next > a`. Each scraper resolves that relative link against the current page and continues until no next link exists, tracking visited URLs to avoid loops. No page count is hard-coded.

The common CSV schema is `source`, `source_url`, `name_or_title`, `category`, `price`, `rating`, `author`, `tags`, `description`, and `scraped_at`. Book category and description are left empty because listing pages do not provide them; quote price, rating, category, and description are empty. For quotes, `source_url` is the listing page where the quote appeared. Timestamps are UTC ISO-8601 strings. Empty optional fields are blank in the CSV.

## Cleaning, validation, and duplicate rules

Cleaning collapses whitespace (including non-breaking spaces), converts currency strings to numeric prices, maps star words to integers 1–5, sorts and lowercases tags, and only accepts absolute HTTP(S) URLs. Validation requires a recognized source, a title/text value, and a valid URL; it checks nonnegative numeric prices, integer ratings 1–5, and a quote author. Invalid records are counted by reason and logged.

Books are identified by source plus title; quote records by source, author, and the first 50 normalized characters of quote text. Fingerprints lowercase text, remove punctuation, collapse whitespace, then hash it. Repeated records are removed, with their count reported. Source is part of the key, so different source types do not collide.

## Reliability and outputs

Requests use a descriptive User-Agent, a 15-second timeout, up to three retries for temporary HTTP/network errors (including 429 and common 5xx responses), and a 0.5-second pause between requests. Individual malformed records are skipped; an exhausted page request stops that source while allowing the other source and the rest of the pipeline to continue.

- `output/final_dataset.csv`: one row per valid unique record.
- `output/summary_report.json`: times, raw/cleaned counts per source, rejection counts, removed duplicates, and final count.
- `logs/scraper.log`: timestamped request progress, warnings, and errors.

The count relationship is `valid before deduplication - duplicates removed = final_record_count`; rejected records are reported separately and are not included in the deduplication input.

## Assumptions and limitations

The project uses only the two public practice sites and their visible listing pages. It does not fetch the approximately 1,000 book detail pages, so category and description are not collected. A page that remains unavailable after retries ends collection for that source; the report reflects records successfully gathered before that failure. The websites can change their HTML, requiring selector updates. The current data files are the result of the included run; regenerate them with `python main.py`.

## AI usage

See [AI_USAGE.md](AI_USAGE.md) for the tool disclosure, representative prompt, review notes, and verification details.


## Included run status

The included unit tests passed (7 tests). A live scrape was attempted, but this execution environment could not establish a trusted TLS connection to either practice site. The generated CSV therefore contains only its header and the report records zero collected records. Run python main.py from an internet-connected environment with working certificate trust to generate the actual dataset before submitting the assignment.


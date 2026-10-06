from processing.validation import validate_record

def test_valid_book():
    rec = {"source":"Books to Scrape", "source_url":"https://books.toscrape.com/a", "name_or_title":"A book", "price":1.25, "rating":3}
    assert validate_record(rec) == []

def test_invalid_fields_are_reported():
    rec = {"source":"Other", "source_url":"bad", "name_or_title":"", "price":-1, "rating":8}
    assert set(validate_record(rec)) == {"unknown_source", "missing_name", "invalid_url", "invalid_price", "invalid_rating"}

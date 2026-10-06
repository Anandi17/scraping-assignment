from processing.cleaning import clean_text, clean_price, clean_rating, clean_tags, normalize_url

def test_clean_text_and_nbsp():
    assert clean_text("  Hello\n  World\xa0 ") == "Hello World"

def test_price_and_rating():
    assert clean_price("£51.77") == 51.77
    assert clean_rating("star-rating Three") == 3

def test_tags_and_url():
    assert clean_tags(["Science", " art ", "science"]) == "art;science"
    assert normalize_url("https://example.com/a") == "https://example.com/a"
    assert normalize_url("/relative") is None

from processing.deduplication import find_duplicates

def test_books_duplicates_ignore_case_and_spaces():
    base = {"source":"Books to Scrape", "source_url":"https://books.toscrape.com", "price":1}
    records = [{**base, "name_or_title":"Example Book Title"}, {**base, "name_or_title":" EXAMPLE   BOOK TITLE "}]
    unique, duplicates = find_duplicates(records)
    assert len(unique) == 1 and len(duplicates) == 1

def test_quotes_identify_by_author_and_text_prefix():
    base = {"source":"Quotes to Scrape", "author":"A. Person"}
    unique, duplicates = find_duplicates([{**base,"name_or_title":"A quote!"},{**base,"name_or_title":"A QUOTE"}])
    assert len(unique) == 1 and len(duplicates) == 1

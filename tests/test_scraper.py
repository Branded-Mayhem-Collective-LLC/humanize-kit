import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from engine.scraper import scrape_url, is_available

def test_is_available_returns_bool():
    assert isinstance(is_available(), bool)

def test_scrape_url_returns_string_or_none():
    if not is_available():
        return
    result = scrape_url('https://example.com')
    assert result is None or isinstance(result, str)

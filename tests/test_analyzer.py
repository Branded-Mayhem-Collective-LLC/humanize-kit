import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from engine.analyzer import analyze_punctuation

def test_punctuation_counts_em_dashes():
    text = "This is a test \u2014 with em dashes \u2014 and more text."
    result = analyze_punctuation(text)
    assert result['em_dash'] == 2

def test_punctuation_counts_hyphens_as_dashes():
    text = "This is a test - with hyphens - used as dashes."
    result = analyze_punctuation(text)
    assert result['hyphen_dash'] == 2

def test_punctuation_counts_parentheses():
    text = "This (has) parenthetical (asides) in it."
    result = analyze_punctuation(text)
    assert result['parentheses'] == 2

def test_punctuation_counts_ellipsis():
    text = "Trailing off... and then again... and done."
    result = analyze_punctuation(text)
    assert result['ellipsis'] == 2

def test_punctuation_ratios():
    text = "Test - one. Test - two. Test \u2014 three."
    result = analyze_punctuation(text)
    assert result['hyphen_dash'] == 2
    assert result['em_dash'] == 1
    assert result['ratios']['hyphen_to_emdash'] == 2.0

def test_punctuation_zero_emdash_ratio():
    text = "Test - one. Test - two. No em dashes here."
    result = analyze_punctuation(text)
    assert result['ratios']['hyphen_to_emdash'] == float('inf')

def test_suggested_max_emdash():
    text = "A - b. C - d. E - f. G - h. Only one \u2014 here."
    result = analyze_punctuation(text)
    assert result['suggested_max_emdash'] <= 2

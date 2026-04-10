import re
from collections import Counter
from statistics import mean, stdev


def analyze_punctuation(text: str) -> dict:
    """
    Counts punctuation devices in text and calculates ratios.

    Returns a dict with:
    - em_dash: count of Unicode em dashes (U+2014)
    - hyphen_dash: count of hyphens used as dashes (space-hyphen-space)
    - parentheses: count of matched parenthetical pairs (...)
    - ellipsis: count of ellipsis sequences (...)
    - colons: count of colons
    - semicolons: count of semicolons
    - total_devices: sum of all above
    - ratios: dict with hyphen_to_emdash (float or inf)
    - suggested_max_emdash: int recommendation
    """
    em_dash = len(re.findall(r'\u2014', text))
    hyphen_dash = len(re.findall(r' - ', text))
    parentheses = len(re.findall(r'\([^)]+\)', text))
    ellipsis = len(re.findall(r'\.\.\.', text))
    colons = len(re.findall(r':', text))
    semicolons = len(re.findall(r';', text))

    total_devices = em_dash + hyphen_dash + parentheses + ellipsis + colons + semicolons

    if em_dash == 0:
        hyphen_to_emdash = float('inf')
    else:
        hyphen_to_emdash = hyphen_dash / em_dash

    if em_dash == 0 or hyphen_to_emdash > 3:
        suggested_max_emdash = 0
    elif hyphen_to_emdash > 1.5:
        suggested_max_emdash = 2
    else:
        suggested_max_emdash = 3

    return {
        'em_dash': em_dash,
        'hyphen_dash': hyphen_dash,
        'parentheses': parentheses,
        'ellipsis': ellipsis,
        'colons': colons,
        'semicolons': semicolons,
        'total_devices': total_devices,
        'ratios': {
            'hyphen_to_emdash': hyphen_to_emdash,
        },
        'suggested_max_emdash': suggested_max_emdash,
    }


def _split_sentences(text: str) -> list:
    """Split text on .!? delimiters, strip whitespace, filter empty strings."""
    parts = re.split(r'[.!?]+', text)
    return [s.strip() for s in parts if s.strip()]


def analyze_rhythm(text: str) -> dict:
    """
    Analyze sentence rhythm characteristics of the given text.

    Returns a dict with:
    - lengths: list of word counts per sentence
    - mean: average sentence length (rounded to 1 decimal)
    - stdev: standard deviation (rounded to 1 decimal, 0 if only 1 sentence)
    - min: shortest sentence length
    - max: longest sentence length
    - fragment_rate: ratio of sentences with 4 or fewer words
    - conjunction_starters: count of sentences starting with And/But/Or/So/Yet
    - count: total sentence count
    """
    conjunctions = {'and', 'but', 'or', 'so', 'yet'}

    sentences = _split_sentences(text)

    if not sentences:
        return {
            'lengths': [],
            'mean': 0,
            'stdev': 0,
            'min': 0,
            'max': 0,
            'fragment_rate': 0,
            'conjunction_starters': 0,
            'count': 0,
        }

    lengths = [len(s.split()) for s in sentences]
    sentence_mean = round(mean(lengths), 1)
    sentence_stdev = round(stdev(lengths), 1) if len(lengths) > 1 else 0
    sentence_min = min(lengths)
    sentence_max = max(lengths)
    fragment_rate = sum(1 for l in lengths if l <= 4) / len(lengths)
    conjunction_starters = sum(
        1 for s in sentences
        if s.split() and s.split()[0].lower() in conjunctions
    )

    return {
        'lengths': lengths,
        'mean': sentence_mean,
        'stdev': sentence_stdev,
        'min': sentence_min,
        'max': sentence_max,
        'fragment_rate': fragment_rate,
        'conjunction_starters': conjunction_starters,
        'count': len(sentences),
    }

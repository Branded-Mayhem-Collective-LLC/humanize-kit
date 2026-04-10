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

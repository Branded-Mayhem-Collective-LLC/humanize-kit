import re
from collections import Counter
from statistics import mean, stdev


STOPWORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
    'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
    'could', 'should', 'may', 'might', 'shall', 'can', 'this', 'that',
    'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me',
    'him', 'her', 'us', 'them', 'my', 'your', 'his', 'its', 'our', 'their',
    'what', 'which', 'who', 'whom', 'when', 'where', 'why', 'how', 'not',
    'no', 'so', 'if', 'then', 'than', 'too', 'very', 'just', 'about', 'up',
    'out', 'all', 'also', 'as', 'into', 'over', 'after', 'before', 'between',
    'through', 'during', 'without', 'again', 'there', 'here', 'more', 'some',
    'such', 'only', 'other', 'new', 'now', 'any', 'each', 'much', 'own',
    'same', 'even', 'most', 'many', 'well', 'back', 'still',
}

AI_BLACKLIST = {
    'leverage', 'synergy', 'paradigm', 'disrupt', 'ecosystem', 'furthermore',
    'additionally', 'moreover', 'robust', 'streamline', 'cutting-edge',
    'game-changer', 'unlock', 'empower', 'harness',
    'delve', 'crucial', 'pivotal', 'testament', 'tapestry', 'vibrant',
    'meticulous', 'meticulously', 'bolstered', 'garner', 'enduring',
    'intricate', 'intricacies', 'interplay', 'showcase', 'showcasing',
    'enhance', 'enhancing', 'fostering', 'highlighting', 'valuable',
    'nestled', 'groundbreaking', 'renowned', 'profound', 'exemplifies',
    'navigating', 'landscape', 'holistic', 'comprehensive',
    'serves as', 'stands as', 'features',
    'emphasizing',
}


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


def analyze_vocabulary(text: str) -> dict:
    """
    Analyze vocabulary signature of the given text.

    Returns a dict with:
    - top_words: list of (word, count) tuples, top 25 content words
                 (excluding stopwords, min length 3), sorted by frequency desc
    - whitelisted: sorted list of AI blacklist words the user uses 2+ times
    - never_use: sorted AI blacklist minus whitelisted words
    - unique_count: count of unique content words
    - total_count: total content word tokens
    """
    # Extract lowercase words only (alpha characters)
    raw_words = re.findall(r"[a-z]+(?:-[a-z]+)*", text.lower())

    # Filter to content words: not stopwords, min length 3
    content_words = [w for w in raw_words if w not in STOPWORDS and len(w) >= 3]

    counts = Counter(content_words)

    # Top 25 by frequency
    top_words = counts.most_common(25)

    # Words used 2+ times that appear in the AI blacklist
    whitelisted = sorted(
        word for word, cnt in counts.items()
        if cnt >= 2 and word in AI_BLACKLIST
    )

    # AI blacklist minus whitelisted words
    never_use = sorted(AI_BLACKLIST - set(whitelisted))

    return {
        'top_words': top_words,
        'whitelisted': whitelisted,
        'never_use': never_use,
        'unique_count': len(counts),
        'total_count': sum(counts.values()),
    }

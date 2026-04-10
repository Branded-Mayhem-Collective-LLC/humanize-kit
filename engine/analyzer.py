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


FORMAL_WORDS = {
    'therefore', 'however', 'consequently', 'furthermore', 'moreover',
    'nevertheless', 'notwithstanding', 'whereas', 'hereby', 'thereof',
    'pursuant', 'accordingly', 'henceforth', 'subsequently', 'utilize',
    'facilitate', 'implement', 'comprehensive', 'demonstrate', 'indicate',
}


def analyze_structure(text: str) -> dict:
    """
    Analyze paragraph-level structure of the given text.

    Returns a dict with:
    - paragraph_count: number of paragraphs (split on double newlines)
    - avg_paragraph_sentences: mean sentence count across paragraphs
    - paragraph_variance: stdev of sentence counts (0 if only 1 paragraph)
    - list_ratio: ratio of paragraphs starting with -, *, or a digit
    """
    paragraphs = [p.strip() for p in re.split(r'\n\n+', text) if p.strip()]
    paragraph_count = len(paragraphs)

    if paragraph_count == 0:
        return {
            'paragraph_count': 0,
            'avg_paragraph_sentences': 0,
            'paragraph_variance': 0,
            'list_ratio': 0,
        }

    sentence_counts = [len(_split_sentences(p)) for p in paragraphs]
    avg_paragraph_sentences = mean(sentence_counts)
    paragraph_variance = stdev(sentence_counts) if paragraph_count > 1 else 0

    list_paragraphs = sum(
        1 for p in paragraphs
        if re.match(r'^[-*]|\d', p)
    )
    list_ratio = list_paragraphs / paragraph_count

    return {
        'paragraph_count': paragraph_count,
        'avg_paragraph_sentences': avg_paragraph_sentences,
        'paragraph_variance': paragraph_variance,
        'list_ratio': list_ratio,
    }


def _classify_sentence(sentence: str) -> str:
    """
    Classify a sentence into one of five types:
    - 'question': ends with ?
    - 'fragment': 4 or fewer words
    - 'personal': starts with I/We/My/Our
    - 'story_hook': starts with Once/When/Last/Yesterday/Two/Three
    - 'declaration': default
    """
    stripped = sentence.strip()
    if stripped.endswith('?'):
        return 'question'
    words = stripped.split()
    if len(words) <= 4:
        return 'fragment'
    first = words[0] if words else ''
    if first in ('I', 'We', 'My', 'Our'):
        return 'personal'
    if first in ('Once', 'When', 'Last', 'Yesterday', 'Two', 'Three'):
        return 'story_hook'
    return 'declaration'


def _split_sentences_with_punct(text: str) -> list:
    """Split text into sentences, preserving trailing punctuation on each."""
    parts = re.split(r'(?<=[.!?])\s+', text.strip())
    return [p.strip() for p in parts if p.strip()]


def analyze_openings_closings(samples: list) -> dict:
    """
    Analyze the opening and closing sentences of a list of text samples.

    Returns:
    - openings: list of {'type': str, 'text': str[:80]} for first sentence of each sample
    - closings: list of {'type': str, 'text': str[:80]} for last sentence of each sample
    """
    openings = []
    closings = []

    for sample in samples:
        sentences = _split_sentences_with_punct(sample)
        if not sentences:
            continue
        first = sentences[0]
        last = sentences[-1]
        openings.append({'type': _classify_sentence(first), 'text': first[:80]})
        closings.append({'type': _classify_sentence(last), 'text': last[:80]})

    return {'openings': openings, 'closings': closings}


def analyze_register(text: str) -> dict:
    """
    Analyze the register (formality level) of the given text.

    Returns:
    - formality_score: ratio of formal words to total words (rounded to 4 decimal)
    - has_contractions: bool — presence of contractions (n't, 're, 've, 'll, 'm, 's)
    - has_fragments: bool — presence of short word sequences followed by a period
    """
    words = re.findall(r"[a-z]+(?:'[a-z]+)*", text.lower())
    total_words = len(words)
    formal_count = sum(1 for w in words if w in FORMAL_WORDS)
    formality_score = round(formal_count / total_words, 4) if total_words > 0 else 0.0

    has_contractions = bool(re.search(r"n't|'re|'ve|'ll|'m|'s", text))
    has_fragments = bool(re.search(r'\b\w{1,4}\b\.', text))

    return {
        'formality_score': formality_score,
        'has_contractions': has_contractions,
        'has_fragments': has_fragments,
    }


def detect_sign_off(samples: list) -> str | None:
    """
    Detect a consistent sign-off pattern across a list of text samples.

    Checks for:
    - Pattern `\\n[-–—] Name` at the end of samples
    - Closing salutations like "Best,", "Thanks,", etc.

    Returns the sign-off string (normalised to "- Name") if it appears in 40%+
    of samples, otherwise None.
    """
    if not samples:
        return None

    threshold = 0.4 * len(samples)
    sign_off_counts: Counter = Counter()

    dash_pattern = re.compile(r'\n[-\u2013\u2014]\s*(\S+)\s*$')
    salutation_pattern = re.compile(r'\b(Best|Thanks|Regards|Cheers|Sincerely),\s*\S+\s*$')

    for sample in samples:
        m = dash_pattern.search(sample)
        if m:
            sign_off_counts[f'- {m.group(1)}'] += 1
            continue
        m2 = salutation_pattern.search(sample)
        if m2:
            sign_off_counts[m2.group(0).strip()] += 1

    for sign_off, count in sign_off_counts.most_common():
        if count >= threshold:
            return sign_off

    return None


def build_profile(samples: list) -> dict:
    """
    Compose all analyzers into a single voice profile dict.

    Returns a dict containing results from all sub-analyzers plus
    metadata about the sample set.
    """
    combined_text = '\n\n'.join(samples)
    return {
        'punctuation': analyze_punctuation(combined_text),
        'rhythm': analyze_rhythm(combined_text),
        'vocabulary': analyze_vocabulary(combined_text),
        'structure': analyze_structure(combined_text),
        'register': analyze_register(combined_text),
        'openings_closings': analyze_openings_closings(samples),
        'sign_off': detect_sign_off(samples),
        'samples_used': len(samples),
        'total_words': len(combined_text.split()),
    }

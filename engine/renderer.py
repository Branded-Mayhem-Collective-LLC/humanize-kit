import re
from pathlib import Path
from collections import Counter

TEMPLATE_DIR = Path(__file__).parent / 'templates'


def render_skill(template_text: str, profile_data: dict) -> str:
    """Replace {{placeholders}} in template with values from profile_data.
    Unknown placeholders are left as-is."""
    def replacer(match):
        key = match.group(1)
        return profile_data.get(key, match.group(0))

    return re.sub(r'\{\{(\w+)\}\}', replacer, template_text)


def load_template(name: str) -> str:
    """Load template file from engine/templates/{name}.md.
    Raises FileNotFoundError if missing."""
    path = TEMPLATE_DIR / f'{name}.md'
    if not path.exists():
        raise FileNotFoundError(f'Template not found: {path}')
    return path.read_text(encoding='utf-8')


def profile_to_template_data(profile: dict) -> dict:
    """Convert analyzer profile JSON into placeholder values for templates."""
    # words_reach_for: top 15 words as quoted strings
    top_words = profile.get('vocabulary', {}).get('top_words', [])
    words_reach_for = ', '.join(f'"{w}"' for w, _ in top_words[:15])

    # words_never_use
    never_use = profile.get('vocabulary', {}).get('never_use', [])
    words_never_use = ', '.join(never_use)

    # opening_pattern: count types, format as percentages
    openings = profile.get('openings_closings', {}).get('openings', [])
    opening_pattern = _format_type_distribution(openings)

    # closing_pattern: same for closings
    closings = profile.get('openings_closings', {}).get('closings', [])
    closing_pattern = _format_type_distribution(closings)

    # sentence_rhythm
    rhythm = profile.get('rhythm', {})
    mean = rhythm.get('mean', 0)
    rmin = rhythm.get('min', 0)
    rmax = rhythm.get('max', 0)
    fragment_rate = rhythm.get('fragment_rate', 0)
    fragment_pct = round(fragment_rate * 100)
    sentence_rhythm = (
        f'Average sentence {mean} words. '
        f'Range {rmin}-{rmax}. '
        f'Fragment rate: {fragment_pct}%.'
    )

    # max_emdash
    max_emdash = str(profile.get('punctuation', {}).get('suggested_max_emdash', 0))

    # sign_off
    sign_off = profile.get('sign_off', '') or ''

    return {
        'voice_identity': 'Extracted from your writing samples. Your voice, your rhythm, your choices.',
        'sentence_rhythm': sentence_rhythm,
        'words_reach_for': words_reach_for,
        'words_never_use': words_never_use,
        'opening_pattern': opening_pattern,
        'closing_pattern': closing_pattern,
        'sign_off': sign_off,
        'writing_samples': '',
        'max_emdash': max_emdash,
        'persuasion_style': 'Extracted from your samples. Apply your natural persuasion approach.',
    }


def _format_type_distribution(items: list) -> str:
    """Count 'type' field in list of dicts, return formatted percentage string."""
    if not items:
        return ''
    counts = Counter(item.get('type', 'unknown') for item in items)
    total = len(items)
    parts = []
    for type_name, count in counts.most_common():
        pct = round(count / total * 100)
        parts.append(f'{pct}% {type_name}.')
    return ' '.join(parts)

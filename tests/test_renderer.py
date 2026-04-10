import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from engine.renderer import render_skill, profile_to_template_data

def test_render_replaces_placeholders():
    template = "Your voice: {{voice_identity}}. Words: {{words_reach_for}}."
    data = {'voice_identity': 'Sounds like a builder', 'words_reach_for': 'build, teardown'}
    result = render_skill(template, data)
    assert '{{voice_identity}}' not in result
    assert 'Sounds like a builder' in result

def test_render_leaves_unknown_placeholders():
    template = "Known: {{voice_identity}}. Unknown: {{something_else}}."
    data = {'voice_identity': 'test'}
    result = render_skill(template, data)
    assert '{{something_else}}' in result

def test_profile_to_template_data_has_all_keys():
    profile = {
        'punctuation': {'suggested_max_emdash': 2},
        'rhythm': {'mean': 14, 'min': 3, 'max': 38, 'fragment_rate': 0.18, 'conjunction_starters': 5},
        'vocabulary': {'top_words': [('build', 10), ('brand', 8)], 'never_use': ['delve', 'leverage'], 'whitelisted': []},
        'structure': {},
        'register': {},
        'openings_closings': {'openings': [{'type': 'declaration', 'text': 'test'}], 'closings': [{'type': 'fragment', 'text': 'test'}]},
        'sign_off': '- Michael',
    }
    data = profile_to_template_data(profile)
    assert 'voice_identity' in data
    assert 'words_reach_for' in data
    assert 'max_emdash' in data
    assert data['sign_off'] == '- Michael'
    assert data['max_emdash'] == '2'

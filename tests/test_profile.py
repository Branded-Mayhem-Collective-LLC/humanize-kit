import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from engine.analyzer import build_profile

SAMPLE_TEXTS = [
    "The problem is simple. Your brand has no spine.\n\nMessaging shifts every quarter.\n\n- Michael",
    "I build systems that turn websites into the reason the phone rings.\n\nWant me to show you?\n\n- Michael",
    "Three things wrong with your site. Your homepage buries the CTA. Your contact form asks too much.\n\n- Michael",
]

def test_build_profile_returns_all_keys():
    profile = build_profile(SAMPLE_TEXTS)
    for key in ['punctuation', 'rhythm', 'vocabulary', 'structure',
                'register', 'openings_closings', 'sign_off', 'samples_used']:
        assert key in profile, f"Missing key: {key}"

def test_build_profile_detects_sign_off():
    profile = build_profile(SAMPLE_TEXTS)
    assert profile['sign_off'] == '- Michael'

def test_build_profile_serializable():
    profile = build_profile(SAMPLE_TEXTS)
    json_str = json.dumps(profile, indent=2)
    assert len(json_str) > 100

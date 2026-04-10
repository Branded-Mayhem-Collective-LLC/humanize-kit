#!/usr/bin/env python3
"""
Humanize Kit Installer — Guided CLI wizard.
Contraband from Branded Mayhem.
"""

import json
import os
import platform
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

# Ensure engine imports work
sys.path.insert(0, str(Path(__file__).parent))

from engine.analyzer import build_profile
from engine.renderer import load_template, render_skill, profile_to_template_data
from engine import scraper


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def clear_screen():
    if platform.system() == 'Windows':
        subprocess.run(['cls'], check=False, shell=True)
    else:
        subprocess.run(['clear'], check=False)


def prompt(msg='', default=''):
    try:
        val = input(msg).strip()
    except EOFError:
        val = ''
    return val if val else default


def word_count(text):
    return len(text.split())


def print_header():
    clear_screen()
    print('=' * 56)
    print('  HUMANIZE KIT INSTALLER')
    print('  Contraband from Branded Mayhem')
    print('=' * 56)
    print()


# ---------------------------------------------------------------------------
# Step 1 — Entry
# ---------------------------------------------------------------------------

def check_python():
    v = sys.version_info
    if v < (3, 8):
        print(f'Python 3.8+ required. You have {v.major}.{v.minor}.{v.micro}.')
        sys.exit(1)
    print(f'Python {v.major}.{v.minor}.{v.micro} — OK')
    print()


def entry():
    print_header()
    check_python()
    prompt('Press Enter to start...')


# ---------------------------------------------------------------------------
# Step 2 — Collect Samples
# ---------------------------------------------------------------------------

def _read_files(path_str):
    """Read .txt, .md, and optionally .docx files from a path."""
    p = Path(path_str).expanduser()
    samples = []

    if p.is_file():
        paths = [p]
    elif p.is_dir():
        paths = sorted(
            f for f in p.iterdir()
            if f.suffix in ('.txt', '.md', '.docx')
        )
    else:
        print(f'  Not found: {p}')
        return samples

    for fp in paths:
        if fp.suffix == '.docx':
            try:
                import docx
                doc = docx.Document(str(fp))
                text = '\n\n'.join(para.text for para in doc.paragraphs if para.text.strip())
                if text.strip():
                    samples.append(text)
                    print(f'  Read: {fp.name} ({word_count(text)} words)')
            except ImportError:
                print(f'  Skipped {fp.name} — install python-docx to read .docx files')
            except Exception as e:
                print(f'  Error reading {fp.name}: {e}')
        else:
            try:
                text = fp.read_text(encoding='utf-8')
                if text.strip():
                    samples.append(text)
                    print(f'  Read: {fp.name} ({word_count(text)} words)')
            except Exception as e:
                print(f'  Error reading {fp.name}: {e}')

    return samples


def collect_samples():
    print()
    print('STEP 1: VOICE SAMPLES')
    print('-' * 40)
    print()
    print('Grab writing you\'re proud of. Not your cleanest work - your most')
    print('honest work. The drunk text that landed. The email you sent without')
    print('editing. The post that felt risky. That\'s what we\'re calibrating to.')
    print()

    samples = []

    while True:
        total_words = sum(word_count(s) for s in samples)
        print(f'[{len(samples)} samples, ~{total_words} words]')
        print()
        print('  1. Paste text directly')
        print('  2. Point to file(s) or folder')
        print('  3. Scrape a URL' + ('' if scraper.is_available() else '  (requires: pip install requests beautifulsoup4)'))
        print('  4. Done')
        print()
        choice = prompt('Choose [1-4]: ')

        if choice == '1':
            print()
            print('Paste your text. Blank line = end of one sample. Type "done" to stop pasting.')
            print()
            while True:
                lines = []
                while True:
                    line = prompt()
                    if line.lower() == 'done':
                        if lines:
                            text = '\n'.join(lines)
                            samples.append(text)
                            print(f'  Added sample ({word_count(text)} words)')
                        print()
                        break
                    if line == '' and lines:
                        text = '\n'.join(lines)
                        samples.append(text)
                        print(f'  Added sample ({word_count(text)} words)')
                        lines = []
                        continue
                    if line:
                        lines.append(line)
                if not lines:
                    break

        elif choice == '2':
            path_str = prompt('Path to file or folder: ')
            if path_str:
                new = _read_files(path_str)
                samples.extend(new)
                if not new:
                    print('  No readable files found.')
            print()

        elif choice == '3':
            if not scraper.is_available():
                print('  Scraper not available. Install: pip install requests beautifulsoup4')
                print()
                continue
            url = prompt('URL: ')
            if url:
                print('  Scraping...')
                text = scraper.scrape_url(url)
                if text:
                    samples.append(text)
                    print(f'  Got {word_count(text)} words')
                else:
                    print('  Could not extract text from that URL.')
            print()

        elif choice == '4':
            total_words = sum(word_count(s) for s in samples)
            if len(samples) < 3 or total_words < 500:
                print()
                print(f'  We have {len(samples)} samples / ~{total_words} words.')
                print('  Recommend at least 3 samples and ~500 words for a solid profile.')
                override = prompt('  Continue anyway? [y/N]: ')
                if override.lower() != 'y':
                    continue
            break

        else:
            print('  Pick 1-4.')
            print()

    return samples


# ---------------------------------------------------------------------------
# Step 3 — Analyze and Review
# ---------------------------------------------------------------------------

def _type_pct(items):
    """Return a percentage breakdown string from a list of {type, text} dicts."""
    if not items:
        return 'N/A'
    from collections import Counter
    counts = Counter(item['type'] for item in items)
    total = len(items)
    parts = []
    for t, c in counts.most_common():
        parts.append(f'{round(c / total * 100)}% {t}')
    return ', '.join(parts)


def analyze_and_review(samples):
    print()
    print('Analyzing your voice...')
    print()

    profile = build_profile(samples)

    # Display fingerprint
    punct = profile['punctuation']
    rhythm = profile['rhythm']
    vocab = profile['vocabulary']
    oc = profile['openings_closings']
    sign_off = profile['sign_off']

    h2e = punct['ratios']['hyphen_to_emdash']
    h2e_str = 'inf' if h2e == float('inf') else f'{h2e:.1f}'

    print('YOUR VOICE FINGERPRINT')
    print('-' * 40)
    print(f'Punctuation:  Hyphen-to-em-dash ratio: {h2e_str}. Parentheses: {punct["parentheses"]}. Ellipsis: {punct["ellipsis"]}.')
    print(f'Rhythm:       Average sentence {rhythm["mean"]} words. Range {rhythm["min"]}-{rhythm["max"]}. Fragment rate: {round(rhythm["fragment_rate"] * 100)}%.')
    top8 = ', '.join(f'"{w}"' for w, _ in vocab['top_words'][:8])
    print(f'Vocabulary:   Words you reach for: {top8}...')
    never5 = ', '.join(vocab['never_use'][:5])
    print(f'              AI tells blocked: {never5}...')
    print(f'Openings:     {_type_pct(oc["openings"])}')
    print(f'Closings:     {_type_pct(oc["closings"])}')
    if sign_off:
        print(f'Sign-off:     "{sign_off}"')
    print()

    # Whitelist philosophy
    if vocab['whitelisted']:
        for w in vocab['whitelisted']:
            print(f'  You actually use "{w}" a lot. AI detection tools flag that word.')
            print(f'  We\'re keeping it anyway. This tool doesn\'t exist to sand you down')
            print(f'  to something safe. It exists to amplify you.')
            print()

    # Review philosophy
    print('AI is the average of everyone. You\'re a fingerprint. This profile is')
    print('yours - curse, hedge, self-deprecate, whatever you do. The point isn\'t')
    print('to write better. The point is to write like you, and not get punished')
    print('for using a tool to do it.')
    print()

    ok = prompt('Does this look right? [Y/n]: ', default='y')
    if ok.lower() == 'n':
        profile = _refine_profile(profile, samples)

    return profile


def _refine_profile(profile, samples):
    """Let user tweak the profile."""
    while True:
        print()
        print('  1. Add reach-for words')
        print('  2. Add never-use words')
        print('  3. Add more samples (re-analyze)')
        print('  4. Accept anyway')
        print()
        choice = prompt('Choose [1-4]: ')

        if choice == '1':
            words = prompt('Words to add (comma-separated): ')
            if words:
                extras = [w.strip().lower() for w in words.split(',') if w.strip()]
                existing = [w for w, _ in profile['vocabulary']['top_words']]
                for w in extras:
                    if w not in existing:
                        profile['vocabulary']['top_words'].append((w, 1))
                print(f'  Added {len(extras)} words.')

        elif choice == '2':
            words = prompt('Words to block (comma-separated): ')
            if words:
                extras = [w.strip().lower() for w in words.split(',') if w.strip()]
                for w in extras:
                    if w not in profile['vocabulary']['never_use']:
                        profile['vocabulary']['never_use'].append(w)
                    if w in profile['vocabulary']['whitelisted']:
                        profile['vocabulary']['whitelisted'].remove(w)
                print(f'  Added {len(extras)} to never-use list.')

        elif choice == '3':
            new_samples = collect_samples()
            samples.extend(new_samples)
            profile = build_profile(samples)
            print('  Re-analyzed with new samples.')

        elif choice == '4':
            break

    return profile


# ---------------------------------------------------------------------------
# Step 4 — Generate and Install
# ---------------------------------------------------------------------------

def _top_samples(samples, n=3, max_words=200):
    """Return top n samples by length, truncated to max_words."""
    ranked = sorted(samples, key=lambda s: word_count(s), reverse=True)
    result = []
    for s in ranked[:n]:
        words = s.split()
        if len(words) > max_words:
            s = ' '.join(words[:max_words]) + '...'
        result.append(s)
    return result


def generate_and_install(profile, samples):
    print()
    print('STEP 3: GENERATE SKILLS')
    print('-' * 40)
    print()

    # Platform
    print('Where will you use this?')
    print('  1. Claude Code')
    print('  2. Claude Desktop / claude.ai')
    print('  3. Both')
    print()
    plat = prompt('Choose [1-3]: ', default='3')
    install_claude_code = plat in ('1', '3')
    install_desktop = plat in ('2', '3')

    # Skills
    print()
    print('Which skills?')
    print('  1. /humanize (long-form)')
    print('  2. /humanize-ig (Instagram captions)')
    print('  3. Both')
    print()
    skill_choice = prompt('Choose [1-3]: ', default='3')
    skill_names = []
    if skill_choice in ('1', '3'):
        skill_names.append('humanize')
    if skill_choice in ('2', '3'):
        skill_names.append('humanize-ig')

    # Prepare template data
    template_data = profile_to_template_data(profile)
    top = _top_samples(samples)
    template_data['writing_samples'] = '\n\n---\n\n'.join(top)

    # Render skills
    rendered = {}
    for name in skill_names:
        try:
            tmpl = load_template(name)
            rendered[name] = render_skill(tmpl, template_data)
            print(f'  Rendered: {name}.md')
        except FileNotFoundError:
            print(f'  Template not found: {name}.md — skipping')

    if not rendered:
        print('  No skills rendered. Check your templates directory.')
        return

    de_emdash_src = Path(__file__).parent / 'engine' / 'de_emdash.py'

    # Install to Claude Code
    if install_claude_code:
        dest = Path.home() / '.claude' / 'skills' / 'humanize'
        dest.mkdir(parents=True, exist_ok=True)

        for name, content in rendered.items():
            target = dest / f'{name}.md'
            if target.exists():
                overwrite = prompt(f'  {target} exists. Overwrite? [y/N]: ')
                if overwrite.lower() != 'y':
                    print(f'  Skipped {name}.md')
                    continue
            target.write_text(content, encoding='utf-8')
            print(f'  Installed: {target}')

        if de_emdash_src.exists():
            de_target = dest / 'de_emdash.py'
            if de_target.exists():
                overwrite = prompt(f'  {de_target} exists. Overwrite? [y/N]: ')
                if overwrite.lower() != 'y':
                    print('  Skipped de_emdash.py')
                else:
                    shutil.copy2(str(de_emdash_src), str(de_target))
                    print(f'  Installed: {de_target}')
            else:
                shutil.copy2(str(de_emdash_src), str(de_target))
                print(f'  Installed: {de_target}')

    # Create zip for Desktop/Online
    if install_desktop:
        out_dir = Path.home() / 'Downloads'
        out_dir.mkdir(parents=True, exist_ok=True)

        for name, content in rendered.items():
            zip_path = out_dir / f'{name}-skill.zip'
            with zipfile.ZipFile(str(zip_path), 'w', zipfile.ZIP_DEFLATED) as zf:
                zf.writestr(f'{name}.md', content)
                if de_emdash_src.exists():
                    zf.write(str(de_emdash_src), 'de_emdash.py')
            print(f'  Created: {zip_path}')

        print()
        print('  To use with Claude Desktop / claude.ai:')
        print('  1. Open a conversation')
        print('  2. Upload the .zip file(s) from ~/Downloads')
        print('  3. Tell Claude: "Use the humanize skill in this zip to rewrite my text"')
        print()

    # Save profile
    profile_path = Path.home() / '.claude' / 'voice-profile.json'
    profile_path.parent.mkdir(parents=True, exist_ok=True)
    profile_path.write_text(json.dumps(profile, indent=2, default=str), encoding='utf-8')
    print(f'  Profile saved: {profile_path}')
    print()


# ---------------------------------------------------------------------------
# Step 5 — Email Capture
# ---------------------------------------------------------------------------

def email_capture():
    print()
    print('You now own a profile of how you write. Not how AI thinks you should')
    print('write. Not how LinkedIn thinks you should write. How you actually write.')
    print('Keep it weird.')
    print()

    notify = prompt('Detection patterns shift as models update. Want to get notified when we update the pattern list? [y/N]: ')
    if notify.lower() != 'y':
        return

    name = prompt('Name: ')
    email = prompt('Email: ')

    if not email:
        print('  No email provided. Skipping.')
        return

    try:
        import urllib.request
        data = json.dumps({'name': name, 'email': email}).encode('utf-8')
        req = urllib.request.Request(
            'https://your-project.supabase.co/functions/v1/humanize-signup',
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST',
        )
        urllib.request.urlopen(req, timeout=10)
        print('  Signed up. We\'ll keep you posted.')
    except Exception:
        print('  Could not reach signup server.')
        print('  Email hello@brandedmayhem.com to sign up manually.')
    print()


# ---------------------------------------------------------------------------
# Step 6 — Done
# ---------------------------------------------------------------------------

def done():
    print()
    print('=' * 56)
    print('  INSTALLATION COMPLETE')
    print('=' * 56)
    print()
    print('What was installed:')
    profile_path = Path.home() / '.claude' / 'voice-profile.json'
    skill_dir = Path.home() / '.claude' / 'skills' / 'humanize'
    if profile_path.exists():
        print(f'  Voice profile  -> {profile_path}')
    if skill_dir.exists():
        for f in sorted(skill_dir.iterdir()):
            print(f'  Skill file     -> {f}')
    dl = Path.home() / 'Downloads'
    for zf in sorted(dl.glob('*-skill.zip')):
        print(f'  Zip download   -> {zf}')
    print()
    print('Contraband builds the tools. Branded Mayhem builds the strategy.')
    print('brandedmayhem.com')
    print()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    entry()
    samples = collect_samples()
    profile = analyze_and_review(samples)
    generate_and_install(profile, samples)
    email_capture()
    done()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n\nInterrupted. Your data was not saved.\n')
        sys.exit(1)

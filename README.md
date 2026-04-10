# Humanize Kit

**Make AI writing sound like you actually wrote it.**

3 Claude Code skills that solve the #1 complaint about AI writing: it all sounds the same. Overly polished, weirdly formal, and nothing like how you actually communicate.

This kit interviews you about your writing style, builds a personal voice profile, then rewrites any AI-generated text to match your fingerprint — not a generic "humanized" version, but text that sounds like *you*.

Free and open source. Built by [Contraband from Branded Mayhem](https://contraband.brandedmayhem.com).

---

## The Problem

You've tried custom instructions. System prompts. Different models. It helps a little but you still end up editing half the output. The tone is wrong. The rhythm is wrong. It doesn't sound like something you'd actually send.

AI detection tools (Pangram, GPTZero, Copyleaks) catch it too — because AI text follows statistical patterns that are invisible to you but obvious to classifiers.

## What This Solves

The Humanize Kit attacks both problems:

1. **Voice Profiler** interviews you and analyzes your real writing samples to build a structured voice profile — your rhythm, vocabulary, persuasion style, grammar personality, and emotional range.

2. **Humanize** scores any text against 23 AI detection patterns, then rewrites it using your voice profile. The output doesn't just avoid detection — it sounds like you wrote it.

3. **Humanize IG** does the same thing but optimized for Instagram: lowercase, dense blocks, imperfect grammar, phone-typed feel.

---

## The 3 Skills

| Skill | What It Does | When to Use |
|-------|-------------|-------------|
| `/voice-profiler` | Interviews you about your writing style. Analyzes 3-5 real writing samples. Generates `~/.claude/voice-profile.md`. | Run once. Update when your voice evolves. |
| `/humanize` | Scores text against 23 AI patterns (statistical, deep learning, document-level). Rewrites in your voice profile. | Any AI-generated text — emails, posts, proposals, copy. |
| `/humanize-ig` | Same detection analysis + Instagram-specific rules: lowercase, no em dashes, one dense paragraph, abbreviated phrasing. | Instagram captions that don't read like a robot wrote them. |

---

## Quick Start

### Install

**Claude Code (recommended):**

```bash
python3 install.py
```

The installer handles everything — copies skills to `~/.claude/skills/`, validates the file structure, and optionally launches the voice profiler to get you set up. Takes 5-10 minutes start to finish.

**Claude Desktop / claude.ai:**

Download the `.zip` from [contraband.brandedmayhem.com](https://contraband.brandedmayhem.com) and upload it through the interface. The zip includes all three skills pre-packaged for manual import.

### Two Paths After Install

**Quick path:** The installer prompts you to run `/voice-profiler` immediately. Answer the questions, paste a few writing samples, and you're done. 5-10 minutes total.

**Deep path:** Run `/voice-profiler` as a full conversational session. It walks you through three phases — sample collection, guided questions, and synthesis. Takes longer but produces a more precise profile, especially useful if you write across multiple formats or contexts.

### Build Your Voice Profile (Do This First)

```
/voice-profiler
```

Claude will ask you for 3-5 pieces of real writing you're proud of — emails, LinkedIn posts, proposals, website copy, anything that sounds like you at your best. Then it asks targeted questions about your style preferences.

**This is the step that makes everything else work.** Without a voice profile, `/humanize` produces generic-human text. With one, it produces YOUR-human text.

### Humanize Any Text

```
/humanize [paste AI-generated text here]
```

Or use "last" to humanize the previous output:

```
/humanize last
```

### Humanize for Instagram

```
/humanize-ig [paste text here]
```

---

## How the Voice Profile Works

The `/voice-profiler` skill runs an interactive interview in three phases:

**Phase 1: Collect Writing Samples**

You paste 3-5 pieces of real writing. Claude analyzes each one for:

- Sentence rhythm (short-long-short? All punchy? Flowing?)
- Opening patterns (cold open? Story? Question?)
- Closing patterns (CTA? Punchline? Reflection?)
- Vocabulary fingerprint (words you reach for repeatedly)
- Grammar personality (fragments? Run-ons? Perfect grammar?)
- Emotional range (humor? Bluntness? Vulnerability?)
- Persuasion style (diagnosis? Storytelling? Data-first?)

**Phase 2: Guided Questions**

Claude asks targeted questions to fill gaps the samples didn't reveal — words you hate, phrases that are distinctly yours, how you sign off.

**Phase 3: Synthesis**

Claude plays back what it found. You correct anything that's off. Then it writes the profile to `~/.claude/voice-profile.md`.

The profile is a structured Markdown file you can read and edit manually anytime. The installer automates setup but the profile itself is plain text — yours to own, version, and modify.

---

## How Humanize Works

The `/humanize` skill runs a 4-step process:

### Step 1: Analyze — Score 23 AI Patterns

Each pattern scored 0-3 (not present → strong AI signal):

**Tier 1 — Statistical Patterns (what older detectors catch):**
- Low perplexity (predictable word choices)
- Low burstiness (uniform sentence lengths)
- Limited semantic diversity (recycled vocabulary)
- Smooth token probability (no surprising word choices)

**Tier 2 — Deep Learning Patterns (what Pangram 3.0 catches):**
- Structural uniformity (intro → points → conclusion)
- Hedging and qualification ("It's important to note...")
- Generic abstraction ("Many businesses struggle with...")
- Mechanical transitions ("Furthermore," "Additionally,")
- Emotional flattening (no personality peaks or valleys)
- Over-completeness (answers questions nobody asked)
- List-heavy structure (bullets as crutch)
- Preamble and summary (restating what was asked, summarizing what was said)
- Significance inflation ("groundbreaking," "revolutionary," "game-changing")
- Superficial -ing clauses ("Leveraging our expertise, we deliver...")
- Copulative avoidance (endless "is/are" constructions, nothing active)
- Rule of three (compulsive three-part lists and triadic phrasing)
- Elegant variation (avoiding word repetition so hard it becomes obvious)
- Negative parallelisms ("not only X but also Y" everywhere)

**Tier 3 — Document-Level Signals (what catches longer content):**
- Consistent register (same formality throughout)
- Balanced paragraph length (uniformly distributed)
- Perfect grammar (no fragments, no bent rules)
- Absence of voice (could have been written by anyone)
- Symmetrical structure (equal weight to every point)

### Step 2: Report — Show the Score

```
PATTERN ANALYSIS
────────────────
Tier 1 (Statistical):   [score]/12
Tier 2 (Deep Learning): [score]/42
Tier 3 (Document):      [score]/15
────────────────
Total: [score]/69 ([percentage]%)
Mode:  [SURGICAL | MODERATE | FULL REWRITE]
```

- **0-15%** → Surgical (touch only flagged sentences)
- **16-50%** → Moderate (rewrite flagged sections)
- **51%+** → Full Rewrite (rebuild from scratch, keep core message)

### Step 3: Rewrite — Apply Your Voice Profile

Loads `~/.claude/voice-profile.md` and applies your:

- Core identity and sentence rhythm
- Opening and closing patterns
- Vocabulary preferences and banned words
- Persuasion style
- Grammar personality
- Emotional range

Each of the 23 pattern-breaking rules maps to specific transformations — if hedging scored high, every hedge gets deleted and replaced with direct statements in your style.

Em dash post-processing runs automatically after rewrite. No extra step required.

### Step 4: Output

Clean rewritten text + before/after score comparison.

---

## Instagram Mode

`/humanize-ig` applies 10 non-negotiable IG voice rules on top of the standard pattern-breaking:

1. **Lowercase everything** except the first word
2. **No em dashes** — periods and commas only
3. **One paragraph** — no line breaks in the body
4. **Imperfect grammar mandatory** — dropped apostrophes, fragments, run-ons
5. **Abbreviated phrasing** — "bc", "tbh", "imo" (2-3 per caption max)
6. **Contractions always**
7. **No transition words**
8. **No hedging**
9. **Hashtags at the end** — 4-8 max, separated by a line break
10. **End like talking, not writing**

The output reads like someone who knows what they're talking about but typed it on their phone between meetings.

---

## Example

**AI-generated input:**
```
It's important to note that brand strategy extends far beyond visual identity.
While many businesses focus primarily on logos and color schemes, the most
successful brands invest in understanding their core audience tensions and
competitive positioning. Furthermore, establishing a clear brand platform
enables consistent decision-making across all touchpoints.
```

**After `/humanize` (with voice profile loaded):**
```
Brand strategy isn't the logo. It's the thing underneath that nobody sees
until it's missing.

Your messaging shifts every quarter. Your team can't explain what you do
in one sentence. Every campaign feels like starting over.

That's not a design problem. That's a spine problem. Fix the structure
and everything above it stops collapsing.
```

**After `/humanize-ig`:**
```
brand strategy isnt the logo. its the thing underneath that nobody sees until its missing. your messaging shifts every quarter, your team cant explain what you do in one sentence and every campaign feels like starting over. thats not a design problem thats a spine problem. fix the structure and everything above it stops collapsing

#brandstrategy #branding #marketingstrategy #builddifferent
```

---

## FAQ

**Do I need a voice profile to use `/humanize`?**

No, but the output will be generic-human instead of YOUR-human. The voice profile is what makes this actually useful. Spend the 10 minutes.

**Do I need to run the installer?**

Only if you're using Claude Code. For Claude Desktop or claude.ai, download the `.zip` from [contraband.brandedmayhem.com](https://contraband.brandedmayhem.com) and import it manually. The installer is just a convenience layer for Claude Code users.

**Can I have multiple voice profiles?**

Yes. Save them as different files (`voice-profile-linkedin.md`, `voice-profile-email.md`) and tell Claude which to load.

**Does this guarantee passing AI detection?**

No. AI detection is probabilistic and evolving. But breaking 23 statistical patterns while writing in an authentic voice profile makes detection significantly harder.

**Can I use this with Cursor or Codex?**

Yes. These are standard SKILL.md files. They work with any tool that reads the SKILL.md format.

**How do I update my voice profile?**

Run `/voice-profiler` again. It detects your existing profile and offers to update or start fresh.

**What's the difference between 16 and 23 patterns?**

The original Humanize Kit targeted 16 patterns. This version adds 7 new Tier 2 patterns — significance inflation, superficial -ing clauses, copulative avoidance, rule of three, elegant variation, and negative parallelisms. These are the patterns Pangram and newer classifiers have gotten better at catching. Max score is now 69 (was 48).

---

## Part of Contraband from Branded Mayhem

This is a free sample from [Contraband](https://contraband.brandedmayhem.com) — Claude Code skills across packages covering brand strategy, content, SEO, conversion optimization, and sales methodology. Built by practitioners who run an agency, not prompt engineers who read a blog post.

If the Humanize Kit is useful, the full stack is worth looking at.

Contraband builds the tools. Branded Mayhem builds the strategy. [brandedmayhem.com](https://brandedmayhem.com)

---

## License

MIT. Free for personal and commercial use. Do whatever you want with it.

Questions: support@brandedmayhem.com

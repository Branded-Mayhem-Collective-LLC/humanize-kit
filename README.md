# Humanize Kit

Your AI writing sounds like AI writing. You know it. The people reading it know it. The detection tools definitely know it.

This fixes that.

Three Claude skills that analyze your real writing, build a fingerprint of how you actually sound, then rewrite AI output to match. Not a generic "humanized" version. Text that sounds like you typed it.

Free. Open source. [Contraband from Branded Mayhem](https://contraband.brandedmayhem.com).

---

## What's wrong with AI writing

You've tried custom instructions. System prompts. Different models. Still editing half the output because the tone is wrong, the rhythm is wrong, and it doesn't sound like something you'd actually send.

Detection tools catch it too. Pangram, GPTZero, Copyleaks - they're keying on statistical patterns you can't see but classifiers eat for breakfast.

## What this does

**Voice Profiler** interviews you, analyzes your real writing samples, and builds a structured voice profile. Your rhythm. Your vocabulary. Your weird grammar habits. The way you actually close an email.

**Humanize** scores any text against 23 AI detection patterns, then rewrites it using your profile. Breaks the statistical fingerprint while sounding like you.

**Humanize IG** does the same thing but for Instagram. Lowercase. Dense blocks. Imperfect grammar. Phone-typed energy.

---

## Install

**Claude Code:**

```bash
python3 install.py
```

Copies skills, validates structure, walks you through voice profiling. 5-10 minutes.

**Claude Desktop / claude.ai:**

Download the `.zip` from [contraband.brandedmayhem.com](https://contraband.brandedmayhem.com). Upload through Settings > Customize > Skills.

## Build your voice profile

This is the step that matters. Without it, `/humanize` produces generic-human text. With it, it produces YOUR-human text.

```
/voice-profiler
```

Paste 3-5 pieces of writing you're proud of. Not your cleanest work - your most honest work. The drunk text that landed. The email you sent without editing. The post that felt risky.

Claude analyzes sentence rhythm, opening patterns, vocabulary fingerprint, grammar personality, emotional range, persuasion style. Asks a few targeted questions. Writes a profile to `~/.claude/voice-profile.md`.

Plain text. Yours to read, edit, version.

**Quick path:** The installer runs voice profiling inline. 5-10 minutes total.

**Deep path:** Run `/voice-profiler` as a separate conversational session. More precise, especially if you write across multiple formats.

## Use it

```
/humanize [paste AI-generated text here]
```

```
/humanize last
```

```
/humanize-ig [paste text here]
```

---

## How it works

Every piece of AI text gets scored against 23 patterns across three tiers.

**Tier 1 (Statistical)** - what older detectors catch. Predictable word choices, uniform sentence lengths, recycled vocabulary, smooth token probability.

**Tier 2 (Deep Learning)** - what Pangram 3.0 catches. Structural uniformity, hedging, generic abstractions, mechanical transitions, emotional flattening, over-completeness, list-heavy structure, preamble/summary. Plus six newer patterns that classifiers have gotten better at flagging: significance inflation, superficial -ing clauses, copulative avoidance, rule of three, elegant variation, negative parallelisms.

**Tier 3 (Document-Level)** - what catches longer content. Consistent register, balanced paragraphs, perfect grammar, absence of voice, symmetrical structure.

```
PATTERN ANALYSIS
────────────────
Tier 1 (Statistical):   [score]/12
Tier 2 (Deep Learning): [score]/42
Tier 3 (Document):      [score]/15
────────────────
Total: [score]/69 ([percentage]%)
Mode:  SURGICAL | MODERATE | FULL REWRITE
```

Under 15%? Surgical. Touch flagged sentences only. 16-50%? Moderate. Rewrite flagged sections. Over 51%? Full rewrite from scratch. Core message stays, everything else gets rebuilt.

Then your voice profile gets applied - vocabulary, rhythm, opening patterns, grammar personality, the whole fingerprint. Em dash post-processing runs automatically (LLMs can't stop using em dashes at the token level, so a Python script catches what the rewrite misses).

---

## Instagram mode

`/humanize-ig` applies 10 rules on top of the standard pattern-breaking. Lowercase everything. No em dashes. One dense paragraph. Imperfect grammar. Abbreviated phrasing. No transition words. No hedging. Hashtags at the end. End like talking.

The output reads like someone who knows what they're talking about but typed it between meetings on their phone.

---

## Example

**AI input:**
```
It's important to note that brand strategy extends far beyond visual identity.
While many businesses focus primarily on logos and color schemes, the most
successful brands invest in understanding their core audience tensions and
competitive positioning. Furthermore, establishing a clear brand platform
enables consistent decision-making across all touchpoints.
```

**After /humanize:**
```
Brand strategy isn't the logo. It's the thing underneath that nobody sees
until it's missing.

Your messaging shifts every quarter. Your team can't explain what you do
in one sentence. Every campaign feels like starting over.

That's not a design problem. That's a spine problem. Fix the structure
and everything above it stops collapsing.
```

**After /humanize-ig:**
```
brand strategy isnt the logo. its the thing underneath that nobody sees
until its missing. your messaging shifts every quarter, your team cant
explain what you do in one sentence and every campaign feels like starting
over. thats not a design problem thats a spine problem. fix the structure
and everything above it stops collapsing

#brandstrategy #branding #marketingstrategy #builddifferent
```

---

## FAQ

**Do I need a voice profile?**
Technically no. Practically yes. Without one you get generic-human. With one you get you.

**Multiple voice profiles?**
Save them as different files. `voice-profile-linkedin.md`, `voice-profile-email.md`. Tell Claude which to load.

**Does this guarantee passing AI detection?**
No. Detection is probabilistic and evolving. Breaking 23 statistical patterns while writing in an authentic voice makes it significantly harder to flag. Not impossible.

**Works with Cursor or Codex?**
Yes. Standard SKILL.md files. Anything that reads the format.

**What changed from v1 to v2?**
v1 had 16 patterns (max score 48). v2 adds 7 Tier 2 patterns that newer classifiers catch - significance inflation, superficial -ing clauses, copulative avoidance, rule of three, elegant variation, negative parallelisms. Max score is 69. Plus the em dash post-processor, the automated installer, and .zip packaging for Desktop/Online.

---

## Contraband from Branded Mayhem

Free sample from [Contraband](https://contraband.brandedmayhem.com). Claude skills for brand strategy, content, SEO, conversion optimization, and sales methodology — work in Claude.ai (web), Claude Code, Claude desktop, Cursor, or Codex. Built by people who run an agency, not prompt engineers who read a blog post.

Contraband builds the tools. Branded Mayhem builds the strategy. [brandedmayhem.com](https://brandedmayhem.com)

---

MIT. Do whatever you want with it.

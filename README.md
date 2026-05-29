# Humanize Kit

[![Claude Code Plugin](https://img.shields.io/badge/Claude_Code-Plugin-D97757?logo=claude&logoColor=white)](https://github.com/anthropics/claude-plugins-community)
[![Anthropic Community Marketplace](https://img.shields.io/badge/Anthropic_Community-Marketplace-D97757?logo=anthropic&logoColor=white)](https://github.com/anthropics/claude-plugins-community)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/Branded-Mayhem-Collective-LLC/humanize-kit?style=social)](https://github.com/Branded-Mayhem-Collective-LLC/humanize-kit)

> **Install:** `/plugin marketplace add anthropics/claude-plugins-community` then `/plugin install humanize-kit@claude-community`
> Or on Claude.ai Cowork: paste this repo's URL.

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

**Humanize** scores any text against 23 AI detection patterns, then rewrites it using your profile. Breaks the statistical fingerprint and reads in your voice. (Read the [workflow notes](#workflow-notes-what-actually-passes-a-detector) before you trust the output to pass a classifier — pasting it directly is not enough.)

**Humanize IG** does the same thing but for Instagram. Lowercase. Dense blocks. Imperfect grammar. Phone-typed energy.

---

## Install

**Claude Code (plugin — recommended):**

```text
/plugin marketplace add Branded-Mayhem-Collective-LLC/humanize-kit
/plugin install humanize-kit@bmc-humanize-kit
```

Skills land namespaced as `/humanize-kit:humanize`, `/humanize-kit:humanize-ig`, and `/humanize-kit:voice-profiler`. A session-start hook will warn you if `~/.claude/voice-profile.md` doesn't exist yet so you know the next step.

Once humanize-kit lands in [Anthropic's community marketplace](https://github.com/anthropics/claude-plugins-community) (submitted for review), you'll also be able to:

```text
/plugin marketplace add anthropics/claude-plugins-community
/plugin install humanize-kit@claude-community
```

**Claude Code (legacy, standalone skills):**

```bash
python3 install.py
```

Copies skills into `~/.claude/skills/`, validates structure, walks you through voice profiling. 5-10 minutes. Use this only if you cannot use the plugin install path; skills won't be namespaced and won't get the SessionStart voice-profile hook.

**Claude.ai web / Claude Desktop:**

Paste this repo's URL into Claude and ask: "Install the skills from https://github.com/Branded-Mayhem-Collective-LLC/humanize-kit". Claude fetches the repo, registers the skills, and asks permission.

Or download the repo as `.zip` (GitHub Code button → Download ZIP, or grab it from [contraband.brandedmayhem.com](https://contraband.brandedmayhem.com)), unzip, then upload skill folders via **Settings → Customize → Skills**.

Note: voice profiles do not persist across Claude.ai web sessions. `/voice-profiler` writes the profile to `/mnt/user-data/outputs/voice-profile.md` — download it locally, then re-upload it at the start of each session where you want `/humanize` to use it. The SKILL.md handles the path resolution automatically.

## Build your voice profile

This is the step that matters. Without it, `/humanize` produces generic-human text. With it, it produces YOUR-human text.

```
/humanize-kit:voice-profiler
```

Paste 3-5 pieces of writing you're proud of. Not your cleanest work - your most honest work. The drunk text that landed. The email you sent without editing. The post that felt risky.

Claude analyzes sentence rhythm, opening patterns, vocabulary fingerprint, grammar personality, emotional range, persuasion style. Asks a few targeted questions. Writes a profile to `~/.claude/voice-profile.md`.

Plain text. Yours to read, edit, version.

**Quick path:** The installer runs voice profiling inline. 5-10 minutes total.

**Deep path:** Run `/voice-profiler` as a separate conversational session. More precise, especially if you write across multiple formats.

## Use it

If installed as a plugin, slash commands are namespaced. If installed via the legacy `install.py`, use the unprefixed form.

```
/humanize-kit:humanize [paste AI-generated text here]
```

```
/humanize-kit:humanize last
```

```
/humanize-kit:humanize-ig [paste text here]
```

You can also describe what you want in plain English and Claude will pick the skill automatically — "humanize this", "rewrite that in my voice", "de-AI the last paragraph" all work.

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

## Workflow notes — what actually passes a detector

Honest disclosure from real-world use, not a benchmark.

**Pasting `/humanize` output directly into Pangram (or similar) does not reliably pass.** Modern classifiers — Pangram 3.0 especially — catch polished prose patterns even after the statistical features have been disrupted. If you treat this kit as "rewrite → paste into Pangram → ship," you'll be disappointed.

**The workflow that has worked in our own PR submissions and outreach:**

1. Run `/humanize-kit:humanize` (or `/humanize-kit:humanize-ig`) with a strong voice profile loaded.
2. Read the output. Don't ship it as-is.
3. **Manually retype it** — type it out fresh into the form/email/CMS where it's going. Or **dictate it verbally** and let your phone's voice-to-text transcribe it.
4. *Then* submit.

The retype step introduces the kind of micro-variation a classifier can't model: your transcription tics, the words your fingers reach for, the slight rewordings that happen between brain and keyboard. In tests against Pangram (anecdotal, single-user, with the author's voice profile) this consistently flips a "highly likely AI" score to "human" or "inconclusive."

**Limits of this claim:**
- This is not independently verified. It's one operator's repeated testing.
- It depends on a real voice profile. A weak or generic profile produces a weak result.
- Detection tools update constantly. What works this month may not work next quarter.
- It will never "guarantee" anything. AI detection is probabilistic and adversarial.

If you're doing PR outreach to outlets that screen with Pangram, or any context where being flagged costs you a placement, treat this kit as **a writing assistant that handles voice consistency**, not **a detection-evasion guarantee**. The retype step is what closes the gap.

---

## FAQ

**Do I need a voice profile?**
Technically no. Practically yes. Without one you get generic-human. With one you get you.

**Multiple voice profiles?**
Save them as different files. `voice-profile-linkedin.md`, `voice-profile-email.md`. Tell Claude which to load.

**Does this guarantee passing AI detection?**
No. See the workflow notes above. Pasting `/humanize` output directly into a classifier does not reliably pass. The retype-before-submit workflow has worked anecdotally for the author but is not independently verified.

**Why submit to Anthropic's community marketplace if it's also paid product adjacent?**
Loss-leader by design. The 3 skills here are genuinely useful standalone. The paid [Content & Creative Lab](https://github.com/Branded-Mayhem-Collective-LLC/content-creative-lab) bundles these plus 5 more (ai-focus-group, creative-thinking-ai, linkedin-authority, mayhem-method-ai-use, story-spine).

**Works with Cursor or Codex?**
Yes. Standard SKILL.md files. Anything that reads the format. Note: the plugin install path is Claude Code specific. For Cursor/Codex use the legacy `install.py` or copy the `skills/` folder directly into the tool's skill directory.

**What changed from v1 to v2?**
v1 had 16 patterns (max score 48). v2 adds 7 Tier 2 patterns that newer classifiers catch - significance inflation, superficial -ing clauses, copulative avoidance, rule of three, elegant variation, negative parallelisms. Max score is 69. Plus the em dash post-processor, the automated installer, and .zip packaging for Desktop/Online.

---

## Contraband from Branded Mayhem

Free sample from [Contraband](https://contraband.brandedmayhem.com). Claude skills for brand strategy, content, SEO, conversion optimization, and sales methodology — work in Claude.ai (web), Claude Code, Claude desktop, Cursor, or Codex. Built by people who run an agency, not prompt engineers who read a blog post.

Contraband builds the tools. Branded Mayhem builds the strategy. [brandedmayhem.com](https://brandedmayhem.com)

---

MIT. Do whatever you want with it.

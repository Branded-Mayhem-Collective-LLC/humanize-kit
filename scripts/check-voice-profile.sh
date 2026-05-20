#!/usr/bin/env bash
# Humanize Kit — session-start voice-profile check.
#
# The /humanize and /humanize-ig skills require ~/.claude/voice-profile.md to
# produce YOU-specific output instead of generic-human output. This hook warns
# (does not block) when the file is missing so first-time users know the next
# step.

set -u

PROFILE="${HOME}/.claude/voice-profile.md"

if [ ! -f "${PROFILE}" ]; then
  printf '%s\n' "[humanize-kit] No voice profile found at ${PROFILE}. Run /humanize-kit:voice-profiler before /humanize-kit:humanize for personalized output. Without it, /humanize produces generic-human text instead of your-voice text." >&2
fi

exit 0

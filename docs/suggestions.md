# Suggestions that remember your answers

[← back to README](../README.md)

As a project grows, the same manual work keeps coming back: writing release notes, rebuilding test data, reading a 2,000-line test log to find two failures. The system notices, suggests turning it into a project skill or a helper agent, and **remembers what you said**:

```
> mph-handoff
  🧭 [recipe-app] … committed.
  I noticed you rebuilt the test data by hand in 3 of the last 5 sessions.
  Want a skill for it? (yes / no / never / later)
```

- **`mph-suggest-skill`** turns repeated manual work into a project-specific skill. Session mode looks at this chat; project mode reviews the last ~10 daily logs and the project's README/scripts.
- **`mph-suggest-agent`** proposes an optional **helper agent** for heavy, noisy work (big logs, browser checks, data audits) that returns only the findings, so the main session stays small. Created as a real subagent where the tool supports it (Claude Code: `.claude/agents/`), or as a skill elsewhere.
- **Every answer is stored** in `notes/SUGGESTIONS.md`: `yes` creates it, `never` is never asked again, `no` comes back only if the evidence at least doubles ("you declined this when it was 3 times; it's 7 now"), `later` returns after a few sessions.
- **No nagging:** at most one short question per handoff, never the same idea twice in a session, and `suggestions: off` under `## Modules` in `PROJECT.md` turns it off.
- Created skills and agents are listed in `PROJECT.md`, so every tool, and `mph-menu`, knows they exist.

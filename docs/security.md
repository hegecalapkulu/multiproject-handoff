# Security overview

[← back to README](../README.md)

A one-page summary of what multiproject-handoff reads, writes and changes, for you or for whoever approves tools at your company. Everything here can be checked in the source: the skills are Markdown, the scripts are short Python and shell files using only the standard library.

## At a glance

| | |
|---|---|
| Network | **None.** No script opens a network connection. No telemetry, no account, no server. (The only network step is `git push`, and only if you set `Push: yes` in a project.) |
| Dependencies | None beyond `python3` and `git`, which you already have. Nothing is downloaded at run time. |
| Your code | Read by your AI tool as usual. The skills tell it to read **less**, not more: notes first, code only when the work needs it. |
| Deleting | Never. Notes are edited, appended or moved. The uninstaller **moves** files to `~/.handoff-removed/`. |
| Git history | Never rewritten: no force push, reset, rebase or amend. |
| Settings of your AI tool | Changed only by `mph-guard`, only after it shows you the exact change and you say yes. |

## What runs, and what it touches

| Part | Runs when | Reads | Writes |
|---|---|---|---|
| Skills (`skills/*/SKILL.md`) | you call them | your project notes; `git status/log/diff` | your project notes; a `git commit` at handoff (push only if you set it) |
| `mph-scan.py` | inside `mph-resume` and `mph-handoff` | `PROJECT.md`, resume notes, backlogs, file dates, read-only `git` commands | **nothing** |
| `install.sh` | you run it | the repo | skill folders of your AI tools, `~/.handoff/` (rules and the three scripts), optionally one block in an `AGENTS.md` you name |
| `mph-guard.py` (opt-in hook) | before each tool call in Claude Code | the command or path about to be used, `~/.handoff/guard.conf` | nothing; it only allows, asks or blocks |
| `mph-context.py` (opt-in hook) | before each message in Claude Code | Claude Code's local session transcripts (token counts, model names, how many file edits) | `~/.handoff/context-state.json` (sizes and per-session flags, no message text) |

The two hooks are installed **inactive**. They start working only when you run `mph-guard`, see the change to `~/.claude/settings.json` and say yes. Existing hooks are never removed.

## What goes into the notes

- **No secrets.** The skills are told never to write passwords, keys, tokens or real customer data into notes. The guard can also block reading `.env` files.
- **Your working-style profile stays local** by default: it is git-ignored in each project, and the general profile lives in `~/.handoff/`, outside every repo.
- **Notes can live outside the repo.** For a public repo, or notes you don't want next to the code, keep them in a private folder and point to the code from `PROJECT.md` ([how](how-it-works.md#where-the-files-live)).

## Limits, honestly

- The skills are **instructions** to an AI agent. The agent follows them, but an instruction is not a lock. If you need a lock, turn on `mph-guard` (Claude Code), or use your tool's own approval or sandbox settings (Codex, Gemini CLI, Cursor).
- The guard matches commands and paths. It is a safety net against mistakes, not a sandbox against a determined attacker.
- Notes are plain files. Anyone who can read your repo can read the notes you commit.

## Removing it

`./install.sh --uninstall --dry-run` shows what would be removed; `./install.sh --uninstall` moves it to `~/.handoff-removed/<date-time>/`. Your project notes stay. [Details](install.md#uninstall)

# Changelog

## Unreleased

- **Language choice in setup:** `mph-setup-project` asks for the language of notes and replies (English · Español · 中文 · Português · Türkçe · other), defaulting to the language the user writes in. It is kept as `Language:` in `PROJECT.md` and used whenever a message shows no language. Tested in Claude Code: a Turkish request got a Turkish screen with Türkçe as the default.
- README: **tested with Claude Code and Codex**; other tools read the same files but are not tested yet and may need more manual steps.
- **Tested across tools:** a handoff written by Claude Code was resumed by Codex (0.172) in the same folder, with the right state and next step, in 3 steps. Fixes from that test: the rules lookup now says plainly that `RULES.md` sits next to `SKILL.md` (Codex looked one folder up), and a bare command such as `mph-resume recipe-app` is answered in the language of the notes (Codex once answered in another language).
- README: use several AI tools on a project **one at a time**.
- **One-line install for Claude Code:** the repo is now a Claude Code plugin marketplace. `/plugin install multiproject-handoff --marketplace hegecalapkulu/multiproject-handoff` installs all 12 skills (no hooks; the guard stays opt-in). Tested with a real session: `/mph-resume` showed the example dashboard in 4 steps, about $0.11.
- **CI:** `scripts/check.sh` runs on every push and pull request (GitHub Actions, Ubuntu and macOS); "tests" badge in the README.

## 0.4.0 (2026-11-24)

- **Model advice** (part of the `mph-guard` hooks, on by default there): before a clearly simple, mechanical **and large** task on a large model (many files, long texts; small tasks are just done), the agent offers once to switch to a lighter one, with the exact command for the tool. The user decides; nothing is switched or delegated silently; it stays quiet if the agent can't tell which model it is. "Don't ask again" turns it off.
- **Long-conversation note:** thresholds raised to 150k / 300k / 600k tokens; the suggested command is configurable (`context_hint_command`). Tested live in Claude Code.

## 0.3.0 (2026-11-24)

- **Cheaper sessions, same information.** `mph-scan.py` (read-only, standard library) gathers in one call what used to take many steps: the dashboard, a project's load bundle, and the git facts for a handoff. It understands Turkish and English dates, paths with spaces and adopted files. Measured on a real Obsidian vault (copy, Claude Code, Sonnet): dashboard **12 → 3 steps, $0.20 → $0.10**; resume **3 steps, $0.12**.
- Skills read the rules file directly, read and edit several files in one step, and **search the notes before saying they don't know**.
- **Long-conversation hint** (`guard/mph-context.py`, part of `mph-guard`): suggests `mph-handoff` + a new session once when the conversation crosses 120k / 250k / 500k tokens.
- From testing on a real vault: adoption proposes the Obsidian module off; existing settings notes are linked with `Also follow:`; the user's own rules count as a yes; handoff asks approvals inside the plan and sticks to it; labels in the user's language.
- Windows: installer via Git Bash or WSL; `python` where `python3` is missing.

## 0.2.0 (2026-11-24)

- **Adopt existing notes.** `mph-setup-project` looks around first and maps the notes a project already has (status notes, `TODO.md`, `docs/adr/`, research folders…) where they are; nothing is moved or renamed. Works for a whole folder or Obsidian vault of projects at once, and writes `PROJECTS.md`.
- **Projects are recognized by a marker** on the first line of `PROJECT.md`, not by file names, so unrelated `RESUME.md` files or `notes/` folders are never touched. The notes folder can have any name.
- **One-screen setup** with defaults; asks only what it can't work out.
- **`mph-guard`**: optional Claude Code hook that enforces the safety rules (blocks deleting, history rewrites, reading secrets; asks before commands you name; protected folders), configured in `~/.handoff/guard.conf`. Tests in `scripts/test-guard.py`.
- Example: `landing-page` is now an adopted project with its own `notes/` folder left alone.
- Answers use the user's language, headings included.
- Real-session tests (Claude Code): dashboard, resume, handoff, and adopting an existing project with its own `notes/` folder left untouched.

## 0.1.0 (2026-11-24)

First public release.

- **Core:** `mph-resume` (multi-project dashboard, active project, drift check), `mph-handoff` (facts from git and tests, one-line plan, `quick` mode, cross-project backlog routing), `mph-setup-project`, `mph-decision-log`, `mph-daily-log`, `mph-menu`.
- **Modules:** `mph-knowledge` (topics that grow into folders, knowledge map, "organize notes"), `mph-profile` (per-project working style, promoted to general at two projects, local by default), `mph-suggest-skill` and `mph-suggest-agent` (answers remembered in `SUGGESTIONS.md`), `mph-obsidian-map` (links, tags, map notes, Canvas).
- **Shared rules** in `shared/RULES.md`, copied next to every skill and to `~/.handoff/`, with a fallback search.
- **Installer** for Claude Code, Codex, Gemini CLI, Antigravity, any folder (`--dir`), one project (`--project`) and `AGENTS.md`-based tools (`--agents-md`).
- Three-project example workspace.

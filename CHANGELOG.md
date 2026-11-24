# Changelog

## 0.2.0 (2026-11-24)

- **Adopt existing notes.** `mph-setup-project` looks around first and maps the notes a project already has (status notes, `TODO.md`, `docs/adr/`, research folders…) where they are; nothing is moved or renamed. Works for a whole folder or Obsidian vault of projects at once, and writes `PROJECTS.md`.
- **Projects are recognized by a marker** on the first line of `PROJECT.md`, not by file names, so unrelated `RESUME.md` files or `notes/` folders are never touched. The notes folder can have any name.
- **One-screen setup** with defaults; asks only what it can't work out.
- **`mph-guard`**: optional Claude Code hook that enforces the safety rules (blocks deleting, history rewrites, reading secrets; asks before commands you name; protected folders), configured in `~/.handoff/guard.conf`. Tests in `scripts/test-guard.py`.
- Example: `landing-page` is now an adopted project with its own `notes/` folder left alone.
- First real-session test (Claude Code): `mph-resume` and `mph-handoff` answers kept within their length limits.

## 0.1.0 (2026-11-24)

First public release.

- **Core:** `mph-resume` (multi-project dashboard, active project, drift check), `mph-handoff` (facts from git and tests, one-line plan, `quick` mode, cross-project backlog routing), `mph-setup-project`, `mph-decision-log`, `mph-daily-log`, `mph-menu`.
- **Modules:** `mph-knowledge` (topics that grow into folders, knowledge map, "organize notes"), `mph-profile` (per-project working style, promoted to general at two projects, local by default), `mph-suggest-skill` and `mph-suggest-agent` (answers remembered in `SUGGESTIONS.md`), `mph-obsidian-map` (links, tags, map notes, Canvas).
- **Shared rules** in `shared/RULES.md`, copied next to every skill and to `~/.handoff/`, with a fallback search.
- **Installer** for Claude Code, Codex, Gemini CLI, Antigravity, any folder (`--dir`), one project (`--project`) and `AGENTS.md`-based tools (`--agents-md`).
- Three-project example workspace.

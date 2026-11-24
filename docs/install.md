# Install for your AI tool

[← back to README](../README.md)

```bash
git clone https://github.com/hegecalapkulu/multiproject-handoff.git
cd multiproject-handoff
./install.sh            # installs for every AI tool it finds on this machine
```

Or choose:

| You use | Command | Installs to |
|---|---|---|
| Claude Code | `./install.sh --tool claude` | `~/.claude/skills/` |
| Codex | `./install.sh --tool codex` | `~/.codex/skills/` |
| Tools using the shared `.agents` folder | `./install.sh --tool agents` | `~/.agents/skills/` |
| Gemini CLI | `./install.sh --tool gemini` | `~/.gemini/skills/` |
| Antigravity | `./install.sh --tool antigravity` | `~/.gemini/antigravity/skills/` |
| Any other skills folder | `./install.sh --dir PATH` | `PATH` |
| One project only | `./install.sh --project ~/code/app [--tool claude]` | `app/.agents/skills/` (or the tool's project folder) |
| A tool without skill support (Cursor, Copilot, Windsurf…) | `./install.sh --agents-md ~/code` | skills to `~/.handoff/skills/` + a short block in `~/code/AGENTS.md` that tells the agent which file to follow for "resume", "handoff", … |

Skill folders differ between tools and change between versions. If your tool doesn't see the skills, check its docs and use `--dir`. `--dry-run` shows what would happen without changing anything.

The installer **never deletes anything**, skips any existing skill with the same name, appends to `AGENTS.md` only once (never overwrites it), and `--update` refreshes only what it installed itself.

Then open a project with your AI tool and say **"setup project"**.

## Safety guard

The skills *promise* not to delete files or rewrite history. The guard *enforces* it: a Claude Code `PreToolUse` hook (`~/.handoff/mph-guard.py`, placed by the installer but inactive until you set it up) that runs before every command and file change.

Run `mph-guard` and pick from a short checklist:

| Choice | Default | What it does |
|---|---|---|
| `block_delete` | on | blocks deleting commands and deleting from scripts; can suggest a "to delete" folder instead |
| `block_history` | on | blocks force push, hard resets, rebase, amend |
| `block_secrets` | on | blocks reading `.env` files and dumping environment variables |
| `ask_push` | off | asks before every `git push` |
| `ask_commands` | empty | asks before commands containing these words (`deploy.sh`, `npm publish`) |
| `protect_paths` | empty | no edits or writes inside these folders |

Choices live in `~/.handoff/guard.conf`; change them any time by running `mph-guard` again. Registering the hook is shown to you first and needs your yes; existing hooks are never removed. Other tools (Codex, Gemini CLI, Cursor) have their own approval or sandbox settings; use those there.

Test it yourself: `python3 scripts/test-guard.py`.

## Windows

- **The skills** are plain Markdown and work the same on Windows.
- **The installer** is a shell script. Run it from **Git Bash** (it comes with Git for Windows, which Claude Code on Windows already uses): `./install.sh`. WSL works too.
- **The scanner, guard and context hint** are Python (standard library only). Where `python3` is not a command, the agent uses `python` (or `py`) instead.
- **Registering the guard on Windows:** use the full path in the hook command, for example `python %USERPROFILE%\\.handoff\\mph-guard.py`; `mph-guard` does this for you.

Tested so far on macOS. Reports from Windows and Linux users are very welcome.


# Install for your AI tool

[← back to README](../README.md)

## Claude Code plugin (one line)

Type this inside Claude Code (version 2.1.275 or later):

```
/plugin install multiproject-handoff --marketplace hegecalapkulu/multiproject-handoff
```

On older versions, two lines:

```
/plugin marketplace add hegecalapkulu/multiproject-handoff
/plugin install multiproject-handoff@multiproject-handoff
```

Start a new session and the 12 `mph-` skills are there (`/mph-resume`, `/mph-handoff`, …). Each skill carries its own copy of the shared rules, so nothing else is needed. The plugin adds no hooks: the safety guard stays off until you run `mph-guard`. To update: `/plugin update multiproject-handoff`.

## Let your AI tool install it

Paste this into any agent that can run commands (Codex, Cursor, Gemini CLI, Antigravity, Claude Code…):

```text
Install multiproject-handoff (https://github.com/hegecalapkulu/multiproject-handoff) for the AI tool you are running in: clone the repo, run `./install.sh --dry-run` and show me what it would change, then install it for this tool after I say yes. Finally, tell me how to start.
```

It shows you what would change before installing anything.

## Install script (every tool)

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

## Uninstall

**Nothing is deleted.** Everything the installer put on your machine is moved to `~/.handoff-removed/<date-time>/`, so you can put it back. Your project notes (`PROJECT.md`, resume notes, backlog, decisions, logs) are never touched: they stay as plain Markdown you can keep reading.

**Step 1: Claude Code plugin.** If you installed the plugin, type in Claude Code:

```
/plugin uninstall multiproject-handoff
/plugin marketplace remove multiproject-handoff
```

**Step 2: everything else.** Needed if you used `install.sh`, or set up the safety guard (also with the plugin). From the repo folder (`git clone` it again if you deleted it):

```bash
./install.sh --uninstall --dry-run     # shows what it would move, changes nothing
./install.sh --uninstall               # asks once, then moves it
```

| It moves | It keeps |
|---|---|
| skill folders our installer marked (`.multiproject-handoff` file inside), in every tool's skills folder | skills that are not ours, even with the same name |
| our files in `~/.handoff/` (`RULES.md`, scripts, `guard.conf`) | your files there, such as `working-style.md` or `PROJECTS.md` |
| the guard and long-conversation entries in `~/.claude/settings.json` (a copy of the file is kept) | every other setting and hook |
| the block in `AGENTS.md`, if you add `--agents-md DIR` (a copy is kept) | the rest of `AGENTS.md` |

Installed inside one project? Add `--project DIR`. A skills folder you named? Add `--dir PATH`. Agents can add `--yes` after showing you the dry run.

**Step 3: restart your AI tools.** When you are sure you won't need it, delete `~/.handoff-removed/` yourself.

**Let your AI tool do it:**

```text
Uninstall multiproject-handoff (https://github.com/hegecalapkulu/multiproject-handoff) from this machine: get the repo, run `./install.sh --uninstall --dry-run` and show me what it would change, then run `./install.sh --uninstall --yes` after I say yes. Keep my project notes.
```

**Your notes afterwards:** they keep working as ordinary Markdown. If you want them gone too, delete the notes folder yourself; the first line of `PROJECT.md` (`<!-- mph:project … -->`) is only a marker and can stay or go.

## Safety guard

The skills *promise* not to delete files or rewrite history. The guard *enforces* it: a Claude Code `PreToolUse` hook (plus a `UserPromptSubmit` hook for the long-conversation note and the model advice) (`~/.handoff/mph-guard.py`, placed by the installer but inactive until you set it up) that runs before every command and file change.

Run `mph-guard` and pick from a short checklist:

| Choice | Default | What it does |
|---|---|---|
| `block_delete` | on | blocks deleting commands and deleting from scripts; can suggest a "to delete" folder instead |
| `block_history` | on | blocks force push, hard resets, rebase, amend |
| `block_secrets` | on | blocks reading `.env` files and dumping environment variables |
| `ask_push` | off | asks before every `git push` |
| `ask_commands` | empty | asks before commands containing these words (`deploy.sh`, `npm publish`) |
| `protect_paths` | empty | no edits or writes inside these folders |
| `context_hint` | on | once per threshold, a note when the conversation gets long, and the agent suggests a handoff |
| `context_hint_tokens` | 500000,800000 | the thresholds, for 1M-window models; with a 200k-window model use `150000` (below where it gets compacted) |
| `context_hint_command` | mph-handoff | the command it suggests (use your own, e.g. `/devir`) |
| `model_advice` | on | before a clearly simple task on a large model, the agent offers once to switch to a lighter one; you decide |

Choices live in `~/.handoff/guard.conf`; change them any time by running `mph-guard` again. Registering the hook is shown to you first and needs your yes; existing hooks are never removed. Other tools (Codex, Gemini CLI, Cursor) have their own approval or sandbox settings; use those there.

Test it yourself: `python3 scripts/test-guard.py`.

## Windows

- **The skills** are plain Markdown and work the same on Windows.
- **The installer** is a shell script. Run it from **Git Bash** (it comes with Git for Windows, which Claude Code on Windows already uses): `./install.sh`. WSL works too.
- **The scanner, guard and context hint** are Python (standard library only). Where `python3` is not a command, the agent uses `python` (or `py`) instead.
- **Registering the guard on Windows:** use the full path in the hook command, for example `python %USERPROFILE%\\.handoff\\mph-guard.py`; `mph-guard` does this for you.

Tested so far on macOS. Reports from Windows and Linux users are very welcome.


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

# multiproject-handoff

**Juggling several projects with AI coding agents? Stop re-explaining each one every session.**

`multiproject-handoff` is a set of plain-Markdown skills that turn the end of a session into a clean handoff and the start of the next one into a 10-second resume, **across all your projects at once**. It works with Claude Code, Codex, Gemini CLI, Antigravity, Cursor, Copilot, or any agent that can read a file and follow instructions.

```
> resume

You have 3 projects with notes:

1. recipe-app      updated 1 day ago
   Search works, 41 tests pass; shopping list half done. Now: finish "remove item".
2. landing-page    updated 6 days ago
   Waiting on headline copy from the client. Now: hero section.
3. cli-tool        updated 23 days ago  ⚠ stale
   v0.2 released; next is Windows support. Now: Windows CI runner.

Which one? (number or name)
```

…work…

```
> handoff
  facts checked from git and tests · daily log appended · decision recorded
  · backlog updated (one item routed to cli-tool) · resume note rewritten · committed
```

No server, no database, no account. Markdown files next to your code, and instructions any agent can follow.

---

## The problem

Sessions end, get compacted, or you switch tools. The next session starts cold, so you either paste the same background again, let the agent re-read half the codebase, or watch it **undo a decision** you made last week because it doesn't know *why* you made it.

It gets worse with several projects: which one was blocked, which one did you forget, where did that idea for the other project go?

## How it works

Each project gets a small `notes/` folder. Each file has one job and its own lifecycle:

```
recipe-app/
└── notes/
    ├── PROJECT.md      settings for this project: check command, paths, push or not, "never do X"
    ├── RESUME.md       ≤60 lines: where we are · tried, didn't work · open questions · next steps
    ├── BACKLOG.md      open work only (Now / Next / Later)
    ├── DECISIONS.md    every decision + date + one-sentence "why"
    └── daily/
        └── 2026-11-23.md   append-only log of what happened
```

| File | Changes how | Read when |
|---|---|---|
| `RESUME.md` | Rewritten short at every handoff | Every resume (the first line feeds the dashboard) |
| `BACKLOG.md` | Finished items leave, new ones arrive | Only the `Now` section |
| `DECISIONS.md` | A changed decision replaces the old one, with "(previously: …)" | When a decision matters |
| `daily/*.md` | Append-only | Rarely: it's the history |

**The resume note stays tiny because everything else has a home.** Before anything leaves `RESUME.md`, the handoff moves it to the daily log or the decision file. Nothing gets lost, and the next session reads one short file instead of your whole history.

## Where the files live

The notes always live in a `notes/` folder **inside each project**, so they are versioned with the code. How you arrange the projects is up to you. Pick one of three layouts:

**1. One parent folder (simplest).** All projects under one folder. Open your AI tool there; `resume` finds every `*/notes/RESUME.md` up to two levels deep.

```
~/code/
├── recipe-app/notes/
├── landing-page/notes/
└── clients/acme/cli-tool/notes/
```

**2. Projects scattered around the disk.** Put a `PROJECTS.md` in the folder where you open your AI tool, or in `~/.handoff/PROJECTS.md` to use it everywhere:

```markdown
- recipe-app: ~/code/recipe-app
- landing-page: ~/clients/acme/landing-page
- thesis: ~/Documents/thesis
```

**3. Notes apart from the code** (for example an Obsidian vault for notes, repos elsewhere). Keep `notes/` in the vault and point to the code from `PROJECT.md`:

```markdown
| Code | `~/code/recipe-app` |
```

Checks and git commands then run in the code folder; notes stay in the vault.

## Does it split work into projects automatically?

It keeps work **separated** by project automatically. It does not invent projects on its own.

- **Notes go to the right project.** At handoff, the agent works out which project the session was about from the files it touched, confirms in one sentence, and writes only into that project's notes. If the session touched two projects, it asks whether to hand off both, each into its own notes.
- **Ideas go to the project they belong to.** If, while working on `recipe-app`, you say "the CLI needs the same fix", that item goes into **`cli-tool`'s** backlog, not recipe-app's, and the report tells you.
- **New work is caught.** If the session worked in a folder that has no notes yet, handoff asks: new project (`setup project`) or part of an existing one?
- **Forgotten work is flagged.** Projects untouched for 14 days show as **⚠ stale** on the dashboard.

What it won't do: break a big idea into several projects for you, or create a project without asking. You decide what a project is; it keeps them apart.

## Where decisions are stored

By default in each project's `notes/DECISIONS.md`:

```markdown
## Tech
- **SQLite full-text search instead of a search service** (2026-11-20). Why: one file, no extra server, fast enough for <100k recipes. (previously: Algolia)
```

- Every decision has a date and a one-sentence **why**, so a later session won't "helpfully" undo it.
- A changed decision **replaces** the old one and keeps "(previously: …)". Full history is in git.
- A suggestion is not a decision: it's only written after you agree.
- Bigger projects can split decisions by topic with a map in `PROJECT.md` (`pricing → notes/decisions/pricing.md`, `architecture → docs/architecture.md`).

## The skills

Each skill is a standard [`SKILL.md`](https://agentskills.io) file. In tools with slash commands, type `/resume`; elsewhere, just say "resume".

| Skill | What it does |
|---|---|
| `setup-project` | Creates `notes/` for a project from its README and git history, asks 3 questions, adds it to `PROJECTS.md` if you keep one. Never overwrites. |
| `resume [project]` | With several projects: a one-screen dashboard first. Then reads `PROJECT.md`, `RESUME.md` and the backlog's `Now`, warns about commits since the last handoff, answers in ≤8 lines. Read-only. |
| `handoff [project]` | Finds the right project, checks facts from git and tests (not from memory), appends the daily log, records decisions, routes backlog items to the right project, rewrites the resume note, commits. |
| `daily-log` | Today's log without the full handoff. |
| `decision-log` | Records a decision with its reason, replacing the old one if it changed. |
| `suggest-skill` | Spots work you repeated by hand in the session and suggests ≤3 new skills, with evidence. Rule of three: the third time becomes a skill. |

## Install

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

## Try it in 1 minute

[`examples/workspace/`](examples/workspace/) holds three filled-in projects: exactly what the dashboard above reads. After installing, open your AI tool in that folder and say "resume".

## Safety rules built into every skill

- **Never delete files.** Notes are edited or appended. Old versions live in git.
- **Never rewrite git history.** No force push, no reset. A failed push is reported, not "fixed".
- **Never claim work that didn't happen.** "Tests pass" is only written if they passed during the handoff.
- **You decide.** The agent's suggestion is not a decision until you agree.
- **No secrets in notes.** No keys, passwords or real customer data.

## How is this different from other handoff / memory-bank tools?

There are good tools in this space, and some ideas here come from them. Most do one of two things: **one handoff file for one project**, or a **memory bank** of context files for a single project, often tied to one tool. `multiproject-handoff` differs in four ways:

1. **Many projects, one command:** the dashboard, `resume <project>`, stale warnings, a handoff that knows which project it is closing, and backlog items routed to the right project.
2. **Each kind of information has its own lifecycle,** so the file the next session reads stays under 60 lines after months of work.
3. **Per-project settings instead of per-project skills:** one `PROJECT.md` changes paths, checks and rules; the skills stay the same everywhere.
4. **Not tied to one AI tool:** start a project in Claude Code, continue it in Codex or Gemini tomorrow. The notes are the same.

## FAQ

**My tool already has memory.**
Use it for preferences. This is for project *state*, which changes every day and belongs in the repo, next to the code, where it's versioned and shared with every tool and teammate.

**Why Markdown files and not a database or an MCP server?**
You can read them, diff them, edit them by hand and open them in Obsidian. If you stop using this tomorrow, your notes still make sense.

**Can I change the folder layout?**
Yes: write the paths in `notes/PROJECT.md` and every skill follows them.

## Contributing

Issues and PRs are welcome, especially:
- confirmed skill-folder paths for more tools
- `PROJECT.md` examples for different stacks
- changes that make `resume` read *less*
- translations

## License

MIT

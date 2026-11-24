# claude-handoff

**Stop re-explaining your project to Claude every session.**

`claude-handoff` is a small set of [Claude Code](https://claude.com/claude-code) skills that turn the end of a session into a clean handoff and the start of the next one into a 10-second resume. It's built for people who juggle **several projects at once** and keep losing context between them.

```
/resume

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
/handoff   → facts checked from git and tests · daily log appended · decision recorded
             · backlog updated · resume note rewritten · committed
```

No server, no database, no extra service. Just Markdown files in your repo and plain-English skills Claude follows.

---

## The problem

Long sessions get compacted or closed. A new session starts cold, so you either:

- paste the same background again, or
- let Claude re-read half the codebase (slow, expensive), or
- watch it **undo a decision** you made two days ago because it doesn't know *why* you made it.

Built-in memory helps with preferences. It doesn't keep **project state**: where the work stopped, what's open, what was decided and why.

## How it works

Each project gets a small `notes/` folder:

```
your-project/
└── notes/
    ├── PROJECT.md      ← per-project settings: check command, paths, push or not, "never do X"
    ├── RESUME.md       ← ≤60 lines: where we are · open questions · next steps
    ├── BACKLOG.md      ← open work only (Now / Next / Later)
    ├── DECISIONS.md    ← every decision + one-sentence "why"
    └── daily/
        └── 2026-11-23.md   ← append-only log of what happened
```

Each file has one job:

| File | Changes how | Read when |
|---|---|---|
| `RESUME.md` | Rewritten short at every handoff | Every `/resume` |
| `BACKLOG.md` | Finished items leave, new ones arrive | Only the `Now` section on resume |
| `DECISIONS.md` | Old decisions are replaced, with "(previously: …)" | When a decision matters |
| `daily/*.md` | Append-only | Rarely; it's the history |

The key idea: **the resume note stays tiny because everything else has a home.** Before anything leaves `RESUME.md`, the handoff moves it to the daily log or the decision file. Nothing gets lost, and the next session reads one short file instead of your whole history.

### Several projects in one folder

Keep all your projects under one folder (a `~/code` directory, an Obsidian vault, a monorepo) and open Claude Code there:

- **`/resume`** finds every `*/notes/RESUME.md` (two levels deep), reads only the first lines of each and shows the dashboard above, newest first. Projects you haven't touched in 14 days are marked **⚠ stale**, so nothing quietly dies.
- **`/resume recipe-app`** skips the dashboard and opens that project directly.
- **`/handoff`** works out which project the session was about from the files it touched, confirms in one sentence, and writes only into that project's notes. If the session touched two projects, it asks whether to hand off both.

Opening Claude Code inside a single project works too: then `/resume` goes straight to it.

### Where decisions are stored

By default every decision goes to the project's `notes/DECISIONS.md`, in this format:

```markdown
## Tech
- **SQLite full-text search instead of a search service** (2026-11-20). Why: one file, no extra server, fast enough for <100k recipes. (previously: Algolia)
```

- Every decision has a date and a one-sentence **why**, so a later session won't "helpfully" undo it.
- A changed decision **replaces** the old one and keeps a short "(previously: …)". The full history is in git.
- Suggestions are not decisions: a decision is only written after you agree.
- Bigger projects can split decisions by topic. Add a map to `PROJECT.md`, for example `pricing → notes/decisions/pricing.md`, `architecture → docs/architecture.md`, and `/decision-log` files each decision in the right place.

### One set of skills, any number of projects

The skills are generic. Everything project-specific lives in `notes/PROJECT.md`, which **overrides the defaults**: a different test command, a different folder layout, "push after every handoff", "never touch the production database". Add a new project and you add one file, not a new set of skills.

## The skills

| Skill | What it does |
|---|---|
| `/setup-project` | Creates the `notes/` folder for a project, filled from its README and git history. Asks you 3 questions. Never overwrites. |
| `/resume [project]` | Starts a session. With several projects: a one-screen dashboard first. Then reads `PROJECT.md`, `RESUME.md` and the `Now` part of the backlog, warns if commits happened since the last handoff, answers in ≤8 lines. Read-only. |
| `/handoff [project]` | Ends a session: finds the right project, checks the facts from git and tests (not from memory), appends the daily log, records decisions, updates the backlog, rewrites the resume note (including what was tried and failed), commits. |
| `/daily-log` | Writes today's log without the full handoff. |
| `/decision-log` | Records a decision with its reason, replacing the old one if it changed. |
| `/suggest-skill` | Looks at the session for work you repeated by hand and suggests ≤3 new skills, with evidence. Rule of three: the third time is a skill. |

## Install

```bash
git clone https://github.com/hegecalapkulu/claude-handoff.git
cd claude-handoff
./install.sh
```

That copies the skills to `~/.claude/skills/` so they work in every project. To install for a single project instead:

```bash
./install.sh --project ~/code/my-app
```

The installer **never deletes anything** and skips any existing skill with the same name. Use `--update` to refresh skills it installed before.

Then open a project in Claude Code and type:

```
/setup-project
```

## Safety rules built into every skill

These come from running this system daily on real projects:

- **Never delete files.** Notes are edited or appended. Old versions live in git.
- **Never rewrite git history.** No force push, no reset. A failed push is reported, not "fixed".
- **Never claim work that didn't happen.** Failing tests go in the resume note, in plain words.
- **The user decides.** Claude's suggestion is not a decision until you agree.
- **No secrets in notes.** No keys, passwords or real customer data.

## Example

[`examples/workspace/`](examples/workspace/) is a folder with three filled-in projects: exactly what the dashboard above reads. Open Claude Code in that folder after installing and type `/resume` to try it without touching your own projects.

## How is this different from other handoff / memory-bank tools?

There are good tools in this space, and some ideas here came from them. Most of them do one of two things: **one handoff file for one project** (a `HANDOFF.md` you paste into the next session) or a **memory bank** (several context files a single project keeps up to date). `claude-handoff` differs in three ways:

1. **Many projects, one command.** The dashboard, `/resume <project>`, stale warnings, and a handoff that knows which project it is closing.
2. **Each kind of information has a lifecycle.** Resume note: rewritten and short. Backlog: open items only. Decisions: replaced, with the reason. Daily log: append-only. That's why the file the next session reads stays under 60 lines after months of work.
3. **Per-project overrides instead of per-project skills.** One `PROJECT.md` changes paths, checks and rules; the skills stay the same everywhere.

## FAQ

**Doesn't Claude Code already have memory?**
Yes, and use it for preferences ("I like small commits"). `claude-handoff` is for project *state*, which changes every day and belongs in the repo next to the code, where it's versioned and shared.

**Why Markdown files and not a database or an MCP server?**
Because you can read them, diff them, edit them by hand and open them in Obsidian. If you stop using this tool tomorrow, your notes still make sense.

**Does it work with Obsidian?**
Yes. A `notes/` folder (or a whole vault of projects) opens fine in Obsidian. Point `PROJECT.md` at any paths you like.

**Can I change the folder layout?**
Yes. Write the paths in `notes/PROJECT.md` and every skill follows them.

## Contributing

Issues and PRs are welcome, especially:
- `PROJECT.md` examples for different stacks
- improvements that make `/resume` read *less*
- translations of the skills

## License

MIT

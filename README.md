# claude-handoff

**Stop re-explaining your project to Claude every session.**

`claude-handoff` is a small set of [Claude Code](https://claude.com/claude-code) skills that turn the end of a session into a clean handoff and the start of the next one into a 10-second resume. It's built for people who juggle **several projects at once** and keep losing context between them.

```
/resume    → "Where we are: search works, 41 tests pass. Next: finish 'remove item'. Continue?"
  ...work...
/handoff   → tests checked · daily log appended · decision recorded · backlog updated · resume note rewritten · committed
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

### One set of skills, any number of projects

The skills are generic. Everything project-specific lives in `notes/PROJECT.md`, which **overrides the defaults**: a different test command, a different folder layout, "push after every handoff", "never touch the production database". Add a new project and you add one file, not a new set of skills.

## The skills

| Skill | What it does |
|---|---|
| `/setup-project` | Creates the `notes/` folder for a project, filled from its README and git history. Asks you 3 questions. Never overwrites. |
| `/resume` | Starts a session: reads `PROJECT.md`, `RESUME.md` and the top of the backlog. Answers in ≤8 lines and asks what to do. Read-only. |
| `/handoff` | Ends a session: runs the check command, appends the daily log, records decisions, updates the backlog, rewrites the resume note, commits. |
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

See [`examples/recipe-app/notes/`](examples/recipe-app/notes/) for a filled-in project: a resume note, a backlog, a decision that replaced an earlier one, and a daily log.

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

# How it works

[← back to README](../README.md)

## The big picture: five layers

| Layer | Question it answers | Where | Skills |
|---|---|---|---|
| 1. Handoff | Where did we stop? | `RESUME.md`, `BACKLOG.md`, `daily/` | `mph-resume`, `mph-handoff`, `mph-daily-log` |
| 2. Memory | What did we choose, and what did we learn? | `decisions/`, `knowledge/` | `mph-decision-log`, `mph-knowledge` |
| 3. You | How should the agent work with you here? | `working-style.md`, `~/.handoff/working-style.md` | `mph-profile` |
| 4. Growth | What should be automated next? | `SUGGESTIONS.md`, project skills and agents | `mph-suggest-skill`, `mph-suggest-agent` |
| 5. View | How do I see it all? | `_map.md`, `map.canvas`, the menu | `mph-obsidian-map`, `mph-menu` |

One file ties the layers together: each project's `notes/PROJECT.md` (checks, modules, maps, structure rules, project skills and agents). One file ties the skills together: [`shared/RULES.md`](../shared/RULES.md) (finding projects, the active project, modules, reports, safety).

### A session, step by step

1. `mph-resume` → dashboard → pick a project → resume note, `Now`, working style and the knowledge map are read.
2. While working: decisions go through `mph-decision-log`, research through `mph-knowledge`; items for other projects go to their backlogs.
3. `mph-handoff` → facts from git and tests → a one-line plan you confirm → only the steps with material run, each reading its own skill's rules only then → backlog and resume note → Obsidian map (if on) → commit → at most one suggestion question.
4. `mph-handoff quick` → resume note and commit only.

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

**1. One parent folder (simplest).** All projects under one folder. Open your AI tool there; `mph-resume` finds every `*/notes/RESUME.md` up to two levels deep.

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

## One question per session, not per command

Once a project is chosen (by `mph-resume`, by the first skill that needs it, or by saying "let's work on cli-tool"), it is the session's **active project**. Every skill uses it without asking again, and every report starts with `[recipe-app]` so a wrong project is obvious. It changes only when you say "switch to landing-page" or `mph-resume landing-page`.

Forgot the commands? Say **`mph-menu`**: every skill on one screen, the active project, this project's own skills and agents, and the most useful next step.

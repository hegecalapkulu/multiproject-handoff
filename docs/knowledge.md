# Notes that grow with your project

[← back to README](../README.md)

## Notes that grow with your project

A project produces three kinds of information, and each is kept differently:

| Kind | Example | Where it goes |
|---|---|---|
| **State** | "search works, remove-item is half done" | `RESUME.md`, rewritten every handoff |
| **Decisions** | "SQLite instead of Algolia, because…" | decision files, replaced when they change |
| **Knowledge** | competitor pricing, interview notes, research, strategy | **topic files that grow over time** |

Most tools only carry *state* from one session to the next. Here, knowledge that would otherwise die with the chat is filed into topics, and the structure grows as the project does:

```
week 1                          month 3
notes/                          notes/
├── RESUME.md                   ├── RESUME.md          ← still ≤60 lines
├── DECISIONS.md                ├── decisions/
└── BACKLOG.md                  │   ├── product.md
                                │   └── tech.md
                                ├── knowledge/
                                │   ├── competitors/
                                │   │   ├── _overview.md
                                │   │   ├── pantrypal.md
                                │   │   └── cookbase.md
                                │   ├── interviews/
                                │   │   └── 2026-11-21-household-1.md
                                │   └── pricing.md
                                └── BACKLOG.md
```

How it grows:

- **A new topic starts as one file.** The first time competitor research shows up, the agent proposes `knowledge/competitors.md` and creates it after your yes.
- **Big topics become folders.** When a topic passes ~150 lines or covers 4+ separate subjects, the agent proposes splitting it: one file per subject plus an `_overview.md`. Content is moved with `git mv`, every line ends up somewhere, links are fixed.
- **Decisions split the same way** when `DECISIONS.md` grows clear areas (product, tech, pricing).
- **Everything is on a map.** Each topic is listed in the `## Knowledge map` of `PROJECT.md`, so any session, in any tool, knows where things are without opening them.
- **Opening a session stays cheap.** `mph-resume` reads the map, not the topic files. A topic is opened only when the work needs it ("let's set the price" → `pricing.md`).
- **Say "organize notes"** at any time for a full review: merges, splits, archive candidates, accepted one by one.

Nothing structural happens without your OK. Filing into an existing topic is automatic; new topics, splits, merges and archives are proposals.

## Your structure, your rules

The skills ship with defaults, not opinions you have to accept. Everything about how notes are organized lives in each project's `PROJECT.md`, and every skill follows it:

```markdown
## Knowledge map
- Competitors → 02 Research/Competitors/
- Sales calls → 03 Sales/Calls/
- Architecture → docs/architecture.md

## Structure rules
- Number top-level folders: "01 Decisions", "02 Research", "03 Sales"
- Write notes in Turkish
- Split a topic into a folder at 100 lines
- Calls: one file per call, named YYYY-MM-DD-company.md
```

- **Any names, any language, any location**, including an existing Obsidian vault or `docs/` folder. `mph-setup-project` maps the folders you already have instead of creating new ones.
- **Different projects, different structures.** A client project, a thesis and a side app can each have their own map and rules; the skills stay the same.
- **Your structure is never "fixed" to fit a default.** The agent doesn't rename or move your folders unless you ask.

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

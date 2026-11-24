---
name: mph-setup-project
description: Set up multiproject-handoff for a project, or adopt the notes a project (or a whole folder or Obsidian vault of projects) already has, without moving or renaming anything. Looks around first, shows what it found and what it proposes in one short screen, asks only what it cannot work out, and writes a marked PROJECT.md. Use when the user says "mph-setup-project", "/mph-setup-project", "set up this project", "adopt my notes", or when another skill finds no project.
---

# mph-setup-project: fit into what is already there

<!-- mph:lookup:start -->
> **Shared rules first.** Read `RULES.md` before anything else. Look for it in this order and stop at the first hit:
> 1. `RULES.md` next to this `SKILL.md`, in the same folder (if this file is `…/mph-resume/SKILL.md`, read `…/mph-resume/RULES.md`, not the parent `skills/` folder; many tools state this folder as the skill's base directory). Read it directly, without searching;
> 2. `~/.handoff/RULES.md`;
> 3. a search of the home folder, a few levels deep (skip `node_modules`, `.git`, `Library`, `AppData`), for a `RULES.md` whose first line contains `multiproject-handoff RULES`.
>
> If it was found by searching, use it and tell the user where, offering to copy it back to `~/.handoff/`. If it is nowhere, say so and suggest re-running `install.sh`. Never guess the rules.
<!-- mph:lookup:end -->

Principle: **the system adapts to the user, not the other way round.** Look first, propose second, write last. One short screen of questions, with good defaults, so setup takes a minute.

## 1. Which mode?

Look at the working folder (and what the user said):

| Situation | Mode |
|---|---|
| A single project, no notes of its own | **new** |
| A single project that already has notes (resume/handoff notes, TODO or backlog, decision records, research, meeting notes, a `docs/` folder…) | **adopt** |
| A folder of several projects (a code folder, an Obsidian vault, a monorepo) | **adopt many**: run *adopt* or *new* per project, then write `PROJECTS.md` |
| A project that already has a marked `PROJECT.md` | already set up → offer to review its settings instead |

Confirm the folder and the mode in one sentence before anything else.

## 2. Look around (read-only, a few seconds)

- `README`, package/build files, `git log --oneline -15` (if git): what the project is, and its check command (tests, lint, build).
- **Existing notes**, by name *and* by content (read only the first lines):
  - resume / handoff / status notes: `HANDOFF.md`, `STATUS.md`, `NOTES.md`, `Devam Notu.md`, `Continue.md`, "where we are"-style notes;
  - backlog: `TODO.md`, `TASKS.md`, `BACKLOG.md`, `Backlog/`, `ROADMAP.md`;
  - decisions: `DECISIONS.md`, `docs/decisions/`, `docs/adr/`, `adr/`, folders named like "Decisions" or "Kararlar";
  - logs: daily/weekly report folders, `CHANGELOG.md` (only as a source, never as the daily log);
  - knowledge: `docs/`, `research/`, meeting/interview notes, numbered folders like `02 Research/`;
  - settings that other skills use (a "project settings" note, `AGENTS.md`, `CLAUDE.md`): read, never change.
- **Obsidian:** a `.obsidian/` folder in the working folder, the project or any parent folder means a vault. Hidden folders are skipped by many search tools, so check with `ls -a` on each of those folders.
- **Name clashes:** if a `notes/` folder or a `PROJECT.md` already exists **without** the marker, it is the user's. Do not write into it; choose another notes folder (`.mph/` by default, or what the user prefers).

## 3. Show one screen

Show what you found and what you propose, in this shape (adapt the wording to the user's language):

```
🧭 recipe-app: Next.js app, tests with `npm test`, git repo.

Found notes, I'd use them where they are (nothing moves or gets renamed):
  resume note  → docs/STATUS.md
  backlog      → TODO.md
  decisions    → docs/adr/            (ADR files, kept as they are)
  knowledge    → docs/research/
New, in .mph/ (notes/ is already used for something else):
  PROJECT.md (settings) · daily/ · SUGGESTIONS.md

A few choices (Enter keeps the default):
  1. Language for notes and replies: 1 English · 2 Español · 3 中文 · 4 Português · 5 Türkçe · 6 other: ___   (default: English)
  2. Modules: knowledge ✓ · profile ✓ · suggestions ✓ · obsidian ✗
  3. Push after each handoff? no
  4. Your working-style notes stay on this computer only? yes
  5. Anything I must never do here? (e.g. "never touch dist/")
  6. Safety guard (blocks deleting files, rewriting git history, reading .env)? set up / skip

OK?
```

- **In adopt / adopt many, propose `obsidian` off** even inside a vault, and say why in a few words: it adds a header block and links to many existing notes. The user can switch it on later.
- **Only ask what you could not work out.** If there is no Obsidian vault, do not mention Obsidian. If the guard is already set up on this machine, skip the guard question.
- **Language:** always ask, with the default set to the language the user writes in (or, in adopt, the language of their existing notes). Show the five options and "other" exactly as above, each language in its own name; "other" takes any language the user types. In adopt many, ask once for all projects unless the user changes one.
- In **adopt many**, show one compact block per project (found notes + proposal) and let the user accept all, or skip or change single projects.
- The user can correct any line ("decisions are in `01 Kararlar/`").

## 4. Write (after OK)

1. **`PROJECT.md`** in the notes folder, from `templates/PROJECT.md`. **First line: `<!-- mph:project <name> -->`.** If the project already has a settings note for other skills (for example a "project settings" note with a decision map, report rules or a backup command), add a line `- Also follow: <path to it>` at the top of `PROJECT.md`, and copy nothing from it: its rules then apply to every mph skill too. Write the chosen language under `## Language`. Fill `## Paths` with the adopted files (paths relative to the notes folder, e.g. `../TODO.md`), `## Modules`, check command, push, "Never" list, and the existing folders as decision and knowledge maps.
2. **Only the files that do not exist yet**, from `templates/`: a resume note if none was adopted (filled from what you learned; "Next steps" left for the user), backlog, decisions, `daily/_template.md`. Never overwrite or move an existing file.
3. **Adopted files keep their format.** Skills write into them following the style they already have (headings, language, numbering), and add only what they need.
4. **Profile:** unless the user chose to share it, append `<notes folder>/working-style*.md` to the project's `.gitignore` (append only; create the file if missing).
5. **adopt many:** write `PROJECTS.md` in the parent folder (one line per project; append only if it exists).
6. **Guard:** if the user said "set up", follow the `mph-guard` skill.
7. Commit the new files if the project is a git repo (only the files this skill created or changed).

## 5. Finish

One short report: what was adopted, what was created and where, what was left untouched. Then: "From now on: `mph-resume` to start, `mph-handoff` to end, `mph-menu` for the rest."

## Rules

- Never move, rename, delete or reformat the user's files. Adopting means **mapping**, not migrating.
- Never write into a file or folder that is not mapped in a marked `PROJECT.md`.
- Ask at most one screen of questions; everything else has a default the user can change later in `PROJECT.md`.

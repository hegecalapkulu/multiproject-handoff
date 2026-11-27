---
name: mph-handoff
description: Close the current AI coding session cleanly so the next one can pick up in seconds. Works out which project the session was about, shows a one-line plan of what it will save (and skip) for a quick OK, checks facts from git and tests, then writes only what this session actually produced. "mph-handoff quick" saves just the resume note and commits. Use when the user says "mph-handoff", "/mph-handoff", "handoff", "wrap up", "let's start a new session" or "save where we are".
---

# mph-handoff: end this session, prepare the next one

<!-- mph:lookup:start -->
> **Shared rules first.** Read `RULES.md` before anything else. Look for it in this order and stop at the first hit:
> 1. `RULES.md` next to this `SKILL.md`, in the same folder (if this file is `…/mph-resume/SKILL.md`, read `…/mph-resume/RULES.md`, not the parent `skills/` folder; many tools state this folder as the skill's base directory). Read it directly, without searching;
> 2. `~/.handoff/RULES.md`;
> 3. a search of the home folder, a few levels deep (skip `node_modules`, `.git`, `Library`, `AppData`), for a `RULES.md` whose first line contains `multiproject-handoff RULES`.
>
> If it was found by searching, use it and tell the user where, offering to copy it back to `~/.handoff/`. If it is nowhere, say so and suggest re-running `install.sh`. Never guess the rules.
<!-- mph:lookup:end -->

Goal: a fresh session understands where the project stands by reading **one short file** (`RESUME.md`).
Principle: **do only what this session produced, and read a step's detailed rules only when that step runs.**

## 1. Which project?

- `mph-handoff <name>` → that project. Otherwise the **active project** (RULES.md §2), without asking again.
- No active project → follow RULES.md §2. If work happened in a folder without a marked `PROJECT.md`, ask: "New project (`mph-setup-project` can set it up or adopt its existing notes), or part of an existing one?" A one-off question with nothing to save → say so and stop.
- If the session also touched **another** project, say so and ask: "Hand off both, or only <active>?" For both, run the steps once per project, each into its own notes.

## 2. Quick mode

`mph-handoff quick` (or "quick handoff"): rewrite the resume note (step 5.5), commit (step 6), report. Nothing else. Use it when the user just wants to leave.

**Catch-up** (started by `mph-resume` when the last session ended without a handoff): the same quick mode, but the session's work is not in this conversation, so write the resume note only from `mph-scan.py facts` (commit messages, the diff, uncommitted files), never from guesses, and mark the date line `(caught up from git)`. Commit **only the notes**: uncommitted code belongs to the user, so list it in the report instead.

## 3. Gather facts, then show the plan

1. **Facts from the repo, not from memory.** Fast path: `python3 <this skill's folder>/mph-scan.py facts <name>` (git status, diff summary, commits since the resume note, branch and remote, in one call). By hand: `git status`, `git diff --stat`, this session's `git log --oneline`. If code changed, run the check command from `PROJECT.md` (or the tests). "Tests pass" is written only if they passed now.
2. **Sort what the session produced:** code changes · decisions · knowledge (research, competitors, interviews, strategy) · working-style observations · new or finished work items · items for other projects.
3. **Show a one-line plan** and wait for OK (Enter / "yes") or a correction:

```
🧭 [recipe-app] This session: code changed (tests pass), 1 decision, competitor research.
Will do: log · decision · knowledge · backlog · resume note · commit
Skip: profile, Obsidian map (nothing new for them)
OK? (yes, or e.g. "add profile")
```

Only include steps that have material **and** whose module is on (RULES.md §3). The user's correction wins.

**Keep the plan to at most 4 lines** (5 with the git offer below), in exactly the shape above: no bullet list of every step, no explanations of each item. Details go in the final report, not the plan.

If a step will need something the user must approve (a new decision file, a new topic), **ask it inside the plan** ("New decision file `01 Kararlar/Gönderim.md`?"), not after the work.

**No git yet? Offer it once, rarely.** If the code folder is not inside a git repo (`mph-scan.py facts` says `not a git repo`), read the `Git:` line under `## Commit / backup` in `PROJECT.md`:
- no line, or `not now` → add **one line** to the plan, before `OK?`, in the user's language:
  `No backup yet: this folder has no git. Start it? Every handoff then saves a version you can go back to, so a bad change (yours or the AI's) can always be undone. It stays on this computer. (yes / not now / never)`
- `on` or `never` → say nothing about git. Never ask in `quick` mode.
- If `git` itself is not installed, say so in that line instead ("git is not installed: git-scm.com, then say 'start git'") and record nothing.

The answer goes with the plan's OK. See step 6 for what each answer does. Whenever the user says "start git", do the `yes` path.

**Do exactly the confirmed plan.** If something new comes up while writing, put it in the report as a suggestion; do not act on it.

## 4. Steps (read the linked skill's rules only for the steps that run)

| Step | Runs when | Detailed rules in |
|---|---|---|
| 5.1 Daily log | anything was done | `mph-daily-log` |
| 5.2 Decisions | a decision was made | `mph-decision-log` |
| 5.3 Knowledge | module on and lasting knowledge came up | `mph-knowledge` |
| 5.4 Working style | module on and something new was clearly observed | `mph-profile` |
| 5.5 Backlog + resume note | always | below |
| 5.6 Obsidian map | module on | `mph-obsidian-map` (only the notes changed now) |
| 5.7 Suggestion question | module on | below |

To read a linked skill, open `../<skill-name>/SKILL.md` next to this skill's folder (read all the needed ones in one step). If it is not there, look in the same skills folders RULES.md was searched in.

## 5. The steps

**5.1–5.4** as planned, following each skill's rules. Prepare all the changes first, then **apply the edits to different files together in one step** (RULES.md §5); this is where most of a handoff's cost is.

**5.5 Backlog and resume note**
- Backlog: remove finished items (they are in the daily log now), add new ones to the right section. **Items for another project go to that project's backlog**; mention them in the report.
- Resume note: read it, rewrite it short (default ≤60 lines: Where we are · Tried, didn't work · Open questions · Next steps), "Last updated: YYYY-MM-DD" on top. The first line under "Where we are" feeds the dashboard: make it the most useful sentence. Anything removed from the note must already be in the log or a decision/knowledge file.

**5.7 Suggestion question** (at most one per handoff)
Read `notes/SUGGESTIONS.md` and skim the last ~10 daily logs, one line each. If one pattern of repeated manual work (→ `mph-suggest-skill`) or heavy, noisy work (→ `mph-suggest-agent`) meets the rule of three and is not blocked by a past answer, add one line to the report: "You rebuilt test data by hand in 3 of the last 5 sessions. Want a skill for it? (yes / no / never / later)". Otherwise say nothing.

## 6. Commit and report

- Commit: the backup command from `PROJECT.md` if there is one; otherwise, in a git repo, add the notes and finished work and commit with a short message (git-ignored files such as local profiles stay out). Push only if `PROJECT.md` says so.
- **Git offer answers** (only if it was in the plan), recorded under `## Commit / backup` in `PROJECT.md` (add or replace the one `- Git:` line):
  - `yes` → `git init` in the code folder (the notes folder too, if it lies outside it). Before the first commit, append to `.gitignore` (create it if missing, never remove lines): `.env`, `.env.*`, `node_modules/`, and the profile line from setup if the profile is local. List what will be committed; leave out anything that looks like a secret (keys, tokens, `*.pem`) or is over 50 MB, and say what you left out. Commit as `Start version history`. Record `- Git: on (since YYYY-MM-DD)`. Push nothing; putting it on GitHub is a separate step the user starts.
  - `not now` → record `- Git: not now (asked YYYY-MM-DD)`; the next handoff asks again.
  - `never` → record `- Git: never`. Not asked again; the user can still say "start git".
  - Without git, the notes are still written; the report says "saved, no version history" only on the handoff that asked.
- Report, starting with `🧭 [project]`: what was saved where, anything failing or unfinished, items sent to other projects, and how to start next time: `mph-resume` (or `mph-resume <name>` in a folder with several projects).

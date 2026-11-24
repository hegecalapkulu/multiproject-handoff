---
name: mph-handoff
description: Close the current AI coding session cleanly so the next one can pick up in seconds. Works out which project the session was about, shows a one-line plan of what it will save (and skip) for a quick OK, checks facts from git and tests, then writes only what this session actually produced. "mph-handoff quick" saves just the resume note and commits. Use when the user says "mph-handoff", "/mph-handoff", "handoff", "wrap up", "let's start a new session" or "save where we are".
---

# mph-handoff: end this session, prepare the next one

<!-- mph:lookup:start -->
> **Shared rules first.** Read `RULES.md` before anything else. Look for it in this order and stop at the first hit:
> 1. `RULES.md` in this skill's own folder;
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

## 3. Gather facts, then show the plan

1. **Facts from the repo, not from memory.** In a git repo: `git status`, `git diff --stat`, this session's `git log --oneline`. If code changed, run the check command from `PROJECT.md` (or the tests). "Tests pass" is written only if they passed now.
2. **Sort what the session produced:** code changes · decisions · knowledge (research, competitors, interviews, strategy) · working-style observations · new or finished work items · items for other projects.
3. **Show a one-line plan** and wait for OK (Enter / "yes") or a correction:

```
🧭 [recipe-app] This session: code changed (tests pass), 1 decision, competitor research.
Will do: log · decision · knowledge · backlog · resume note · commit
Skip: profile, Obsidian map (nothing new for them)
OK? (yes, or e.g. "add profile")
```

Only include steps that have material **and** whose module is on (RULES.md §3). The user's correction wins.

**Keep the plan to at most 4 lines**, in exactly the shape above: no bullet list of every step, no explanations of each item. Details go in the final report, not the plan.

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

To read a linked skill, open `../<skill-name>/SKILL.md` next to this skill's folder. If it is not there, look in the same skills folders RULES.md was searched in.

## 5. The steps

**5.1–5.4** as planned, following each skill's rules.

**5.5 Backlog and resume note**
- Backlog: remove finished items (they are in the daily log now), add new ones to the right section. **Items for another project go to that project's backlog**; mention them in the report.
- Resume note: read it, rewrite it short (default ≤60 lines: Where we are · Tried, didn't work · Open questions · Next steps), "Last updated: YYYY-MM-DD" on top. The first line under "Where we are" feeds the dashboard: make it the most useful sentence. Anything removed from the note must already be in the log or a decision/knowledge file.

**5.7 Suggestion question** (at most one per handoff)
Read `notes/SUGGESTIONS.md` and skim the last ~10 daily logs, one line each. If one pattern of repeated manual work (→ `mph-suggest-skill`) or heavy, noisy work (→ `mph-suggest-agent`) meets the rule of three and is not blocked by a past answer, add one line to the report: "You rebuilt test data by hand in 3 of the last 5 sessions. Want a skill for it? (yes / no / never / later)". Otherwise say nothing.

## 6. Commit and report

- Commit: the backup command from `PROJECT.md` if there is one; otherwise, in a git repo, add the notes and finished work and commit with a short message (git-ignored files such as local profiles stay out). Push only if `PROJECT.md` says so.
- Report, starting with `🧭 [project]`: what was saved where, anything failing or unfinished, items sent to other projects, and how to start next time: `mph-resume` (or `mph-resume <name>` in a folder with several projects).

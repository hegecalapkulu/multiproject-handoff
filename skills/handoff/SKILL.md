---
name: handoff
description: Close the current AI coding session cleanly (Claude Code, Codex, Gemini, Cursor, Copilot or any agent that follows these instructions) so the next session can pick up in seconds. Works out which project the session was about (also when several projects share one folder), checks the real state from git and tests, appends the daily log, records decisions, updates the backlog, rewrites a short resume note and commits. Use when the user says "handoff", "/handoff", "/handoff <project>", "wrap up", "let's start a new session" or "save where we are".
---

# Handoff: end this session, prepare the next one

The goal: a fresh session should understand where the project stands by reading **one short file** (`RESUME.md`), not by replaying this conversation.

## 0. Which project was this session about?

Projects are found as in the `resume` skill ("Finding projects"): a `PROJECTS.md` list first, then a scan for `*/notes/RESUME.md`. A project's code may live elsewhere (the `Code` entry in its `PROJECT.md`); run git and checks there.

- **`/handoff <name>`** → that project (matched by folder name, case-insensitive).
- **An active project is set in this session** (by `resume`, by an earlier skill, or by the user naming it; see "The active project" in the `resume` skill) → use it. Do not ask again. Still check that the session's work did not also touch another project (point 3 in the list below).
- **The working folder itself has `notes/`** → that is the project.
- **Otherwise** (the session ran in a folder with several projects):
  1. Look at which project folders this session actually changed or read: files edited, commands run, paths mentioned. Also check `git status` in each candidate.
  2. **One clear candidate** → confirm in one sentence: "This session was about **recipe-app**. Handing that off?" Continue on yes.
  3. **Work touched several projects** → list them and ask: "This session touched recipe-app and cli-tool. Hand off both, or only one?" If both, run the steps below once per project, each into its own notes.
  4. **Work happened in a folder that has no notes** → ask: "This looks like a new project (`<folder>`). Set it up with setup-project, or file this work under an existing project?"
  5. **No candidate** (a one-off question) → say there is nothing to hand off and stop.
- If the chosen project has no `notes/` folder yet, do not create it silently. Ask: "This project has no notes setup yet. Shall I run setup-project?"

Then read the project's `notes/PROJECT.md` if it exists. **Paths, check commands and extra steps written there override every default below.** Defaults:

- Resume note: `notes/RESUME.md`
- Daily log: `notes/daily/YYYY-MM-DD.md`
- Backlog: `notes/BACKLOG.md`
- Decisions: `notes/DECISIONS.md`

## 1. Get the facts from the repo, not from memory

At the end of a long session, memory is at its least reliable. Before writing anything:

- If the project is a git repo, run `git status`, `git diff --stat` and `git log --oneline` for this session's commits. Write what **actually** changed.
- If code changed, run the project's check command (from `PROJECT.md`; otherwise the test suite if there is one). "Tests pass" is only written if they passed **during this handoff**. If they fail, fix them first or write plainly that they are failing.
- Anything you cannot verify (for example "the client liked it") is written as reported by the user, not as fact.

## 2. Write the notes

First sort what this session produced into **state** (where we are → resume note), **decisions** (what we chose and why → decision files) and **knowledge** (research, competitors, interviews, strategy, anything worth looking up again → topic files). Knowledge that only lives in the chat is lost at the end of the session, so look for it on purpose.

1. **Daily log.** Append a short entry to today's log (at most ~8 bullets: done, decided, blocked). Use the template if the project has one. Only append, never rewrite earlier entries. Skip if nothing was done.
2. **Decisions.** If a decision was made, record it with the `decision-log` skill rules (read the target file first).
3. **Knowledge.** File lasting knowledge with the `knowledge` skill rules: into existing topics directly; new topics, splits and other structure changes only after the user's OK (ask once, listing all proposals together). The daily log gets one line pointing to where it went.
4. **Working style.** If something new and clearly observed about how the user works came up, update the profiles with the `profile` skill rules (project first; promote to general when the same item is in two projects). Say what changed, one line per item. If nothing new, touch nothing.
5. **Backlog.** Remove finished items (make sure they are in the daily log first) and add new requests to the right section. The backlog only holds open work.
   - **Route items to the project they belong to.** If the session produced an idea, bug or request for *another* project ("the CLI needs the same fix"), add it to **that** project's backlog, not this one, and mention it in the report. If it fits no project, list it in the report and ask.
6. **Resume note.** Read `RESUME.md` and rewrite it short (limit and sections from `PROJECT.md`; default at most ~60 lines with: Where we are · Tried, didn't work · Open questions · Next steps). Put "Last updated: YYYY-MM-DD" at the top. The first line under "Where we are" is what the `/resume` dashboard shows, so make it the single most useful sentence. Finished details do not stay in the note; if they are not in the daily log yet, move them there first.
   - **Tried, didn't work:** approaches that failed in this session and why, so the next session does not retry them. Drop entries once they no longer matter.

## 3. Light suggestion check (once per handoff, optional)

Skip this step if `PROJECT.md` says `Suggestions: off`.

1. Read `notes/SUGGESTIONS.md` (past answers) and skim the last ~10 daily logs, one line per entry.
2. Is there **one** strong pattern: repeated manual work (→ `suggest-skill`) or repeated heavy, noisy work (→ `suggest-agent`) that meets the rule of three and is not blocked by a past answer?
3. If yes, add **one line** at the end of the report, not a full proposal: "I noticed you wrote release notes by hand in 3 of the last 5 sessions. Want a skill for it? (yes / no / never / later)". On yes, run the full skill. Record any answer in `SUGGESTIONS.md` (an answer that arrives after the commit is committed at the next handoff).
4. If no, say nothing. At most one such question per handoff.

## 4. Commit and report

1. **Obsidian map.** If `PROJECT.md` says `Obsidian: on`, run the `obsidian-map` skill for the notes changed in this session (links, frontmatter, map note; canvas only if `Canvas: on`).
2. **Commit.** If `PROJECT.md` names a backup command, run it. Otherwise, if the project is a git repo, add the notes (git-ignored files such as local profiles stay out automatically) (and any finished work) and commit with a short message. Push only if `PROJECT.md` says the project pushes routinely.
3. **Report** in a few lines: which project, what was saved (including which topic files got new knowledge), anything failing or unfinished, and how to start next time: "In the new session, run `/resume`" (or `/resume <name>` when the folder holds several projects).

## Rules

- **Nothing gets lost.** Shortening the resume note means moving information to the daily log or decision file first, then removing it from the note.
- **Never delete files.** Edit, append, or move. Old versions live in git history.
- **Never claim work that did not happen.** Unfinished work and failing tests are written plainly.
- **Never rewrite git history.** No force push, no reset, no rebase. If a push fails, report it.
- **One project's notes never go into another project's files.**

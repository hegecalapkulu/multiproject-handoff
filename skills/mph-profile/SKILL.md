---
name: mph-profile
description: Keep short, evidence-based notes on how the user likes to work, per project first and in a general profile once a pattern shows up in two projects, so every session communicates the way the user prefers. Working style only, never personality. Local by default (git-ignored). Use when the user says "profile", "show my profile", "remove that from my profile", "in this project I want…", or when handoff finds a new, clearly observed working-style fact.
---

# Profile: how to work with this user

<!-- mph:lookup:start -->
> **Shared rules first.** Read `RULES.md` before anything else. Look for it in this order and stop at the first hit:
> 1. `RULES.md` next to this `SKILL.md`, in the same folder (if this file is `…/mph-resume/SKILL.md`, read `…/mph-resume/RULES.md`, not the parent `skills/` folder; many tools state this folder as the skill's base directory). Read it directly, without searching;
> 2. `~/.handoff/RULES.md`;
> 3. a search of the home folder, a few levels deep (skip `node_modules`, `.git`, `Library`, `AppData`), for a `RULES.md` whose first line contains `multiproject-handoff RULES`.
>
> If it was found by searching, use it and tell the user where, offering to copy it back to `~/.handoff/`. If it is nowhere, say so and suggest re-running `install.sh`. Never guess the rules.
<!-- mph:lookup:end -->

> **Optional module** (`profile`). Runs automatically only when `profile: on` in the `## Modules` section of `PROJECT.md` (RULES.md §3). Called by name, it works once even when off.

The agent knows the code and the project, but relearns **how to work with the user** every session. This skill keeps that knowledge in two short, readable files.

## The two layers

| File | Holds | Default location |
|---|---|---|
| **Project profile** | How the user works **in this project**: their knowledge of this domain, how much explanation they want, pace (fast prototype vs. careful), what they decide themselves and what they leave to the agent, project-specific sensitivities | `notes/working-style.md` (per person in team projects: `notes/working-style.<name>.md`) |
| **General profile** | What is the same **everywhere**: language and tone, answer format, approval habits ("ask before deleting"), things that get in the way of work in every project | `~/.handoff/working-style.md` |

### The four rules

1. **Project first.** A new observation goes to the **project** profile. One project is not enough to know a habit is general.
2. **Promotion at two projects.** When the same observation is in the project profiles of **two** projects, move it to the general profile and remove it from both project files. Say so: `🧭 [recipe-app] profile → general: "prefers tables over long text" (seen in recipe-app and cli-tool)`.
3. **The project wins.** If a project contradicts the general profile, write the exception in the project file under "Different from the general profile". Do not change the general profile for one project.
4. **People change.** Update an item instead of piling up new ones: "Early on wanted step-by-step explanations; since 2026-12 prefers to move fast." Remove items that are no longer true.

## What may be written

- **Only what was clearly observed or said** in a session: the user said it, corrected the agent, or the same reaction happened at least twice. No guesses, no generalizing from one moment.
- **Working style, not personality.** "Wants to see a list of affected files before a change" ✔. "Is impatient" ✘.
- **Never:** health, mood, private life, beliefs, anything about other people, or anything the user asked not to keep.
- **Every item has evidence and a date**, in a few words: `(said so, 2026-11-20)`, `(3 sessions)`, `(corrected me twice, 2026-11-22)`.
- **Short:** project profile at most ~15 lines, general profile at most ~40. When over, merge or drop the weakest items.
- **Readable by the user:** plain sentences in the user's language, no code. The user should be able to read it and say "yes, that's me" or "no, remove that".

## Format

```markdown
# Working style: <project>
Last updated: YYYY-MM-DD · General profile: ~/.handoff/working-style.md

## In this domain
- <knowledge level, how much explanation> (<evidence>, <date>)

## How we work here
- <pace, who decides what, sensitivities> (<evidence>, <date>)

## Different from the general profile
- <exception> (general profile says: "<item>")
```

The general profile uses the same shape with the headings **Communication**, **Format**, **Approvals and safety**, **Gets in the way**.

## Steps

### When reading (called by `mph-resume`)
1. Read the general profile and the active project's profile (≤ ~55 lines together).
2. Apply them quietly for the rest of the session. Do not recite them.

### When updating (called by `mph-handoff`, or when the user states a preference)
1. Use the **active project** (RULES.md §2).
2. Was there something **new and clearly observed** about how the user works? If not, touch nothing.
3. Decide the layer: domain knowledge, detail, pace and roles → project. Language, tone, format, approvals → still **project first** (rule 1), unless the same item already sits in another project's profile → promote (rule 2). To check, find the other projects as in RULES.md §1 and read only the item lines of the `working-style*.md` files in their notes folders.
4. Read the target file, then add, update or remove items. Keep the length limits.
5. **Always say what changed**, one line per item: `🧭 [recipe-app] profile added: "explain database steps, fast on frontend"`.

### When the user asks
- **"profile" / "show my profile"** → show both layers merged, each item marked `(general)` or `(this project)`.
- **"remove …" / "that's wrong"** → remove or correct it at once, confirm in one line.
- **"in this project I want …"** → write it to the project profile as `(said so, <date>)`.

## Local by default

- Profiles are **not committed** by default. The project profile is listed in the project's `.gitignore` (`mph-setup-project` adds `notes/working-style*.md`). The general profile lives outside every repo.
- If the user chose to share it (the `Profile:` line in `PROJECT.md` says `committed`), the project profile is committed like other notes.
- `.gitignore` only works for files that were never committed. If a profile was committed before, say so and let the user decide; do not rewrite history.

## Rules

- The user can read, edit or delete these files at any time; their edits win.
- Never use the profile to argue with the user ("your profile says you like short answers"). It is there to serve them, not to correct them.

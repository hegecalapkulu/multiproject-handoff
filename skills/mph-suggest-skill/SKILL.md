---
name: mph-suggest-skill
description: Find work the user keeps repeating by hand, in this session or across the project's history, and suggest at most 3 project-specific skills (or changes to existing ones) with evidence. Remembers every answer in notes/SUGGESTIONS.md, so a declined idea is not asked again unless the evidence clearly grows. Creates nothing without approval. Use when the user says "suggest-skill", "/mph-suggest-skill", "what could be automated here", or when handoff's light check finds a strong pattern.
---

# Suggest skills: learn the project, remember the answers

<!-- mph:lookup:start -->
> **Shared rules first.** Read `RULES.md` before anything else. Look for it in this order and stop at the first hit:
> 1. `RULES.md` next to this `SKILL.md`, in the same folder (if this file is `…/mph-resume/SKILL.md`, read `…/mph-resume/RULES.md`, not the parent `skills/` folder; many tools state this folder as the skill's base directory). Read it directly, without searching;
> 2. `~/.handoff/RULES.md`;
> 3. a search of the home folder, a few levels deep (skip `node_modules`, `.git`, `Library`, `AppData`), for a `RULES.md` whose first line contains `multiproject-handoff RULES`.
>
> If it was found by searching, use it and tell the user where, offering to copy it back to `~/.handoff/`. If it is nowhere, say so and suggest re-running `install.sh`. Never guess the rules.
<!-- mph:lookup:end -->

> **Optional module** (`suggestions`). Runs automatically only when `suggestions: on` in the `## Modules` section of `PROJECT.md` (RULES.md §3). Called by name, it works once even when off.

Goal: turn repeated manual work into skills, so the same quality costs fewer tokens and fewer forgotten steps, **without nagging**.

## 0. Project and memory

- Use the **active project** (RULES.md §2).
- Read `notes/SUGGESTIONS.md` if it exists. It is the memory of past suggestions:

```markdown
# Suggestions

| Date | Kind | Name | Answer | Evidence then | Ask again when |
|---|---|---|---|---|---|
| 2026-11-20 | skill | release-notes | accepted | 3 releases written by hand | - |
| 2026-11-22 | skill | deploy-check | declined: "I like doing it by hand" | 3 manual deploys | never (user said so) |
| 2026-11-23 | agent | log-reader | later | 2 large log reviews | after 3 more sessions |
```

## 1. Gather evidence

Pick the mode from how the skill was called:

- **Session mode** (default, or when called by `mph-handoff`): this conversation.
- **Project mode** ("review the project", "what could be automated here", or the user asks for a deeper look): the project's history. Read the **last ~10 daily logs** and the `## Project skills` list in `PROJECT.md`; skim the project's scripts and README for manual procedures (a "how to release" section is a skill waiting to happen). Do not read the whole codebase.

Look for:
- Steps done in the same order more than once (reads, commands, note updates).
- Rules or corrections the user gave more than once ("always do it like this").
- Steps that were forgotten and remembered later.
- Context explained again from scratch.
- The same kind of task showing up in several daily logs ("wrote release notes", "checked translations").

## 2. Filter

- **Already exists?** Check the tool's skills folders (for example `~/.claude/skills/`, `~/.codex/skills/`, `~/.agents/skills/`, the project's `.claude/skills/` or `.agents/skills/`) and `PROJECT.md`. If an existing skill is missing a step, suggest adding it there instead.
- **Not a skill:** something that happened once; facts that belong in the project instructions (`AGENTS.md`, `CLAUDE.md`) or a note; something that must run automatically on every message (that is a hook, only if truly needed).
- **Rule of three:** repeated by hand a third time → skill. Twice is enough only if it is multi-step and error-prone.
- **Respect the memory** (`SUGGESTIONS.md`):
  - `accepted` → never suggest again (maybe suggest an improvement to it).
  - `declined` with "never" → never suggest again.
  - `declined` without "never" → suggest again only if the evidence has **at least doubled** since then, and say so: "You declined this on 11-22 (3 times then, 7 now)."
  - `later` → only after its "ask again when" condition is met.

## 3. Suggest (at most 3)

For each:
- **Name** (lowercase, hyphens) and one-sentence description.
- **When:** which words or situation trigger it.
- **Evidence:** where it was needed (session moments or daily-log dates).
- **Saving:** tokens, time or mistakes it removes.
- **Steps:** a 3-6 bullet draft.
- **Scope:** project-specific (default) or general.

Then ask for an answer per suggestion: **yes / no / never / later**.

If there is nothing worth it, say so ("No repetition worth a skill yet.") and write nothing.

## 4. Record the answers, then act

1. Add one row per suggestion to `notes/SUGGESTIONS.md` (create it if missing): date, kind `skill`, name, the answer (with the user's reason in their words if given), the evidence count, and "ask again when":
   - yes → `-`
   - no → `if evidence doubles`
   - never → `never (user said so)`
   - later → `after 3 more sessions`, or what the user said
2. **For each yes**, create the skill:
   - Project-specific: in the project's skills folder for the tool in use (`.claude/skills/<name>/SKILL.md`, `.agents/skills/<name>/SKILL.md`, …).
   - General: in the personal skills folder of the tool.
   - Add one line to the `## Project skills` section of `PROJECT.md` (`- <name>: <one line>`), so every tool, `mph-menu` and future suggestions know it exists.
3. Report what was created and where, starting with `🧭 [<project>]`.

## Rules

- Create no skill without a yes.
- Never ask about the same idea twice in one session.
- `SUGGESTIONS.md` is append-and-update only; never delete rows (an answer can be updated, e.g. `later` → `accepted`).

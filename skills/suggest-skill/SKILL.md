---
name: suggest-skill
description: Review this conversation for work that was repeated by hand and suggest at most 3 new skills (or changes to existing ones), with evidence and expected savings. Creates nothing without the user's approval. Use when the user says "suggest-skill" or "/suggest-skill".
---

# Suggest skills

Goal: turn repeated manual work into skills, so the same quality costs fewer tokens and fewer forgotten steps.

## Steps

1. **Check what exists.** List the skills folders your tool uses (for example `~/.claude/skills/`, `~/.codex/skills/`, `~/.agents/skills/`, and the project's `.claude/skills/` or `.agents/skills/`). Never suggest something that already exists; if an existing skill is missing a step, suggest adding it there.
2. **Scan the conversation** for:
   - Steps done in the same order more than once (reads, commands, note updates).
   - Rules or corrections the user gave more than once ("always do it like this").
   - Steps that were forgotten and remembered later.
   - Context that had to be explained again from scratch.
3. **Filter.** These are *not* skills:
   - Something that happened once.
   - Facts the code or notes already record (those belong in the project instructions file, such as `AGENTS.md` or `CLAUDE.md`, or in a note).
   - Things that must run automatically on every message (that is a hook, and only if truly needed).
   - **Rule of three:** work repeated by hand a third time becomes a skill. Twice is enough only if it is multi-step and error-prone.
4. **Suggest at most 3.** For each:
   - **Name** (lowercase, hyphens) and one-sentence description.
   - **When:** which words or situation trigger it.
   - **Evidence:** where in this conversation it was needed (short).
   - **Saving:** tokens, time or mistakes it removes.
   - **Steps:** a 3-6 bullet draft.
5. If there is nothing worth it, say so: "I saw no repetition worth a skill in this session." Do not invent suggestions.
6. **Only after the user approves**, create the skill: in the project skills folder of the tool in use (for example `.claude/skills/<name>/SKILL.md` or `.agents/skills/<name>/SKILL.md`) if it is project-specific (default when unsure), or in the personal skills folder if it is general.

## Rules

- Create no files without approval.

---
name: decision-log
description: Record a new decision, or a changed one, in the current project's decision file, with the reason. Use when the user decides something ("let's go with X", "we won't do Y") or reverses an earlier decision.
---

# Decision log

Decisions are the most expensive thing to lose between sessions. A new session that does not know *why* something was decided will happily undo it.

## 0. Find the project
- The project is the folder this session is working in. If unclear, ask.
- Read `notes/PROJECT.md` first if it exists: it may contain a map of "which kind of decision goes to which file".
- Default: `notes/DECISIONS.md`. If it does not exist, ask before creating it.

## Steps

1. Identify the topic and find the right file using the map. If nothing fits, follow the map's "new file" rule, or add a new heading in `DECISIONS.md`.
2. Read the file. If the new decision contradicts an older one, **replace** the old one, write today's date, and add a short "(previously: X)" note. Do not leave struck-through lines; history lives in git.
3. Write **why** next to every decision, in one sentence.
4. If the decision closes an open question (in `RESUME.md` or wherever `PROJECT.md` says), mark it there.
5. If the decision changes planned work, update the backlog.

## Format

```markdown
## <Topic>
- **<Decision>** (YYYY-MM-DD). Why: <one sentence>. (previously: <old decision>)
```

## Rules

- Separate decisions from hypotheses. Anything not yet tested is written as "hypothesis".
- **The user decides.** A suggestion from Claude is not a decision until the user agrees.

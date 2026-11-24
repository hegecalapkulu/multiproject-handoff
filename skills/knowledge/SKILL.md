---
name: knowledge
description: File lasting project knowledge (research, competitors, strategy, interviews, specs, anything worth keeping) into the project's notes so it grows into an organized structure over time. Picks the right file from the project's knowledge map, starts new topics and proposes splitting big topics into folders, always with the user's OK. Use when the user says "save this", "keep this research", "add to notes", "knowledge", "organize notes", or when handoff finds lasting knowledge in the session.
---

# Knowledge: notes that grow with the project

A project produces three kinds of information. Only the third one is handled here:

| Kind | Example | Goes to |
|---|---|---|
| **State** | "search works, remove-item is half done" | `RESUME.md` (rewritten every handoff) |
| **Decision** | "SQLite instead of Algolia, because…" | decisions (`decision-log` skill) |
| **Knowledge** | competitor pricing, interview notes, research results, a strategy, an API's quirks | **topic files**, organized by the knowledge map |

Knowledge is anything a future session would want to look up again and that is not just "where we are" or "what we chose".

## 0. Find the project and its map

- Find the project as in `handoff` step 0.
- Read the `## Knowledge map` section of `notes/PROJECT.md`. Each line maps a topic to a file or folder:
  ```markdown
  ## Knowledge map
  - Competitors → notes/knowledge/competitors/
  - Pricing research → notes/knowledge/pricing.md
  ```
- **The map is the user's structure.** Names, languages, numbering and locations are whatever the user chose (`03 Sales/`, `docs/research/`, an Obsidian folder…). Follow it exactly; never rename or move the user's folders to fit a default.
- No map yet → the default root is `notes/knowledge/`, and the map starts empty.
- Read `## Structure rules` in `PROJECT.md` too, if present (folder naming, language, split size, file naming). They override the defaults in this skill.

## 1. File a piece of knowledge

1. **Decide what it is.** One topic, a short title, the date and the source (the session, a URL, a person). If it is really state or a decision, hand it to the right place instead.
2. **Find its topic in the map.** Match by meaning, not exact words ("rivals", "competition" → Competitors).
3. **Topic exists:**
   - File → read it, then add the new knowledge under a dated heading, or update the existing entry if it is about the same thing (a competitor's price changed → replace the price, keep "(previously: …)").
   - Folder → read its `_overview.md`, then write into the matching sub-file, or create a new sub-file for a new subject (a new competitor gets its own file) and add one line for it in `_overview.md`.
4. **Topic is new** → propose it in one line, then create it after a yes:
   "New topic **Competitors** → `notes/knowledge/competitors.md`. OK?"
   Start as a **single file**. Folders come later, when the topic earns them (step 2).
   Add the topic to the knowledge map in `PROJECT.md`.
5. **Write knowledge, not chat.** Facts, numbers, links, quotes, conclusions. Mark anything unverified as "unverified". Keep the source.

### Entry format

```markdown
## Paprika (checked 2026-12-03)
- Price: $4.99 one-time on mobile, $29.99 desktop. Source: paprikaapp.com
- Strong: offline, recipe import from any site.
- Weak: no shared shopping list between household members (3 reviews mention it).
- Takeaway for us: shared list is a real gap. (unverified: how many users care)
```

## 2. Let the structure grow (propose, never force)

Check these whenever you write to a topic. When one applies, **propose** the change in one or two sentences and wait for a yes:

| Signal | Proposal |
|---|---|
| A topic file is over ~150 lines, **or** it holds 4+ clearly separate subjects (4 competitors, 5 interviews) | Split it into a folder: one file per subject plus `_overview.md` with a one-line summary and link per subject. |
| The same kind of knowledge has shown up in 2+ sessions but has no topic | Start a topic for it. |
| Two topics keep overlapping | Merge them, or define the boundary in the map. |
| A topic has not changed in a long time and nothing links to it | Mention it; the user may want to archive it (move to `notes/knowledge/_archive/`). |
| `DECISIONS.md` has grown several clear areas (product, tech, pricing…) | Split it into `notes/decisions/<area>.md` and add a decisions map. |

When the user agrees to a restructure:

1. **Move, never delete.** Use `git mv` when the project is a git repo, so history follows the file.
2. Split content without losing a line: every entry of the old file ends up in exactly one new file.
3. Write the `_overview.md` (one line per sub-file: name, one-sentence summary, link).
4. Fix links that pointed to the old file (search the notes for its name).
5. Update the knowledge map in `PROJECT.md`.
6. Say what moved where, in a short list.

**"organize notes"**: when the user asks, review the whole structure against the table above and propose all changes at once, as a short list they can accept item by item.

## Rules

- **The user owns the structure.** New topics, folders, splits, merges and archives happen only after a yes. Filing into an existing topic needs no question.
- **Never delete.** Move, merge or archive. History lives in git.
- **No secrets and no personal data** that should not be in a repo (passwords, keys, private phone numbers, real customer data unless the user's project rules allow it).
- **Reading is cheap only if it stays rare:** `resume` reads the map, not the topic files. Open a topic file only when the current work needs it.

---
name: mph-obsidian-map
description: Make a project's notes work as a connected map in Obsidian. Adds links between related notes (decisions, knowledge, daily logs, resume note), keeps a map note per project and one for all projects, adds frontmatter tags for graph coloring, and can draw an Obsidian Canvas of the project. Use when the user says "obsidian-map", "link my notes", "update the map", "draw the project map", or at handoff when PROJECT.md says Obsidian is on.
---

# Obsidian map: turn the notes into a connected graph

<!-- mph:lookup:start -->
> **Shared rules first.** Read `RULES.md` before anything else. Look for it in this order and stop at the first hit:
> 1. `RULES.md` next to this `SKILL.md`, in the same folder (if this file is `…/mph-resume/SKILL.md`, read `…/mph-resume/RULES.md`, not the parent `skills/` folder; many tools state this folder as the skill's base directory). Read it directly, without searching;
> 2. `~/.handoff/RULES.md`;
> 3. a search of the home folder, a few levels deep (skip `node_modules`, `.git`, `Library`, `AppData`), for a `RULES.md` whose first line contains `multiproject-handoff RULES`.
>
> If it was found by searching, use it and tell the user where, offering to copy it back to `~/.handoff/`. If it is nowhere, say so and suggest re-running `install.sh`. Never guess the rules.
<!-- mph:lookup:end -->

> **Optional module** (`obsidian`). Runs automatically only when `obsidian: on` in the `## Modules` section of `PROJECT.md` (RULES.md §3). Called by name, it works once even when off.

Obsidian shows notes as a graph: every link between two notes is a line. Notes written by the other skills are already organized, but mostly **not linked**, so in the graph they float as separate dots. This skill adds the connections, so the user can see and walk the project: from a decision to the research behind it, from a competitor to the decision it caused, from a daily log to what it changed.

## 0. Setup checks

- Use the **active project** (RULES.md §2).
- **Find the vault root:** the nearest folder above the notes that contains `.obsidian/`. If there is none, the notes are not in a vault: say so, and offer to continue anyway (links still work in any Markdown viewer and on GitHub).
- Read the `## Obsidian` section of `PROJECT.md` (the on/off switch is `obsidian:` under `## Modules`):
  ```markdown
  ## Obsidian
  - Links: markdown         <!-- markdown (works on GitHub too) | wikilinks ([[Note]], Obsidian only) -->
  - Canvas: off             <!-- on: keep notes/map.canvas up to date at handoff -->
  ```
  Missing section → treat as `Links: markdown`, `Canvas: off`.

## 1. Links between notes

Add links only where a real relation exists. Never link just to make the graph look busy.

| From | To | When |
|---|---|---|
| A decision | the knowledge note it was based on | the decision's "why" uses that research |
| A knowledge note | the decision it led to | a decision cites it |
| A daily log | decisions made and knowledge filed that day | they were written in that session |
| A daily log | the previous daily log | always (`Previous log:` line) |
| `RESUME.md` | the decisions/knowledge behind open questions and next steps | the next step depends on them |
| A topic `_overview.md` | each of its sub-notes | always |

How to write links:
- **Markdown style** (default): `[pricing research](../knowledge/pricing.md)`: relative path from the current file. Obsidian's graph counts these too.
- **Wikilinks** (if chosen): `[[pricing]]`, or `[[knowledge/pricing|pricing research]]` when the name is not unique in the vault.
- Add links **inline**, where the relation is mentioned ("based on [pricing research](…)"), or as a short `Related:` line at the end of an entry. Never rewrite the user's text to fit a link.

## 2. Frontmatter for graph groups

Add (or complete) a small frontmatter block at the top of each note the skills manage:

```yaml
---
project: recipe-app
type: decision        # resume · backlog · decision · knowledge · daily · profile · map
tags: [project/recipe-app, type/decision]
---
```

With these tags the user can color the graph by project or by note type (Graph view → Groups → `tag:#type/decision`). Tell them that once; do not edit `.obsidian/` settings yourself.

If a note already has frontmatter, only add missing keys; never change the user's own keys.

## 3. Map notes

- **Project map** `notes/_map.md`: the project's entry point. One short line and a link per item:
  ```markdown
  ---
  project: recipe-app
  type: map
  tags: [project/recipe-app, type/map]
  ---
  # recipe-app: map
  - Now: [resume note](RESUME.md) · [backlog](BACKLOG.md)
  - Decisions: [product](decisions/product.md) · [tech](decisions/tech.md)
  - Knowledge: [competitors](knowledge/competitors/_overview.md) · [interviews](knowledge/interviews/) · [pricing](knowledge/pricing.md)
  - Project skills: seed-test-data · Agents: none yet
  - Logs: latest [2026-11-23](daily/2026-11-23.md)
  ```
  Built from the knowledge and decisions maps in `PROJECT.md`, so it never invents structure.
- **Workspace map** `PROJECTS-MAP.md` in the folder that holds the projects (or next to `PROJECTS.md`): one line per project with its first "Where we are" line and a link to its `_map.md`. This becomes the center of the graph, with each project as a cluster around it.

## 4. Canvas (optional)

When the user asks ("draw the project map"), or when `Canvas: on`: write `notes/map.canvas` in the [JSON Canvas](https://jsoncanvas.org) format that Obsidian opens natively:

- One **file node** per main note (`RESUME.md`, each decision file, each knowledge topic), with `file` = its path relative to the vault root.
- **Group nodes** for "Now", "Decisions", "Knowledge", laid out left to right.
- **Edges** for the links from step 1 between decisions and knowledge.
- Keep it readable: at most ~25 nodes; topics with sub-notes show only their `_overview.md`.
- Regenerate the file as a whole each time, and say that hand-made changes to `map.canvas` will be replaced (or use another file name for hand-made canvases).

## When it runs

- **Manually:** "link my notes", "update the map", "draw the project map", "obsidian-map".
- **At handoff**, if `obsidian: on` under `## Modules`: only for the notes written or changed in this session (new links, frontmatter, the map note's changed lines). Not a full rebuild every time, so it stays fast.
- **Full rebuild:** "rebuild the map" re-checks every note of the project.

It does not run in the background. A skill runs when it is called; running it at each handoff keeps the map current without a background process.

## Rules

- **Never delete or move notes** here; this skill only adds links, frontmatter and map files. Restructuring belongs to the `mph-knowledge` skill.
- **Never break existing links.** Before adding a link, check that the target file exists.
- **Do not touch `.obsidian/`** (the user's Obsidian settings).
- Report in one line: `🧭 [recipe-app] map: 7 links added, _map.md updated`.

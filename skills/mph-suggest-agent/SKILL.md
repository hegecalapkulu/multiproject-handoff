---
name: mph-suggest-agent
description: Suggest an optional, project-specific helper agent (subagent) for heavy or noisy work, such as reading big logs, checking a site in a browser, auditing data or reviewing many files, so the main session gets back only the findings. At most 2 suggestions with evidence; answers are remembered in notes/SUGGESTIONS.md. Creates nothing without approval. Use when the user says "suggest-agent", "/mph-suggest-agent", "should this be a subagent", or when handoff's light check finds a strong pattern.
---

# Suggest agents: move the noisy work out of the main session

<!-- mph:lookup:start -->
> **Shared rules first.** Read `RULES.md` before anything else. Look for it in this order and stop at the first hit:
> 1. `RULES.md` in this skill's own folder;
> 2. `~/.handoff/RULES.md`;
> 3. a search of the home folder, a few levels deep (skip `node_modules`, `.git`, `Library`, `AppData`), for a `RULES.md` whose first line contains `multiproject-handoff RULES`.
>
> If it was found by searching, use it and tell the user where, offering to copy it back to `~/.handoff/`. If it is nowhere, say so and suggest re-running `install.sh`. Never guess the rules.
<!-- mph:lookup:end -->

> **Optional module** (`suggestions`). Runs automatically only when `suggestions: on` in the `## Modules` section of `PROJECT.md` (RULES.md §3). Called by name, it works once even when off.

A helper agent is worth it when a job **produces a lot of output but only a little of it matters**: screenshots, long logs, big data files, many files to scan. The helper does the heavy reading in its own context and returns a short list of findings. The main session stays small and cheap.

It is **not** worth it for work that needs the main conversation's context, or for writing the main code. That stays in the main session.

## 0. Project and memory

- Use the **active project** (RULES.md §2).
- Read `notes/SUGGESTIONS.md` and apply the same memory rules as `mph-suggest-skill` (accepted → never again; never → never; no → only if the evidence doubles; later → when its condition is met). Rows for agents have kind `agent`.

## 1. Look for these patterns

In this session (or, in project mode, the last ~10 daily logs):

- Large outputs read in the main session just to find a few problems (test logs, build logs, crawls, data dumps).
- Browser checks where many screenshots were taken to verify one flow.
- The same audit done repeatedly (data consistency, broken links, translations, accessibility).
- Searches across many files where only the conclusion mattered.

Rule of three applies: the pattern should have happened about three times, or twice if each time was very expensive.

## 2. Suggest (at most 2)

For each:
- **Name** and one sentence: what it checks and what it returns.
- **Evidence:** when it was needed and roughly how much output it would have kept out of the main session.
- **Input / output:** what the main session gives it, and the exact shape of the answer (for example "a table: problem · file · line · severity", "max 15 lines").
- **Tools it needs**, as few as possible (read-only when it can be).
- **Never does:** for example "never edits files", "never deploys".

Ask: **yes / no / never / later**, then record each answer in `notes/SUGGESTIONS.md` (kind `agent`).

## 3. Create it (only after yes)

Write it where the tool in use reads helper agents:

- **Claude Code:** `.claude/agents/<name>.md` in the project, with frontmatter `name`, `description` (when to use it), and `tools` (the minimum). The body: the job, the input it expects, the exact output format, and the "never" list.
- **Other tools with subagent support:** use that tool's agent folder and format (check its docs; formats differ between tools and versions).
- **Tools without subagents:** create it as a project skill instead, instructing the main agent to do the job as one separate step and report only the findings in the agreed format. Say plainly that this saves less context than a real subagent.

Then:
1. Add one line under `## Project agents` in `PROJECT.md` (`- <name>: <one line> (file: <path>)`), so `mph-menu` and every tool know it exists.
2. Report what was created and where, starting with `🧭 [<project>]`.

## Rules

- Create nothing without a yes. Never ask about the same idea twice in one session.
- Helpers return findings; the main session decides and writes the code.
- Prefer read-only helpers. A helper that changes files needs the user's explicit OK for that.

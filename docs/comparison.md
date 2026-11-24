# Comparison and FAQ

[← back to README](../README.md)

## How is this different from other handoff / memory-bank tools?

There are good tools in this space, and some ideas here come from them. Most do one of two things: **one handoff file for one project**, or a **memory bank** of context files for a single project, often tied to one tool. `multiproject-handoff` differs in five ways:

1. **Notes that grow into a structure:** knowledge is filed into topics that split into folders as they grow, on a map every session can read, in the names and layout you choose.
2. **Many projects, one command:** the dashboard, `mph-resume <project>`, stale warnings, a handoff that knows which project it is closing, and backlog items routed to the right project.
3. **Each kind of information has its own lifecycle,** so the file the next session reads stays under 60 lines after months of work.
4. **Per-project settings instead of per-project skills:** one `PROJECT.md` changes paths, checks and rules; the skills stay the same everywhere.
5. **Not tied to one AI tool:** start a project in Claude Code, continue it in Codex or Gemini tomorrow. The notes are the same.

## FAQ

**My tool already has memory.**
Use it for preferences. This is for project *state*, which changes every day and belongs in the repo, next to the code, where it's versioned and shared with every tool and teammate.

**Why Markdown files and not a database or an MCP server?**
You can read them, diff them, edit them by hand and open them in Obsidian. If you stop using this tomorrow, your notes still make sense.

**Can I change the folder layout?**
Yes: write the paths in `notes/PROJECT.md` and every skill follows them.

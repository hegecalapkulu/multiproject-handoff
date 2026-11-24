# Obsidian map

[← back to README](../README.md)

Keep your projects in an Obsidian vault and set `obsidian: on` under `## Modules` in `PROJECT.md`. At each handoff, `mph-obsidian-map`:

- **links related notes**: a decision to the research behind it, a competitor to the decision it caused, a daily log to what it changed, so the graph shows real relations instead of loose dots;
- **adds frontmatter tags** (`project/…`, `type/decision`, `type/knowledge`…) so you can color the graph by project or by note type;
- **keeps a map note per project** (`notes/_map.md`) and **one for all projects** (`PROJECTS-MAP.md`), the center of the graph;
- **draws a Canvas** (`notes/map.canvas`) of the project on request, or at every handoff with `Canvas: on`.

Links are standard Markdown by default, so they also work on GitHub; switch to `[[wikilinks]]` if you prefer. It never moves notes and never touches your `.obsidian/` settings.

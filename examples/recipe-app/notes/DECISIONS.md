# Decisions

## Product
- **v1 has no social features** (2026-11-18). Why: the goal is a tool for one household, not a network.

## Tech
- **SQLite with full-text search instead of a search service** (2026-11-20). Why: one file, no extra server, fast enough for <100k recipes. (previously: Algolia)

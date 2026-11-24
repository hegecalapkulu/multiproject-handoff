#!/bin/sh
# claude-handoff installer.
# Copies the skills into Claude Code's skills folder. Never deletes anything.
#
#   ./install.sh                 install for every project   (~/.claude/skills)
#   ./install.sh --project DIR   install for one project only (DIR/.claude/skills)
#   ./install.sh --update        overwrite skills installed earlier by this script
set -e

SRC="$(cd "$(dirname "$0")" && pwd)/skills"
DEST="$HOME/.claude/skills"
UPDATE=0

while [ $# -gt 0 ]; do
  case "$1" in
    --project) [ -n "$2" ] || { echo "usage: --project DIR"; exit 1; }
               DEST="$(cd "$2" && pwd)/.claude/skills"; shift 2 ;;
    --update)  UPDATE=1; shift ;;
    -h|--help) sed -n '2,8p' "$0"; exit 0 ;;
    *) echo "unknown option: $1"; exit 1 ;;
  esac
done

mkdir -p "$DEST"
installed=0; skipped=0
for d in "$SRC"/*/; do
  name="$(basename "$d")"
  target="$DEST/$name"
  if [ -e "$target" ] && [ ! -f "$target/.claude-handoff" ]; then
    echo "skip   $name  (a different skill with this name already exists at $target)"
    skipped=$((skipped+1)); continue
  fi
  if [ -e "$target" ] && [ "$UPDATE" -eq 0 ]; then
    echo "skip   $name  (already installed; run with --update to refresh)"
    skipped=$((skipped+1)); continue
  fi
  mkdir -p "$target"
  cp -R "$d". "$target/"
  echo "installed by claude-handoff" > "$target/.claude-handoff"
  echo "ok     $name  -> $target"
  installed=$((installed+1))
done

echo
echo "$installed installed, $skipped skipped."
echo "Next: open a project in Claude Code and type /setup-project"

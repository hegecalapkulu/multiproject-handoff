#!/bin/sh
# multiproject-handoff installer. Never deletes anything.
#
#   ./install.sh                     install for every AI tool found on this machine
#   ./install.sh --tool NAME         install for one tool: claude | codex | agents | gemini | antigravity
#   ./install.sh --dir PATH          install into any skills folder you name
#   ./install.sh --project DIR       install inside one project instead of your home folder
#   ./install.sh --agents-md DIR     for tools without skill support: copy the skills to
#                                    ~/.handoff/skills and add a short block to DIR/AGENTS.md
#   ./install.sh --update            refresh skills this script installed before
#   ./install.sh --dry-run           show what would happen, change nothing
set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"
SRC="$ROOT/skills"
MARK=".multiproject-handoff"
TOOL=""; DIR=""; PROJECT=""; AGENTS_DIR=""; UPDATE=0; DRY=0

usage() { sed -n '2,13p' "$0" | sed 's/^# \{0,1\}//'; }

while [ $# -gt 0 ]; do
  case "$1" in
    --tool)      TOOL="$2"; shift 2 ;;
    --dir)       DIR="$2"; shift 2 ;;
    --project)   PROJECT="$(cd "$2" && pwd)"; shift 2 ;;
    --agents-md) AGENTS_DIR="$(cd "$2" && pwd)"; shift 2 ;;
    --update)    UPDATE=1; shift ;;
    --dry-run)   DRY=1; shift ;;
    -h|--help)   usage; exit 0 ;;
    *) echo "unknown option: $1"; usage; exit 1 ;;
  esac
done

# Where each tool reads skills from. Paths change between tool versions:
# if a tool does not see the skills, check its docs and use --dir.
home_dir() {
  case "$1" in
    claude)      echo "$HOME/.claude/skills" ;;
    codex)       echo "$HOME/.codex/skills" ;;
    agents)      echo "$HOME/.agents/skills" ;;
    gemini)      echo "$HOME/.gemini/skills" ;;
    antigravity) echo "$HOME/.gemini/antigravity/skills" ;;
    *) echo "unknown tool: $1 (use claude, codex, agents, gemini, antigravity, or --dir)" >&2; exit 1 ;;
  esac
}
project_dir() {
  case "$1" in
    claude) echo "$PROJECT/.claude/skills" ;;
    gemini) echo "$PROJECT/.gemini/skills" ;;
    *)      echo "$PROJECT/.agents/skills" ;;   # the cross-tool project folder
  esac
}

installed=0; skipped=0
install_to() { # $1 = skills folder
  dest="$1"
  echo "→ $dest"
  [ "$DRY" -eq 1 ] || mkdir -p "$dest"
  for d in "$SRC"/*/; do
    name="$(basename "$d")"; target="$dest/$name"
    if [ -e "$target" ] && [ ! -f "$target/$MARK" ]; then
      echo "  skip   $name  (a different skill with this name is already there)"
      skipped=$((skipped+1)); continue
    fi
    if [ -e "$target" ] && [ "$UPDATE" -eq 0 ]; then
      echo "  skip   $name  (already installed; use --update to refresh)"
      skipped=$((skipped+1)); continue
    fi
    if [ "$DRY" -eq 0 ]; then
      mkdir -p "$target"; cp -R "$d". "$target/"
      echo "installed by multiproject-handoff" > "$target/$MARK"
    fi
    echo "  ok     $name"
    installed=$((installed+1))
  done
}

add_agents_block() { # $1 = folder that gets AGENTS.md
  file="$1/AGENTS.md"
  if [ -f "$file" ] && grep -q "multiproject-handoff:start" "$file"; then
    echo "→ $file already has the multiproject-handoff block (unchanged)"; return
  fi
  echo "→ adding the multiproject-handoff block to $file"
  [ "$DRY" -eq 1 ] && return
  {
    [ -f "$file" ] && echo
    echo "<!-- multiproject-handoff:start -->"
    echo "## Session handoff (multiproject-handoff)"
    echo
    echo "This workspace keeps per-project notes in \`<project>/notes/\`. When the user says one of the"
    echo "words below, read the matching file and follow it step by step:"
    echo
    echo "- \"resume\" / \"where were we\" → \`$HOME/.handoff/skills/mph-resume/SKILL.md\`"
    echo "- \"handoff\" / \"wrap up\" → \`$HOME/.handoff/skills/mph-handoff/SKILL.md\`"
    echo "- \"daily log\" → \`$HOME/.handoff/skills/mph-daily-log/SKILL.md\`"
    echo "- a decision is made → \`$HOME/.handoff/skills/mph-decision-log/SKILL.md\`"
    echo "- \"setup project\" → \`$HOME/.handoff/skills/mph-setup-project/SKILL.md\`"
    echo "- \"suggest skill\" → \`$HOME/.handoff/skills/mph-suggest-skill/SKILL.md\`"
    echo "- \"menu\" → \`$HOME/.handoff/skills/mph-menu/SKILL.md\` (lists all the others)"
    echo
    echo "Before any of them, read \`$HOME/.handoff/RULES.md\`. Never delete files or rewrite git history."
    echo "Model advice: if you know which model you are and it is a large one, before a clearly simple task offer once to switch to a lighter model (the user decides; never switch silently)."
    echo "<!-- multiproject-handoff:end -->"
  } >> "$file"
}

place_rules() { # shared rules at the known address ~/.handoff/RULES.md
  rules="$HOME/.handoff/RULES.md"
  if [ -f "$rules" ] && ! head -1 "$rules" | grep -q "multiproject-handoff RULES"; then
    echo "→ $rules exists and is not ours: left unchanged"; return
  fi
  echo "→ shared rules: $rules"
  [ "$DRY" -eq 1 ] && return
  mkdir -p "$HOME/.handoff"; cp "$ROOT/shared/RULES.md" "$rules"
  # the optional guard script (not registered here; the mph-guard skill does that after asking)
  cp "$ROOT/guard/mph-guard.py" "$HOME/.handoff/mph-guard.py"
  cp "$ROOT/shared/mph-scan.py" "$HOME/.handoff/mph-scan.py"
  cp "$ROOT/guard/mph-context.py" "$HOME/.handoff/mph-context.py"
  echo "→ guard script: $HOME/.handoff/mph-guard.py (inactive until you run mph-guard)"
}

if [ -n "$AGENTS_DIR" ]; then
  install_to "$HOME/.handoff/skills"
  add_agents_block "$AGENTS_DIR"
elif [ -n "$DIR" ]; then
  install_to "$DIR"
elif [ -n "$PROJECT" ]; then
  install_to "$(project_dir "${TOOL:-agents}")"
elif [ -n "$TOOL" ]; then
  install_to "$(home_dir "$TOOL")"
else
  found=0
  [ -d "$HOME/.claude" ]             && { install_to "$(home_dir claude)"; found=1; }
  [ -d "$HOME/.codex" ]              && { install_to "$(home_dir codex)"; found=1; }
  [ -d "$HOME/.agents" ]             && { install_to "$(home_dir agents)"; found=1; }
  [ -d "$HOME/.gemini/antigravity" ] && { install_to "$(home_dir antigravity)"; found=1; }
  [ -d "$HOME/.gemini" ] && [ -f "$HOME/.gemini/settings.json" ] && { install_to "$(home_dir gemini)"; found=1; }
  if [ "$found" -eq 0 ]; then
    echo "No known AI tool folder found. Use --tool, --dir or --agents-md (see --help)."; exit 1
  fi
fi

place_rules
echo
[ "$DRY" -eq 1 ] && echo "(dry run: nothing was changed)"
echo "$installed installed, $skipped skipped."
echo "Next: open a project with your AI tool and run /mph-setup-project (or just say \"set up this project\")."

#!/bin/sh
# Sanity checks: skill names, shared rules in sync, relative links, installer.
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$ROOT"; fail=0
for f in skills/*/SKILL.md; do
  dir=$(basename "$(dirname "$f")"); name=$(sed -n 's/^name: //p' "$f" | head -1)
  [ "$name" = "$dir" ] || { echo "name mismatch: $f ($name)"; fail=1; }
  echo "$name" | grep -Eq '^[a-z0-9-]{1,64}$' || { echo "invalid name: $name"; fail=1; }
  grep -q '^description: ' "$f" || { echo "no description: $f"; fail=1; }
  cmp -s shared/RULES.md "$(dirname "$f")/RULES.md" || { echo "RULES.md out of sync: $dir (run scripts/sync.sh)"; fail=1; }
  grep -q 'mph:lookup:start' "$f" || { echo "lookup block missing: $f"; fail=1; }
done
python3 - <<'PY' || fail=1
import re, os, glob, sys
bad = 0
for f in glob.glob("**/*.md", recursive=True):
    if f.startswith(("skills/", "shared/")): continue
    for m in re.finditer(r"\]\(([^)#\s]+)\)", open(f).read()):
        t = m.group(1)
        if t.startswith(("http", "mailto:")): continue
        if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(f), t))):
            print("broken link:", f, "->", t); bad += 1
sys.exit(1 if bad else 0)
PY
sh -n install.sh || fail=1
T=$(mktemp -d); mkdir -p "$T/.claude"
HOME="$T" ./install.sh >/dev/null || fail=1
n=$(ls "$T/.claude/skills" | wc -l | tr -d ' '); [ "$n" -eq "$(ls skills | wc -l | tr -d ' ')" ] || { echo "installer installed $n skills"; fail=1; }
[ -f "$T/.handoff/RULES.md" ] || { echo "installer did not place ~/.handoff/RULES.md"; fail=1; }
[ "$fail" -eq 0 ] && echo "all checks passed" || { echo "checks failed"; exit 1; }

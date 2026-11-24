#!/bin/sh
# Copies shared/RULES.md into every skill folder and writes shared/LOOKUP.md
# into each SKILL.md (between the mph:lookup markers). Run after editing shared/.
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
for d in "$ROOT"/skills/*/; do
  cp "$ROOT/shared/RULES.md" "$d/RULES.md"
  python3 - "$d/SKILL.md" "$ROOT/shared/LOOKUP.md" <<'PY'
import re, sys
skill, lookup = sys.argv[1], open(sys.argv[2]).read().strip()
s = open(skill).read()
block = "<!-- mph:lookup:start -->\n" + lookup + "\n<!-- mph:lookup:end -->"
if "<!-- LOOKUP -->" in s:
    s = s.replace("<!-- LOOKUP -->", block, 1)
else:
    s = re.sub(r"<!-- mph:lookup:start -->.*?<!-- mph:lookup:end -->", lambda m: block, s, flags=re.S)
open(skill, "w").write(s)
PY
done
echo "synced $(ls -d "$ROOT"/skills/*/ | wc -l | tr -d ' ') skills"

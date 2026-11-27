#!/bin/sh
# Sanity checks: skill names, shared rules in sync, relative links, installer, plugin manifests.
set -e
ROOT="$(cd "$(dirname "$0")/.." && pwd)"; cd "$ROOT"; fail=0
for f in skills/*/SKILL.md; do
  dir=$(basename "$(dirname "$f")"); name=$(sed -n 's/^name: //p' "$f" | head -1)
  [ "$name" = "$dir" ] || { echo "name mismatch: $f ($name)"; fail=1; }
  echo "$name" | grep -Eq '^[a-z0-9-]{1,64}$' || { echo "invalid name: $name"; fail=1; }
  grep -q '^description: ' "$f" || { echo "no description: $f"; fail=1; }
  cmp -s shared/RULES.md "$(dirname "$f")/RULES.md" || { echo "RULES.md out of sync: $dir (run scripts/sync.sh)"; fail=1; }
  cmp -s shared/mph-scan.py "$(dirname "$f")/mph-scan.py" || { echo "mph-scan.py out of sync: $dir (run scripts/sync.sh)"; fail=1; }
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
[ -f "$T/.handoff/mph-context.py" ] || { echo "installer did not place the context hint"; fail=1; }
[ -f "$T/.handoff/mph-guard.py" ] || { echo "installer did not place the guard script"; fail=1; }
(cd examples/workspace && python3 ../../shared/mph-scan.py | grep -q "^PROJECTS 4") || { echo "scanner did not find the 4 example projects"; fail=1; }
python3 scripts/test-guard.py >/dev/null || { echo "guard tests failed (run scripts/test-guard.py)"; fail=1; }
for p in examples/workspace/*/; do
  find "$p" -maxdepth 3 -name PROJECT.md -exec head -1 {} \; | grep -q '^<!-- mph:project ' || { echo "example without marked PROJECT.md: $p"; fail=1; }
done
head -1 skills/mph-setup-project/templates/PROJECT.md | grep -q '^<!-- mph:project ' || { echo "template PROJECT.md has no marker"; fail=1; }
python3 - <<'PY2' || fail=1
import json, re, sys
p = json.load(open(".claude-plugin/plugin.json")); m = json.load(open(".claude-plugin/marketplace.json"))
e = [x for x in m["plugins"] if x["name"] == p["name"]]
badge = re.search(r"badge/version-([0-9.]+)-", open("README.md").read())
bad = []
if not e: bad.append("marketplace.json does not list the plugin")
elif e[0].get("version") != p["version"]: bad.append("plugin.json and marketplace.json versions differ")
if not badge or badge.group(1) != p["version"]: bad.append("README version badge differs from plugin.json")
for b in bad: print(b)
sys.exit(1 if bad else 0)
PY2
# uninstall: moves only what we installed, keeps foreign skills and hooks
U=$(mktemp -d); mkdir -p "$U/.claude/skills/other-skill"
HOME="$U" ./install.sh >/dev/null || fail=1
printf '{"hooks":{"PreToolUse":[{"hooks":[{"type":"command","command":"python3 ~/.handoff/mph-guard.py"},{"type":"command","command":"other.sh"}]}]}}' > "$U/.claude/settings.json"
HOME="$U" ./install.sh --uninstall --dry-run >/dev/null || fail=1
[ -d "$U/.claude/skills/mph-resume" ] || { echo "uninstall --dry-run changed something"; fail=1; }
HOME="$U" ./install.sh --uninstall --yes >/dev/null || fail=1
[ ! -e "$U/.claude/skills/mph-resume" ] || { echo "uninstall left mph-resume in place"; fail=1; }
[ -d "$U/.claude/skills/other-skill" ] || { echo "uninstall moved a skill that is not ours"; fail=1; }
ls "$U"/.handoff-removed/*/.claude/skills/mph-resume/SKILL.md >/dev/null 2>&1 || { echo "uninstall did not keep a copy"; fail=1; }
grep -q other.sh "$U/.claude/settings.json" && ! grep -q mph-guard "$U/.claude/settings.json" || { echo "uninstall hook cleanup wrong"; fail=1; }
# context hint: learns the size a model was auto-compacted at and warns at half of it
C=$(mktemp -d); mkdir -p "$C/projects/p"
printf '%s\n' '{"type":"assistant","message":{"model":"m-test","usage":{"input_tokens":190000}}}' \
  '{"type":"system","subtype":"compact_boundary","compactMetadata":{"trigger":"auto","preTokens":200000}}' \
  '{"type":"assistant","message":{"model":"m-test","usage":{"input_tokens":110000}}}' > "$C/projects/p/s.jsonl"
printf 'model_advice=off\n' > "$C/g.conf"
echo "{\"session_id\":\"s\",\"transcript_path\":\"$C/projects/p/s.jsonl\"}" | MPH_GUARD_CONF="$C/g.conf" MPH_CONTEXT_STATE="$C/st.json" python3 guard/mph-context.py | grep -q "~200k window" || { echo "context hint did not learn the compaction size"; fail=1; }
printf 'model_advice=off\ncontext_hint_auto=off\n' > "$C/g.conf"
IN2="{\"session_id\":\"s2\",\"transcript_path\":\"$C/projects/p/s.jsonl\"}"
OUT2=$(echo "$IN2" | MPH_GUARD_CONF="$C/g.conf" MPH_CONTEXT_STATE="$C/st2.json" python3 guard/mph-context.py)
[ -z "$OUT2" ] || { echo "context_hint_auto=off still learned"; fail=1; }
# handoff reminder: counts file edits since the last handoff, fires once
python3 - "$C/w.jsonl" <<'PY3'
import json, sys
L = [{"type": "assistant", "message": {"model": "m", "usage": {"input_tokens": 1}, "content": [{"type": "tool_use", "name": "Edit", "input": {}}]}}] * 3
L.append({"type": "user", "message": {"role": "user", "content": "<command-name>/mph-handoff</command-name>"}})
L += [{"type": "assistant", "message": {"model": "m", "usage": {"input_tokens": 1}, "content": [{"type": "tool_use", "name": "Write", "input": {}}]}}] * 2
open(sys.argv[1], "w").write("\n".join(json.dumps(x) for x in L) + "\n")
PY3
IN3="{\"session_id\":\"w\",\"transcript_path\":\"$C/w.jsonl\"}"
printf 'model_advice=off\nhandoff_reminder_edits=3\n' > "$C/w.conf"
[ -z "$(echo "$IN3" | MPH_GUARD_CONF="$C/w.conf" MPH_CONTEXT_STATE="$C/w1.json" python3 guard/mph-context.py)" ] || { echo "handoff reminder ignored the handoff"; fail=1; }
printf 'model_advice=off\nhandoff_reminder_edits=2\n' > "$C/w.conf"
echo "$IN3" | MPH_GUARD_CONF="$C/w.conf" MPH_CONTEXT_STATE="$C/w2.json" python3 guard/mph-context.py | grep -q "2 file edits" || { echo "handoff reminder did not fire"; fail=1; }
[ -z "$(echo "$IN3" | MPH_GUARD_CONF="$C/w.conf" MPH_CONTEXT_STATE="$C/w2.json" python3 guard/mph-context.py)" ] || { echo "handoff reminder fired twice"; fail=1; }
# missed handoff: the scanner flags work after the note, only in that project's folder
G=$(mktemp -d); cp -R examples/workspace/cli-tool "$G/app"
(cd "$G/app" && git init -q && git add -A && git -c user.name=t -c user.email=t@t commit -qm init && echo 1 > a.rs && git add a.rs && git -c user.name=t -c user.email=t@t commit -qm "Add feature")
(cd "$G" && python3 "$ROOT/shared/mph-scan.py" | grep -q "since note: 1 commit (latest: Add feature)") || { echo "scanner missed work after the note"; fail=1; }
(cd examples/workspace && ! python3 ../../shared/mph-scan.py | grep -q "NOT HANDED OFF") || { echo "scanner flagged the examples as not handed off"; fail=1; }
# translations: every README.<lang>.md is listed in the English language line; warn when one lags behind
for t in README.*.md; do
  [ -f "$t" ] || continue
  grep -q "href=\"$t\"" README.md || { echo "translation not linked from README.md: $t"; fail=1; }
  tv=$(sed -n '1s/.*README v\([0-9.]*\).*/\1/p' "$t")
  pv=$(python3 -c 'import json;print(json.load(open(".claude-plugin/plugin.json"))["version"])')
  [ "$tv" = "$pv" ] || echo "note: $t is a translation of v${tv:-?}, README is v$pv (update it when you can)"
done
[ "$fail" -eq 0 ] && echo "all checks passed" || { echo "checks failed"; exit 1; }

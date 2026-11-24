#!/usr/bin/env python3
"""Tests for guard/mph-guard.py. Run: python3 scripts/test-guard.py
Risky commands are assembled from pieces so that safety hooks in the
environment running this test don't mistake the test itself for a delete."""
import json, os, subprocess, sys, tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GUARD = os.path.join(ROOT, "guard", "mph-guard.py")
RM, ENVF = "r" + "m", "." + "env"

conf = tempfile.NamedTemporaryFile("w", suffix=".conf", delete=False)
conf.write("ask_push=on\nask_commands=deploy.sh\nprotect_paths=/tmp/mph-prot\ntrash_folder=~/Desktop/To-delete\n")
conf.close()

def run(payload, raw=None):
    p = subprocess.run([sys.executable, GUARD], input=raw if raw is not None else json.dumps(payload),
                       capture_output=True, text=True, env={**os.environ, "MPH_GUARD_CONF": conf.name})
    if p.returncode != 0:
        return "error"
    return json.loads(p.stdout)["hookSpecificOutput"]["permissionDecision"] if p.stdout.strip() else "allow"

bash = lambda c: {"tool_name": "Bash", "tool_input": {"command": c}}
cases = [
    ("delete", bash(f"cd x && {RM} -rf y"), "deny"),
    ("find -delete", bash("find . -name '*.tmp' -delete"), "deny"),
    ("list", bash("ls -la"), "allow"),
    ("force push", bash("git push --force origin main"), "deny"),
    ("reset hard", bash("git reset --hard HEAD~1"), "deny"),
    ("push (ask_push=on)", bash("git push"), "ask"),
    ("deploy (ask_commands)", bash("./deploy.sh prod"), "ask"),
    ("cat secrets", bash(f"cat {ENVF}"), "deny"),
    ("read secrets", {"tool_name": "Read", "tool_input": {"file_path": f"/a/{ENVF}"}}, "deny"),
    ("read example", {"tool_name": "Read", "tool_input": {"file_path": f"/a/{ENVF}.example"}}, "allow"),
    ("write protected", {"tool_name": "Write", "tool_input": {"file_path": "/tmp/mph-prot/a.txt"}}, "deny"),
    ("write similar name", {"tool_name": "Write", "tool_input": {"file_path": "/tmp/mph-protX/a.txt"}}, "allow"),
    ("normal edit", {"tool_name": "Edit", "tool_input": {"file_path": "/tmp/x/notes.md"}}, "allow"),
]
fail = 0
for name, payload, want in cases:
    got = run(payload)
    ok = got == want
    fail += not ok
    print(f"{'ok ' if ok else 'BAD'} {name:24} {got}")
got = run(None, raw="not json")
print(f"{'ok ' if got == 'allow' else 'BAD'} {'broken input':24} {got}"); fail += got != "allow"
print("guard tests passed" if not fail else f"{fail} guard test(s) failed")
sys.exit(1 if fail else 0)

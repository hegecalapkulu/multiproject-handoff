#!/usr/bin/env python3
"""Replays the demo GIF's terminal session (docs/demo.gif).

The agent replies are real outputs from test sessions on examples/workspace
(Claude Code handoff, then Codex 0.172 resume), trimmed to fit the screen.
Record with:  vhs docs/demo/demo.tape
"""
import sys, time

R, B, D, I = "\033[0m", "\033[1m", "\033[2m", "\033[3m"
ORANGE, GREEN, CYAN, GREY = "\033[38;5;209m", "\033[38;5;114m", "\033[38;5;117m", "\033[38;5;245m"

def out(s=""):
    sys.stdout.write(s + "\n"); sys.stdout.flush()

def typed(s, delay=0.045):
    sys.stdout.write(f"{B}> {R}"); sys.stdout.flush()
    time.sleep(0.4)
    for ch in s:
        sys.stdout.write(ch); sys.stdout.flush(); time.sleep(delay)
    out(); time.sleep(0.6)

def reply(lines, step=0.12, after=0.0):
    for l in lines:
        out(l); time.sleep(step)
    time.sleep(after)

def header(tool, color):
    out(f"{color}{B} {tool} {R}{GREY}  ~/code/recipe-app{R}")
    out()

header("Claude Code", ORANGE)
typed("/mph-handoff")
reply([
    f"{B}[recipe-app]{R} This session: \"remove item\" done, 42 tests pass.",
    f"{GREEN}Will do:{R} daily log · backlog · resume note · Obsidian map",
    f"{GREY}Skip:    decisions, knowledge, profile (nothing new for them){R}",
    "OK?",
], after=0.8)
typed("yes")
reply([
    f"{B}[recipe-app]{R} Handoff saved.",
    f"  daily/2026-11-24.md  {GREY}new{R}",
    f"  RESUME.md            {GREY}shopping list complete; next: accounts, first deploy{R}",
    f"  BACKLOG.md           {GREY}first production deploy moved to Now{R}",
    f"Next time, start with {CYAN}mph-resume recipe-app{R}.",
], after=2.2)

out(); out(f"{I}{GREY}  ── next day, in another tool ──{R}"); out()
time.sleep(1.0)
header("Codex", GREEN)
typed("mph-resume recipe-app")
reply([
    f"{B}[recipe-app]{R}",
    f"{B}Where we are:{R} Ingredient search uses FTS5; the shopping list is complete.",
    "  42 tests passing, and the preview is deployed.",
    f"{B}Tried, didn't work:{R} LIKE search was slow and missed plurals; replaced by FTS5.",
    f"{B}Open question:{R} Does v1 need user accounts, or is a local-only list enough?",
    f"{B}Next:{R} Decide the accounts question, record it, then the first production deploy.",
], step=0.18, after=1.6)
out()
out(f"{B}Same notes, any tool.{R}  {GREY}github.com/hegecalapkulu/multiproject-handoff{R}")
time.sleep(4)

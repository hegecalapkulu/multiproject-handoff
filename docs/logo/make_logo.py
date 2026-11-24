#!/usr/bin/env python3
"""Draws the multiproject-handoff logo (a compass) as a square PNG.
Usage: python3 docs/logo/make_logo.py  ->  .claude-plugin/icon.png and docs/logo/logo.png"""
import math, os
from PIL import Image, ImageDraw, ImageFilter

S = 1024; K = 4; W = S * K          # draw 4x larger, then shrink for smooth edges
BG, RING, TICK = (30, 30, 46), (205, 214, 244), (127, 132, 156)
NORTH, SOUTH, HUB = (240, 130, 90), (137, 220, 235), (30, 30, 46)

img = Image.new("RGBA", (W, W), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
d.rounded_rectangle([0, 0, W - 1, W - 1], radius=int(W * 0.22), fill=BG)

c, r = W / 2, W * 0.36
d.ellipse([c - r, c - r, c + r, c + r], outline=RING, width=int(W * 0.028))
for i in range(12):                  # ticks: long at N/E/S/W, short between
    a = math.radians(i * 30); long = i % 3 == 0
    r1, r2 = r * (0.80 if long else 0.87), r * 0.94
    d.line([(c + r1 * math.sin(a), c - r1 * math.cos(a)), (c + r2 * math.sin(a), c - r2 * math.cos(a))],
           fill=RING if long else TICK, width=int(W * (0.018 if long else 0.010)))

ang = math.radians(45)               # needle points north-east, like 🧭
L, half = r * 0.70, r * 0.17
tip = (c + L * math.sin(ang), c - L * math.cos(ang))
tail = (c - L * math.sin(ang), c + L * math.cos(ang))
side = lambda s: (c + s * half * math.cos(ang), c + s * half * math.sin(ang))
d.polygon([tip, side(1), side(-1)], fill=NORTH)
d.polygon([tail, side(1), side(-1)], fill=SOUTH)
h = r * 0.075
d.ellipse([c - h, c - h, c + h, c + h], fill=HUB, outline=RING, width=int(W * 0.010))

out = img.resize((S, S), Image.LANCZOS)
root = os.path.join(os.path.dirname(__file__), "..", "..")
out.save(os.path.join(root, ".claude-plugin", "icon.png"))
out.resize((256, 256), Image.LANCZOS).save(os.path.join(root, "docs", "logo", "logo.png"))
print("ok")

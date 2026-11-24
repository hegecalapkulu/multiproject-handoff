#!/usr/bin/env python3
"""Draws the multiproject-handoff logo: a thinking meerkat in silhouette,
glasses on, pencil behind the ear. Square PNG.
Usage: python3 docs/logo/make_logo.py  ->  .claude-plugin/icon.png and docs/logo/logo.png"""
import math, os
from PIL import Image, ImageDraw

S = 1024; K = 4; W = S * K             # draw 4x larger, then shrink for smooth edges
BG = (30, 30, 46)                      # dark background
FUR = (242, 196, 140)                  # sand-coloured silhouette
PENCIL, TIP, ERASER = (240, 130, 90), (69, 71, 90), (243, 139, 168)
BUBBLE = (137, 220, 235)

img = Image.new("RGBA", (W, W), (0, 0, 0, 0))
d = ImageDraw.Draw(img)
p = lambda x, y: (x * K, y * K)        # design in 1024 coordinates

def ell(cx, cy, rx, ry, fill=None, outline=None, width=0):
    d.ellipse([p(cx - rx, cy - ry), p(cx + rx, cy + ry)], fill=fill, outline=outline, width=width * K)

def poly(points, fill):
    d.polygon([p(x, y) for x, y in points], fill=fill)

def stroke(points, width, fill):       # thick line with round joints and ends
    pts = [p(x, y) for x, y in points]
    d.line(pts, fill=fill, width=width * K, joint="curve")
    for x, y in points:
        ell(x, y, width / 2, width / 2, fill=fill)

d.rounded_rectangle([0, 0, W - 1, W - 1], radius=int(W * 0.22), fill=BG)

# body, neck, head, snout
ell(478, 800, 158, 360, fill=FUR)                     # body and neck in one (runs off the bottom)
ell(500, 420, 135, 118, fill=FUR)                     # head
poly([(560, 345), (760, 420), (770, 445), (560, 505)], FUR)   # snout
ell(764, 432, 22, 20, fill=TIP)                       # nose

# pencil tucked behind the ear: over the head, under the ear
a = math.radians(-32); ux, uy = math.cos(a), math.sin(a); nx, ny = -uy, ux
x0, y0, L, h = 300, 420, 290, 17
c = lambda t, s: (x0 + ux * t + nx * s, y0 + uy * t + ny * s)
poly([c(0, -h), c(L, -h), c(L, h), c(0, h)], PENCIL)
poly([c(L, -h), c(L + 52, 0), c(L, h)], (250, 227, 176))   # sharpened wood
poly([c(L + 34, -h * 0.35), c(L + 52, 0), c(L + 34, h * 0.35)], TIP)
poly([c(-34, -h), c(0, -h), c(0, h), c(-34, h)], ERASER)
ell(412, 352, 44, 40, fill=FUR)                       # ear, in front of the pencil
ell(414, 355, 20, 18, fill=BG)                        # ear hole

# glasses: lens cut out of the silhouette, eye inside, bridge and arm
ell(585, 410, 48, 44, fill=BG)
ell(585, 410, 48, 44, outline=FUR, width=10)
ell(600, 412, 11, 12, fill=FUR)                       # eye
stroke([(633, 402), (668, 396)], 9, BG)               # bridge towards the snout
stroke([(537, 400), (462, 380)], 9, BG)               # arm to the ear

# thinking: paw up to the chin
stroke([(520, 760), (630, 650), (648, 545)], 54, FUR)
ell(642, 528, 40, 32, fill=FUR)

# thought bubbles
for (bx, by, br) in [(745, 330, 16), (800, 262, 26), (868, 180, 40)]:
    ell(bx, by, br, br, fill=BUBBLE)

out = img.resize((S, S), Image.LANCZOS)
root = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
out.save(os.path.join(root, ".claude-plugin", "icon.png"))
out.resize((256, 256), Image.LANCZOS).save(os.path.join(root, "docs", "logo", "logo.png"))
print("ok")

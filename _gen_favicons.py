"""
Generate LightKey favicon PNGs at 16, 32, 64, 128, 256px
using Pillow (no cairo required).
The icon is the keystone arch from the nav SVG (viewBox 0 0 36 36).
"""
from PIL import Image, ImageDraw
import math

# Colours
BG         = (245, 240, 232, 255)   # --bg parchment
STONE_DARK = (92,  77,  58,  255)   # #5C4D3A arch stroke
COPPER     = (154, 85,  48,  255)   # #9A5530 keystone cap
TEAL       = (61,  122, 138, 180)   # #3D7A8A teal accent (semi)

def draw_icon(size):
    scale = size / 36.0
    img = Image.new("RGBA", (size, size), BG)
    d = ImageDraw.Draw(img)

    def s(v):
        return v * scale

    # ── Arch body (filled parchment, stroked stone-dark) ──────────────────
    # Path: M6 32 L6 18 Q6 6 18 6 Q30 6 30 18 L30 32
    # Approximate the quadratic bezier arcs with polyline points
    def qbez(p0, p1, p2, steps=24):
        pts = []
        for i in range(steps + 1):
            t = i / steps
            x = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
            y = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
            pts.append((x * scale, y * scale))
        return pts

    # Left leg + left arc: M6,32 L6,18 Q6,6 18,6
    left_leg  = [(6*scale, 32*scale), (6*scale, 18*scale)]
    left_arc  = qbez((6,18), (6,6), (18,6))
    # Right arc + right leg: Q30,6 30,18 L30,32
    right_arc = qbez((18,6), (30,6), (30,18))
    right_leg = [(30*scale, 18*scale), (30*scale, 32*scale)]

    arch_outline = left_leg + left_arc + right_arc + right_leg

    # Fill arch interior
    fill_poly = arch_outline + [(30*scale, 32*scale), (6*scale, 32*scale)]
    d.polygon(fill_poly, fill=BG)

    # Stroke arch
    lw = max(1, round(1.5 * scale))
    d.line(arch_outline, fill=STONE_DARK, width=lw)

    # ── Base line ─────────────────────────────────────────────────────────
    d.line([(s(6), s(32)), (s(30), s(32))], fill=STONE_DARK, width=lw)

    # ── Teal accent line ──────────────────────────────────────────────────
    if size >= 32:
        tlw = max(1, round(0.6 * scale))
        d.line([(s(10), s(31)), (s(26), s(31))], fill=TEAL, width=tlw)

    # ── Keystone cap (trapezoid) ──────────────────────────────────────────
    # M14,6 L15,2 L21,2 L22,6
    cap_pts = [(s(14), s(6)), (s(15), s(2)), (s(21), s(2)), (s(22), s(6))]
    cap_fill = (154, 85, 48, 38)   # rgba(154,85,48,0.15)
    d.polygon(cap_pts, fill=cap_fill)
    clw = max(1, round(1.5 * scale))
    d.line(cap_pts + [cap_pts[0]], fill=COPPER, width=clw)

    # ── Keystone circle ───────────────────────────────────────────────────
    if size >= 32:
        r = max(1, round(0.8 * scale))
        cx, cy = s(18), s(3.5)
        d.ellipse([(cx-r, cy-r), (cx+r, cy+r)], fill=COPPER)

    # ── Voussoir hints (only at larger sizes) ─────────────────────────────
    if size >= 64:
        vlw = max(1, round(0.6 * scale))
        hint = (92, 77, 58, 76)
        d.line([(s(10), s(12)), (s(8), s(16))],  fill=hint, width=vlw)
        d.line([(s(26), s(12)), (s(28), s(16))], fill=hint, width=vlw)

    return img

sizes = [16, 32, 64, 128, 256]
for sz in sizes:
    img = draw_icon(sz)
    out = f"/Users/jsp/lightkey/favicon-{sz}.png"
    img.save(out, "PNG")
    print(f"Created {out} ({sz}x{sz})")


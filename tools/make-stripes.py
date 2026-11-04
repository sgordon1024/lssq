#!/usr/bin/env python3
"""Builds mark F, LSSQ drawn in one set of four parallel stripes.

Each letter is a centre line made of straight runs and circular turns. Every
stripe is that centre line offset to one side, so the stripes stay parallel
through every curve, like one ribbon. Run from anywhere:

    python3 tools/make-stripes.py

It writes four files to brand/marks/:
    f-stripes.svg           the wordmark, still
    f-stripes-animated.svg  the same, drawing itself in one stripe at a time
    f-stripe-band.svg       a straight run of the stripes, for decoration
    f-stripe-corner.svg     the stripes turning a corner, for decoration
"""
from math import cos, sin, radians
from pathlib import Path

INK = "#141818"
# Stripe colours, from the right-hand side of each stroke to the left.
COLORS = ["#E2397A", "#F2C230", "#36E2E6", "#B79CF0"]
W, GAP = 5, 1.5                  # stripe width and the dark line between stripes
PITCH = W + GAP
HALF = (len(COLORS) * W + (len(COLORS) - 1) * GAP) / 2   # half the band's width
OUTLINE = 2.5                    # dark edge around each letter
CUT = 3                          # dark gap where the Q's tail crosses its bowl

H, R, CORNER = 80, 20, 18        # centre-line cap height, S bowl radius, L corner radius


def left(h):
    """Unit normal to the left of heading h (degrees, 0 = east, 90 = south)."""
    return sin(radians(h)), -cos(radians(h))


class Stroke:
    """A centre line built from runs and turns, so it can be offset exactly."""

    def __init__(self, x, y, heading):
        self.start, self.heading, self.segs = (x, y), heading, []

    def run(self, length):
        self.segs.append(("run", length))
        return self

    def turn(self, r, deg, side):
        # Split long turns so no single SVG arc covers 180 degrees or more.
        while deg > 0:
            step = min(deg, 90)
            self.segs.append(("turn", r, step, side))
            deg -= step
        return self

    def path(self, d=0.0):
        """SVG path data for this stroke offset d to its left."""
        (x, y), h = self.start, self.heading
        lx, ly = left(h)
        out = [f"M{x + d * lx:.2f} {y + d * ly:.2f}"]
        for seg in self.segs:
            if seg[0] == "run":
                x, y = x + seg[1] * cos(radians(h)), y + seg[1] * sin(radians(h))
                lx, ly = left(h)
                out.append(f"L{x + d * lx:.2f} {y + d * ly:.2f}")
            else:
                _, r, deg, side = seg
                lx, ly = left(h)
                sign = 1 if side == "L" else -1       # the centre is on the turning side
                cx, cy = x + sign * r * lx, y + sign * r * ly
                h = h - deg if side == "L" else h + deg
                lx, ly = left(h)
                x, y = cx - sign * r * lx, cy - sign * r * ly
                rr = r - d if side == "L" else r + d
                sweep = 0 if side == "L" else 1
                out.append(f"A{rr:.2f} {rr:.2f} 0 0 {sweep} {x + d * lx:.2f} {y + d * ly:.2f}")
        return " ".join(out)


def offsets():
    n = len(COLORS)
    return [(i - (n - 1) / 2) * PITCH for i in range(n)]   # right side first


# Letter positions (centre lines). Gaps between letters are about 8 units.
xL = HALF
xS1 = xL + 52.5
xS2 = xS1 + 72.5
xQ = xS2 + 92.5
qc = (xQ, H / 2)
diag = 45


def letters():
    # L flows into the first S along the baseline.
    ls = (Stroke(xL, -HALF, 90)
          .run(H - CORNER + HALF)
          .turn(CORNER, 90, "L")
          .run(xS1 - xL - CORNER)
          .turn(R, 180, "L")
          .turn(R, 240, "R"))
    s2 = (Stroke(xS2 + R * cos(radians(150)), 3 * R + R * sin(radians(150)), 60)
          .turn(R, 240, "L")
          .turn(R, 240, "R"))
    # The bowl starts and ends where the tail crosses it, so the seam stays hidden.
    q = H / 2
    bowl = Stroke(qc[0] + q * cos(radians(diag)), qc[1] + q * sin(radians(diag)), diag - 90).turn(q, 360, "L")
    ux, uy = cos(radians(diag)), sin(radians(diag))
    tail = Stroke(qc[0] + 14 * ux, qc[1] + 14 * uy, diag).run(50)
    return [("ls", ls), ("s2", s2), ("bowl", bowl)], ("tail", tail)


def group(name, stroke, extra_outline=0, cls=""):
    """One letter: its dark backing, then each stripe."""
    parts = [f'<path class="bk {cls}" d="{stroke.path()}" stroke="{INK}" '
             f'stroke-width="{2 * (HALF + OUTLINE + extra_outline):g}"/>']
    for i, (color, d) in enumerate(zip(COLORS, offsets())):
        parts.append(f'<path class="st s{i} {cls}" d="{stroke.path(d)}" stroke="{color}" stroke-width="{W:g}"/>')
    return f'  <g id="f-{name}">\n    ' + "\n    ".join(parts) + "\n  </g>"


def wordmark(animated):
    main, (tname, tail) = letters()
    top, bottom = -HALF - OUTLINE, qc[1] + 64 * sin(radians(diag)) + HALF + CUT
    left_edge, right_edge = -OUTLINE, qc[0] + 64 * cos(radians(diag)) + HALF + CUT
    pad = 8
    vb = (left_edge - pad, top - pad, right_edge - left_edge + 2 * pad, bottom - top + 2 * pad)
    body = [group(n, s, cls=f"l{i}") for i, (n, s) in enumerate(main)]
    body.append(group(tname, tail, extra_outline=CUT - OUTLINE, cls="l3"))
    style = ""
    if animated:
        # Every path has pathLength 1, so one dash pattern draws any of them.
        # Stripe i starts after stripe i-1, and each letter a beat after the last.
        rules = ["path{stroke-dasharray:1 1;stroke-dashoffset:1;animation:draw .7s cubic-bezier(.6,0,.3,1) forwards}",
                 "@keyframes draw{to{stroke-dashoffset:0}}",
                 "@media (prefers-reduced-motion:reduce){path{animation:none;stroke-dashoffset:0}}"]
        for i in range(4):
            for s in range(-1, len(COLORS)):
                sel = f".bk.l{i}" if s < 0 else f".s{s}.l{i}"
                delay = max(s, 0) * 0.45 + i * 0.12
                rules.append(f"{sel}{{animation-delay:{delay:.2f}s}}")
        style = "  <style>" + "".join(rules) + "</style>\n"
    svg = "\n".join(body)
    if animated:
        svg = svg.replace('<path ', '<path pathLength="1" ')
    title = "LSSQ mark F: Stripe Letters" + (" (animated)" if animated else "")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb[0]:.2f} {vb[1]:.2f} {vb[2]:.2f} {vb[3]:.2f}" '
            f'fill="none" stroke-linejoin="round">\n  <title>{title}</title>\n{style}{svg}\n</svg>\n')


def decoration(stroke, viewbox, title):
    parts = [f'<path d="{stroke.path()}" stroke="{INK}" stroke-width="{2 * (HALF + OUTLINE):g}"/>']
    for color, d in zip(COLORS, offsets()):
        parts.append(f'<path d="{stroke.path(d)}" stroke="{color}" stroke-width="{W:g}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" fill="none">\n'
            f'  <title>{title}</title>\n  ' + "\n  ".join(parts) + "\n</svg>\n")


def band(length=400):
    """A straight run of the stripes: the same set, for dividers and borders."""
    y0 = HALF + OUTLINE
    return decoration(Stroke(0, y0, 0).run(length), f"0 0 {length} {2 * y0:g}", "LSSQ stripe band")


def corner(size=120, r=36):
    """The stripes running in along the top and turning down the right side."""
    y0 = HALF + OUTLINE
    stroke = Stroke(0, y0, 0).run(size - y0 - r).turn(r, 90, "R").run(size - y0 - r)
    return decoration(stroke, f"0 0 {size} {size}", "LSSQ stripe corner")


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "brand" / "marks"
    (out / "f-stripes.svg").write_text(wordmark(False))
    (out / "f-stripes-animated.svg").write_text(wordmark(True))
    (out / "f-stripe-band.svg").write_text(band())
    (out / "f-stripe-corner.svg").write_text(corner())
    for name in ("f-stripes.svg", "f-stripes-animated.svg", "f-stripe-band.svg", "f-stripe-corner.svg"):
        print(out / name)

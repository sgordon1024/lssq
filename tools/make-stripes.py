#!/usr/bin/env python3
"""Builds mark F, LSSQ written in one continuous ribbon of three stripes.

The whole word is one centre line made of straight runs and circular turns:
down the L, along the baseline into the first S, out of its top and straight
down into the second S, the same again into the Q, and round the bowl. Every
stripe is that centre line offset to one side, so the stripes stay parallel
through every curve. Where one part of the ribbon passes over another, the
part underneath is cut away, so the mark needs no outline and works in one
colour.
Run from anywhere:

    python3 tools/make-stripes.py

It writes five files to brand/marks/:
    f-stripes.svg           the wordmark, still
    f-stripes-animated.svg  the same, each stripe writing the word in turn
    f-stripes-mono.svg      the wordmark in one colour, for one-ink printing
    f-stripe-band.svg       a straight run of the stripes, for decoration
    f-stripe-corner.svg     the stripes turning a corner, for decoration
"""
from math import cos, sin, tan, radians, pi
from pathlib import Path

INK = "#141818"
# Stripe colours, from the right-hand side of the ribbon to the left.
COLORS = ["#E2397A", "#F2C230", "#36E2E6"]
W, GAP = 8, 3                    # stripe width and the clear gap between stripes
PITCH = W + GAP
HALF = (len(COLORS) * W + (len(COLORS) - 1) * GAP) / 2   # half the ribbon's width

H = 88                           # cap height of the centre line
R = H / 4                        # S bowl radius
CORNER = 20                      # L corner radius
Q = H / 2                        # Q bowl radius

DRAW, STAGGER = 3.6, 0.6         # seconds for one stripe to write the word, and between stripes
TAILT = 0.6                      # seconds for the Q's tail, once a stripe reaches the end


def left(h):
    """Unit normal to the left of heading h (degrees, 0 = east, 90 = south)."""
    return sin(radians(h)), -cos(radians(h))


def step(x, y, h, seg):
    """Where a segment that starts at (x, y) facing h ends, and its turn centre."""
    if seg[0] == "run":
        return x + seg[1] * cos(radians(h)), y + seg[1] * sin(radians(h)), h, None
    _, r, deg, side = seg
    sign = 1 if side == "L" else -1           # the centre is on the turning side
    lx, ly = left(h)
    cx, cy = x + sign * r * lx, y + sign * r * ly
    h = h - deg if side == "L" else h + deg
    lx, ly = left(h)
    return cx - sign * r * lx, cy - sign * r * ly, h, (cx, cy)


class Stroke:
    """A centre line built from runs and turns, so it can be offset exactly."""

    def __init__(self, x, y, heading):
        self.start, self.heading, self.segs = (x, y), heading, []

    def run(self, length):
        self.segs.append(("run", length))
        return self

    def turn(self, r, deg, side):
        # Split long turns so no single SVG arc covers 180 degrees or more.
        while deg > 1e-9:
            chunk = min(deg, 90)
            self.segs.append(("turn", r, chunk, side))
            deg -= chunk
        return self

    def mark(self):
        return len(self.segs)

    def states(self):
        """(x, y, heading) at the start and after every segment."""
        (x, y), h = self.start, self.heading
        out = [(x, y, h)]
        for seg in self.segs:
            x, y, h, _ = step(x, y, h, seg)
            out.append((x, y, h))
        return out

    def slice(self, i, j=None):
        """A new stroke made of this one's segments from index i up to j."""
        x, y, h = self.states()[i]
        s = Stroke(x, y, h)
        s.segs = self.segs[i:j]
        return s

    def length(self, d=0.0, upto=None):
        total = 0.0
        for seg in self.segs[:upto]:
            if seg[0] == "run":
                total += seg[1]
            else:
                _, r, deg, side = seg
                total += (r - d if side == "L" else r + d) * radians(deg)
        return total

    def points(self, d=0.0, every=2.0):
        """Points along the offset line, for working out bounds."""
        (x, y), h = self.start, self.heading
        lx, ly = left(h)
        pts = [(x + d * lx, y + d * ly)]
        for seg in self.segs:
            if seg[0] == "run":
                n = max(1, int(seg[1] / every))
                for k in range(1, n + 1):
                    t = seg[1] * k / n
                    pts.append((x + t * cos(radians(h)) + d * lx, y + t * sin(radians(h)) + d * ly))
                x, y, h, _ = step(x, y, h, seg)
            else:
                _, r, deg, side = seg
                n = max(2, int(r * radians(deg) / every))
                for k in range(1, n + 1):
                    xk, yk, hk, _ = step(x, y, h, ("turn", r, deg * k / n, side))
                    kx, ky = left(hk)
                    pts.append((xk + d * kx, yk + d * ky))
                x, y, h, _ = step(x, y, h, seg)
            lx, ly = left(h)
        return pts

    def path(self, d=0.0):
        """SVG path data for this stroke offset d to its left."""
        (x, y), h = self.start, self.heading
        lx, ly = left(h)
        out = [f"M{x + d * lx:.2f} {y + d * ly:.2f}"]
        for seg in self.segs:
            x, y, h, _ = step(x, y, h, seg)
            lx, ly = left(h)
            if seg[0] == "run":
                out.append(f"L{x + d * lx:.2f} {y + d * ly:.2f}")
            else:
                _, r, deg, side = seg
                rr = r - d if side == "L" else r + d
                sweep = 0 if side == "L" else 1
                out.append(f"A{rr:.2f} {rr:.2f} 0 0 {sweep} {x + d * lx:.2f} {y + d * ly:.2f}")
        return " ".join(out)


def offsets():
    n = len(COLORS)
    return [(i - (n - 1) / 2) * PITCH for i in range(n)]   # right side first


# Letter positions, as centre lines. Each S's top end runs straight down into
# the next letter at LINK degrees, the angle that just clears the S's own lower
# bowl, and that sets how far apart the letters sit.
LINK = 41
xL = HALF
xS1 = xL + 60
xS2 = xS1 + 2 * R / tan(radians(LINK / 2))
DIAG = 2 * R * (1 + cos(radians(LINK))) / sin(radians(LINK))      # S to S
QDIAG = ((Q - R) + (Q + R) * cos(radians(LINK))) / sin(radians(LINK))   # S to Q
xQ = xS2 + (R + Q) * sin(radians(LINK)) + QDIAG * cos(radians(LINK))
LEAD = 50                        # how much of the link into the Q passes over the bowl's end


def word():
    """The word as one stroke, and the parts of it that pass over another part."""
    s = (Stroke(xL, -HALF, 90)
         .run(H - CORNER + HALF).turn(CORNER, 90, "L").run(xS1 - xL - CORNER)   # L
         .turn(R, 180, "L").turn(R, 180 + LINK, "R")                            # first S
         .run(DIAG)
         .turn(R, 180 + LINK, "L").turn(R, 180 + LINK, "R")                     # second S
         .run(QDIAG - LEAD))
    a = s.mark()
    s.run(2)
    k0 = s.mark()
    s.run(LEAD - 2).turn(Q, 10, "L")
    k1 = s.mark()
    s.turn(Q, 2, "L")
    b = s.mark()
    s.turn(Q, 348, "L")          # round the bowl, ending tucked under the link
    ux, uy = cos(radians(45)), sin(radians(45))
    tail = Stroke(xQ + 14 * ux, Q + 14 * uy, 45).run(62)
    return s, (a, b), (k0, k1), tail


# A hidden path sits a little past the end of its dash, so no sliver of it shows
# at either end. The gap in the dash pattern is longer than any path.
HIDE = 1.02


def ease(t):
    return (1 - cos(pi * t)) / 2


def keyframes(name, lo=0.0, hi=1.0, steps=30):
    """Dash offsets for a path that is drawn while the pen goes from lo to hi of the way along."""
    frames = []
    for k in range(steps + 1):
        shown = min(max((ease(k / steps) - lo) / (hi - lo), 0), 1)
        frames.append(f"{100 * k / steps:.2f}%{{stroke-dashoffset:{1 - shown if shown else HIDE:.4f}}}")
    return f"@keyframes {name}{{{''.join(frames)}}}"


def wordmark(animated=False, mono=False):
    s, (a, b), (k0, k1), tail = word()
    link = s.slice(a, b)
    pts = [p for d in (-HALF, HALF) for stroke in (s, tail) for p in stroke.points(d)]
    pad = 8
    x0, y0 = min(p[0] for p in pts) - pad, min(p[1] for p in pts) - pad
    x1, y1 = max(p[0] for p in pts) + pad, max(p[1] for p in pts) + pad
    box = f'x="{x0:.2f}" y="{y0:.2f}" width="{x1 - x0:.2f}" height="{y1 - y0:.2f}"'
    colors = [INK] * len(COLORS) if mono else COLORS
    dl = ' pathLength="1"' if animated else ""
    cut = f'stroke="#000" stroke-width="{2 * (HALF + GAP):g}"'

    # The ribbon is drawn once under a mask that cuts it away wherever another
    # part passes over it, then those parts are drawn again on top.
    body = [
        "  <defs>",
        f'    <mask id="f-under" maskUnits="userSpaceOnUse" {box}>',
        f'      <rect {box} fill="#fff"/>',
        f'      <path class="cut c0"{dl} d="{s.slice(k0, k1).path()}" {cut}/>',
        f'      <path class="cut c1"{dl} d="{tail.path()}" {cut}/>',
        "    </mask>",
        "  </defs>",
        '  <g mask="url(#f-under)">',
    ]
    for i, (color, d) in enumerate(zip(colors, offsets())):
        body.append(f'    <path class="st s{i}"{dl} d="{s.path(d)}" stroke="{color}" stroke-width="{W:g}"/>')
    body.append("  </g>")
    for part, stroke in (("ov", link), ("tl", tail)):
        for i, (color, d) in enumerate(zip(colors, offsets())):
            body.append(f'  <path class="st {part} s{i}"{dl} d="{stroke.path(d)}" stroke="{color}" stroke-width="{W:g}"/>')

    style = ""
    if animated:
        # Each stripe writes the whole word, then the Q's tail, one stripe after
        # another. The copy of the link over the Q is drawn in step with the pen.
        rules = [f".st,.cut{{stroke-dasharray:1 2;stroke-dashoffset:{HIDE};animation:draw {DRAW}s linear forwards}}",
                 keyframes("draw"),
                 f".tl,.c1{{animation-duration:{TAILT}s}}"]
        for i, d in enumerate(offsets()):
            whole = s.length(d)
            rules.append(f".s{i}{{animation-delay:{i * STAGGER:.2f}s}}")
            rules.append(f".ov.s{i}{{animation-name:ov{i}}}")
            rules.append(keyframes(f"ov{i}", s.length(d, a) / whole, s.length(d, b) / whole))
            rules.append(f".tl.s{i}{{animation-delay:{i * STAGGER + DRAW:.2f}s}}")
        whole = s.length()
        rules.append(".c0{animation-name:c0}")
        rules.append(keyframes("c0", s.length(0, k0) / whole, s.length(0, k1) / whole))
        rules.append(f".c1{{animation-delay:{DRAW:.2f}s}}")
        rules.append("@media (prefers-reduced-motion:reduce){.st,.cut{animation:none;stroke-dashoffset:0}}")
        style = "  <style>" + "".join(rules) + "</style>\n"

    title = "LSSQ mark F: Stripe Letters" + (" (one colour)" if mono else "") + (" (animated)" if animated else "")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.2f} {y0:.2f} {x1 - x0:.2f} {y1 - y0:.2f}" fill="none">\n'
            f"  <title>{title}</title>\n{style}" + "\n".join(body) + "\n</svg>\n")


def decoration(stroke, viewbox, title):
    parts = [f'<path d="{stroke.path(d)}" stroke="{color}" stroke-width="{W:g}"/>'
             for color, d in zip(COLORS, offsets())]
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" fill="none">\n'
            f'  <title>{title}</title>\n  ' + "\n  ".join(parts) + "\n</svg>\n")


def band(length=400):
    """A straight run of the stripes: the same set, for dividers and borders."""
    return decoration(Stroke(0, HALF, 0).run(length), f"0 0 {length} {2 * HALF:g}", "LSSQ stripe band")


def corner(size=120, r=36):
    """The stripes running in along the top and turning down the right side."""
    stroke = Stroke(0, HALF, 0).run(size - HALF - r).turn(r, 90, "R").run(size - HALF - r)
    return decoration(stroke, f"0 0 {size} {size}", "LSSQ stripe corner")


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "brand" / "marks"
    files = {
        "f-stripes.svg": wordmark(),
        "f-stripes-animated.svg": wordmark(animated=True),
        "f-stripes-mono.svg": wordmark(mono=True),
        "f-stripe-band.svg": band(),
        "f-stripe-corner.svg": corner(),
    }
    for name, svg in files.items():
        (out / name).write_text(svg)
        print(out / name)

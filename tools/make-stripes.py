#!/usr/bin/env python3
"""Builds mark F, LSSQ written in one continuous ribbon of three stripes.

The whole word is one centre line made of straight runs and circular turns:
down the L, along the baseline into the first S, out of its top and straight
down into the second S, the same again into the Q, and round the bowl. Every
stripe is that centre line offset to one side, so the stripes stay parallel
through every curve. The Q's tail is a second, short ribbon that sweeps out
over the bowl. Where one part passes over another, the part underneath is cut
away, so the mark needs no outline and works in one colour.
Run from anywhere:

    python3 tools/make-stripes.py

It writes these files to brand/marks/:
    f-stripes.svg           the wordmark, still (the default)
    f-stripes-animated.svg  the same, each stripe writing the word in turn, for special moments
    f-stripes-mono.svg      the wordmark in one colour (ink), for one-ink printing
    f-stripes-cream.svg     the wordmark in cream, for one colour on dark grounds
    f-q.svg, f-q-mono.svg   the Q on its own, for avatars, app icons and stickers
    f-stripe-band.svg       a straight run of the stripes, for decoration
    f-stripe-corner.svg     the stripes turning a corner, for decoration
and these pattern tiles to brand/patterns/:
    road.svg                the ribbon snaking along in S-curves, repeats sideways
    arches.svg              rainbow arches side by side, repeats sideways
    glints.svg              a scatter of glint stars, repeats both ways
"""
from math import cos, sin, tan, radians, pi
from pathlib import Path

INK = "#141818"
CREAM = "#FFF6E8"
# Stripe colours, from the right-hand side of the ribbon to the left.
COLORS = ["#E2397A", "#F2C230", "#36E2E6"]
# In colour, each stripe fades from a lighter tint at the top of the letters to
# a deeper shade at the baseline, like an airbrushed 80s sign.
SHADES = [("#E96598", "#D31F64"), ("#F5D060", "#EAB40F"), ("#63E9EC", "#1BD4D8")]
W, GAP = 8, 3                    # stripe width and the clear gap between stripes
PITCH = W + GAP
HALF = (len(COLORS) * W + (len(COLORS) - 1) * GAP) / 2   # half the ribbon's width

H = 88                           # cap height of the centre line
R = H / 4                        # S bowl radius
CORNER = 20                      # L corner radius
Q = H / 2                        # Q bowl radius

DRAW, STAGGER = 2.7, 0.4         # seconds for one stripe to write the word, and between stripes
TAILT, TAILGAP = 0.45, 0.07      # seconds for each stripe of the Q's tail, and between them
SHINE, SPARK = 0.8, 0.7          # the glint across the finished word, and the star that ends it


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
LEAD = 66                        # how much of the link into the Q passes over the bowl's end


def word():
    """The word as one stroke, the part of it that passes over the bowl's end,
    and the part of the link cut away under it."""
    s = (Stroke(xL, -HALF, 90)
         .run(H - CORNER + HALF).turn(CORNER, 90, "L").run(xS1 - xL - CORNER)   # L
         .turn(R, 180, "L").turn(R, 180 + LINK, "R")                            # first S
         .run(DIAG)
         .turn(R, 180 + LINK, "L").turn(R, 180 + LINK, "R")                     # second S
         .run(QDIAG - LEAD))
    # The cut starts far enough back that the bowl's end meets one straight edge
    # all the way across, and the copy drawn on top covers both ends of the cut.
    a = s.mark()
    s.run(2)
    k0 = s.mark()
    s.run(LEAD - 2).turn(Q, 10, "L")
    k1 = s.mark()
    s.turn(Q, 2, "L")
    b = s.mark()
    s.turn(Q, 348, "L")          # round the bowl, ending tucked under the link
    return s, (a, b), (k0, k1)


TAIL_R, TAIL_OUT = 48, 20        # the tail's turn radius, and how far it runs on along the baseline


def tail(cx=None, out=None):
    """The Q's tail: out of the bowl's counter and across it at 45 degrees, then
    curving down to run along the baseline, so the word ends the way the L starts."""
    cx = xQ if cx is None else cx
    out = TAIL_OUT if out is None else out
    c = cos(radians(45))
    run = (H - Q - 14 * c - TAIL_R * (1 - c)) / c      # lands the tail on the baseline
    return Stroke(cx + 14 * c, Q + 14 * c, 45).run(run).turn(TAIL_R, 45, "L").run(out)

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


def star(x, y, r):
    """A four-pointed glint centred on (x, y)."""
    k = r * 0.16
    return (f"M{x:.2f} {y - r:.2f}Q{x + k:.2f} {y - k:.2f} {x + r:.2f} {y:.2f}"
            f"Q{x + k:.2f} {y + k:.2f} {x:.2f} {y + r:.2f}Q{x - k:.2f} {y + k:.2f} {x - r:.2f} {y:.2f}"
            f"Q{x - k:.2f} {y - k:.2f} {x:.2f} {y - r:.2f}Z")


def wordmark(animated=False, mono=False):
    """The wordmark. mono is False for colour, True for ink, or a colour of its own."""
    s, (a, b), (k0, k1) = word()
    t = tail()
    link = s.slice(a, b)
    pts = [p for d in (-HALF, HALF) for stroke in (s, t) for p in stroke.points(d)]
    pad = 8
    x0, y0 = min(p[0] for p in pts) - pad, min(p[1] for p in pts) - pad
    x1, y1 = max(p[0] for p in pts) + pad, max(p[1] for p in pts) + pad
    box = f'x="{x0:.2f}" y="{y0:.2f}" width="{x1 - x0:.2f}" height="{y1 - y0:.2f}"'
    dl = ' pathLength="1"' if animated else ""
    n = len(COLORS)

    defs = []
    paints = paint_defs(mono, defs)

    # The ribbon is drawn once under a mask that cuts it away wherever another
    # part passes over it, then those parts are drawn again on top. The tail's
    # cut follows each of its stripes, so the bowl stays whole until the tail
    # is drawn over it.
    defs += [f'    <mask id="f-under" maskUnits="userSpaceOnUse" {box}>',
             f'      <rect {box} fill="#fff"/>',
             f'      <path class="cut c0"{dl} d="{s.slice(k0, k1).path()}" stroke="#000" stroke-width="{2 * (HALF + GAP):g}"/>']
    for i, d in enumerate(offsets()):
        defs.append(f'      <path class="cut tl s{i}"{dl} d="{t.path(d)}" stroke="#000" stroke-width="{W + 2 * GAP:g}"/>')
    defs.append("    </mask>")

    def stripes(part, stroke, paint=None, indent="  "):
        cls = f"st {part} " if part else "st "
        return [f'{indent}<path class="{cls}s{i}"{dl} d="{stroke.path(d)}" stroke="{paint or paints[i]}" stroke-width="{W:g}"/>'
                for i, d in enumerate(offsets())]

    body = ['  <g mask="url(#f-under)">', *stripes("", s, indent="    "), "  </g>",
            *stripes("ov", link), *stripes("tl", t)]

    style = ""
    if animated:
        # Once the word is written, a glint runs across it and a star twinkles
        # at the end of the tail. Both draw on a white copy of the word.
        tx, ty, _ = t.states()[-1]
        sx, sy, sr = tx - 4, ty - HALF, pad + 3        # on the tail's top corner, inside the frame
        lit = ['    <mask id="f-lit" maskUnits="userSpaceOnUse" {box}>'.replace("{box}", box),
               '      <g mask="url(#f-under)">',
               *[f'        <path d="{s.path(d)}" stroke="#fff" stroke-width="{W:g}"/>' for d in offsets()],
               "      </g>",
               *[f'      <path d="{stroke.path(d)}" stroke="#fff" stroke-width="{W:g}"/>' for stroke in (link, t) for d in offsets()],
               "    </mask>",
               '    <linearGradient id="f-glint"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
               '<stop offset=".5" stop-color="#fff" stop-opacity=".6"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>',
               f'    <radialGradient id="f-glow"><stop offset="0" stop-color="{CREAM}" stop-opacity=".9"/>'
               f'<stop offset="1" stop-color="{CREAM}" stop-opacity="0"/></radialGradient>']
        defs += lit
        gw, skew = 38, 22
        lean = (y1 - y0) * tan(radians(skew))
        gx = x0 - gw - lean - 4
        travel = (x1 - x0) + gw + 2 * lean + 8
        body += ['  <g mask="url(#f-lit)">',
                 f'    <g transform="skewX(-{skew})"><rect class="glint" x="{gx + y1 * tan(radians(skew)):.2f}" y="{y0:.2f}" width="{gw}" height="{y1 - y0:.2f}" fill="url(#f-glint)"/></g>',
                 "  </g>",
                 f'  <g class="spark"><circle cx="{sx:.2f}" cy="{sy:.2f}" r="{sr * 0.55:.2f}" fill="url(#f-glow)"/>'
                 f'<path d="{star(sx, sy, sr)}" fill="{CREAM}"/></g>']

        # Each stripe writes the whole word, one stripe after another, with the
        # copy of the link over the Q drawn in step with the pen. Then the tail
        # sweeps over the finished bowl, its cut keeping pace with it.
        word_end = DRAW + (n - 1) * STAGGER
        tail_end = word_end + (n - 1) * TAILGAP + TAILT
        glint_at = tail_end - 0.15
        rules = [f".st,.cut{{stroke-dasharray:1 2;stroke-dashoffset:{HIDE}}}",
                 f".st{{animation:draw {DRAW}s linear forwards}}",
                 keyframes("draw")]
        for i, d in enumerate(offsets()):
            whole = s.length(d)
            rules.append(f".s{i}{{animation-delay:{i * STAGGER:.2f}s}}")
            rules.append(f".ov.s{i}{{animation-name:ov{i}}}")
            rules.append(keyframes(f"ov{i}", s.length(d, a) / whole, s.length(d, b) / whole))
            rules.append(f".tl.s{i}{{animation:tail {TAILT}s cubic-bezier(.3,.5,.3,1) {word_end + i * TAILGAP:.2f}s forwards}}")
        whole = s.length()
        rules.append(f".c0{{animation:c0 {DRAW}s linear forwards}}")
        rules.append(keyframes("c0", s.length(0, k0) / whole, s.length(0, k1) / whole))
        rules.append(f"@keyframes tail{{from{{stroke-dashoffset:{HIDE}}}to{{stroke-dashoffset:0}}}}")
        rules.append(f".glint{{animation:glint {SHINE}s cubic-bezier(.45,0,.55,1) {glint_at:.2f}s both}}")
        rules.append(f"@keyframes glint{{to{{transform:translateX({travel:.2f}px)}}}}")
        rules.append(f".spark{{opacity:0;transform-box:fill-box;transform-origin:center;"
                     f"animation:spark {SPARK}s ease-out {glint_at + SHINE * 0.6:.2f}s both}}")
        rules.append("@keyframes spark{0%{opacity:1;transform:scale(0) rotate(-45deg)}"
                     "40%{opacity:1;transform:scale(1) rotate(0deg)}100%{opacity:0;transform:scale(.2) rotate(30deg)}}")
        rules.append("@media (prefers-reduced-motion:reduce){.st,.cut{animation:none;stroke-dashoffset:0}.glint,.spark{animation:none}}")
        style = "  <style>" + "".join(rules) + "</style>\n"

    title = "LSSQ mark F: Stripe Letters" + (" (one colour)" if mono else "") + (" (animated)" if animated else "")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.2f} {y0:.2f} {x1 - x0:.2f} {y1 - y0:.2f}" fill="none">\n'
            f"  <title>{title}</title>\n{style}  <defs>\n" + "\n".join(defs) + "\n  </defs>\n" + "\n".join(body) + "\n</svg>\n")


def paint_defs(mono, defs):
    """Stroke paints for each stripe: the shaded gradients in colour, or one flat colour."""
    if mono:
        return [INK if mono is True else mono] * len(COLORS)
    for i, (base, (light, deep)) in enumerate(zip(COLORS, SHADES)):
        defs.append(f'    <linearGradient id="f-g{i}" gradientUnits="userSpaceOnUse" x1="0" y1="{-HALF:g}" x2="0" y2="{H + HALF:g}">'
                    f'<stop offset="0" stop-color="{light}"/><stop offset=".45" stop-color="{base}"/>'
                    f'<stop offset="1" stop-color="{deep}"/></linearGradient>')
    return [f"url(#f-g{i})" for i in range(len(COLORS))]


def qmark(mono=False):
    """The Q on its own, for avatars, app icons and stickers. The bowl is a closed
    ring that starts and ends right under the tail, so its seam never shows."""
    c = cos(radians(45))
    ring = Stroke(Q * c, Q + Q * c, -45).turn(Q, 360, "L")
    t = tail(0, out=4)                                  # a shorter flick keeps it compact in a round avatar
    pts = [p for d in (-HALF, HALF) for stroke in (ring, t) for p in stroke.points(d)]
    x0, y0 = min(p[0] for p in pts), min(p[1] for p in pts)
    x1, y1 = max(p[0] for p in pts), max(p[1] for p in pts)
    side = max(x1 - x0, y1 - y0) + 24                  # square, so it sits centred in a round avatar
    vx, vy = (x0 + x1 - side) / 2, (y0 + y1 - side) / 2
    box = f'x="{vx:.2f}" y="{vy:.2f}" width="{side:.2f}" height="{side:.2f}"'
    defs = []
    paints = paint_defs(mono, defs)
    defs.append(f'    <mask id="q-under" maskUnits="userSpaceOnUse" {box}>')
    defs.append(f'      <rect {box} fill="#fff"/>')
    for d in offsets():
        defs.append(f'      <path d="{t.path(d)}" stroke="#000" stroke-width="{W + 2 * GAP:g}"/>')
    defs.append("    </mask>")
    body = ['  <g mask="url(#q-under)">',
            *[f'    <path d="{ring.path(d)}" stroke="{paints[i]}" stroke-width="{W:g}"/>' for i, d in enumerate(offsets())],
            "  </g>",
            *[f'  <path d="{t.path(d)}" stroke="{paints[i]}" stroke-width="{W:g}"/>' for i, d in enumerate(offsets())]]
    title = "LSSQ mark F: the Q" + (" (one colour)" if mono else "")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vx:.2f} {vy:.2f} {side:.2f} {side:.2f}" fill="none">\n'
            f"  <title>{title}</title>\n  <defs>\n" + "\n".join(defs) + "\n  </defs>\n" + "\n".join(body) + "\n</svg>\n")


def tile(width, height, parts, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width:g} {height:g}" width="{width:g}" height="{height:g}" fill="none">\n'
            f'  <title>{title}</title>\n  ' + "\n  ".join(parts) + "\n</svg>\n")


def flat(stroke):
    return [f'<path d="{stroke.path(d)}" stroke="{color}" stroke-width="{W:g}"/>' for color, d in zip(COLORS, offsets())]


def road(r=26, pad=9):
    """The ribbon snaking along in S-curves. One period wide, so it repeats sideways
    with no seam; it's drawn a period past each edge so the ends never show."""
    period, mid = 4 * r, r + HALF + pad
    s = Stroke(-period, mid, -90)
    for _ in range(3):
        s.turn(r, 180, "R").turn(r, 180, "L")
    return tile(period, 2 * mid, flat(s), "LSSQ pattern: road")


def arches(r=34, leg=18, pad=6):
    """A rainbow arch on two short legs, like a sunrise. Repeats sideways into a row."""
    width, height = 2 * (r + HALF) + 2 * GAP, leg + r + HALF + pad
    s = Stroke(width / 2 - r, height + 1, -90).run(leg + 1).turn(r, 180, "R").run(leg + 1)
    return tile(width, height, flat(s), "LSSQ pattern: arches")


def glints(size=160):
    """A loose scatter of glint stars, the one that ends the animation."""
    stars = [(28, 34, 9, CREAM), (104, 22, 5, COLORS[1]), (132, 92, 11, COLORS[1]), (58, 118, 6, CREAM), (12, 150, 4, COLORS[2])]
    return tile(size, size, [f'<path d="{star(x, y, r)}" fill="{color}"/>' for x, y, r, color in stars], "LSSQ pattern: glints")


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
        "f-stripes-cream.svg": wordmark(mono=CREAM),
        "f-q.svg": qmark(),
        "f-q-mono.svg": qmark(mono=True),
        "f-stripe-band.svg": band(),
        "f-stripe-corner.svg": corner(),
    }
    patterns = out.parent / "patterns"
    patterns.mkdir(exist_ok=True)
    files.update({f"../patterns/{name}.svg": make() for name, make in (("road", road), ("arches", arches), ("glints", glints))})
    for name, svg in files.items():
        (out / name).resolve().write_text(svg)
        print((out / name).resolve())

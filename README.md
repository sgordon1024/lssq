# LSSQ Workshop

Open design work for [Last Saturday Side Quest](https://lastsaturdaysidequest.odoo.com/), a monthly weekend gathering for nomads built on music, play, wellness and connection.

**Site:** https://sgordon1024.github.io/lssq/

This isn't LSSQ's official site. It's where a new logo, a website Jake can update himself, and event chat get designed and built, in the open, so anyone can follow along or pitch in.

## The plan

1. **Logo mark** (now). One simple shape that keeps LSSQ's colors and 80s feel and still reads as an Instagram avatar or a 16px browser tab.
2. **A site Jake can edit** (next). Everything on the current site, but Jake can change it, preview it and open a pull request without touching code.
3. **Event chat** (later). A home for each event's group chat. It might be an existing service rather than a new app.

## What's where

| Path | What it is |
| --- | --- |
| `index.html` | Home page: the plan and what's being worked on now |
| `presentations/` | Every review deck, newest first (decks live in Google Slides) |
| `prototypes/` | Working prototypes. `logo-marks/` is the current one |
| `brand/marks/` | Each logo mark as an SVG, plus PNG exports in `png/` |
| `assets/site.css` | Shared styles for the site |
| `tools/export-marks.sh` | Re-exports every mark SVG to a 1024px PNG (needs Chrome and python3) |

The site is plain HTML and CSS with no build step. GitHub Pages serves it straight from `main`.

## Pitch in

- **Have an idea?** Open an issue.
- **Want to change something?** Open a pull request. Keep it small and say what it's for.
- **Adding a mark?** Put the SVG in `brand/marks/` (100 × 100 viewBox, LSSQ colors), run `zsh tools/export-marks.sh`, and add it to the prototype.

To preview the site locally:

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000.

## Colors

| Name | Hex |
| --- | --- |
| Banner pink | `#E2397A` |
| Record yellow | `#F2C230` |
| Outline cyan | `#36E2E6` |
| Confetti lavender | `#B79CF0` |
| Turntable black | `#141818` |
| Cream | `#FFF6E8` |

Type is Urbanist, the font on LSSQ's current site.

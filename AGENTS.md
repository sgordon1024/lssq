# AGENTS.md: everything you need to pick up LSSQ Workshop

This file is the handoff for any AI assistant (ChatGPT, Codex, Claude) or person taking over this work. Read it first, keep it current, and update the **Status** section whenever something changes. If this file and the code disagree, the code wins. Fix this file.

Last updated: November 19, 2026.

## The short version

- **What:** an open, public workshop where Steve Gordon designs a new logo, an easier website and event tools for Last Saturday Side Quest (LSSQ).
- **Why:** Steve loves LSSQ and wants a regular back-and-forth with Jake, who runs it, and to show what he can do for them if they want it.
- **Done when:** Jake has seen a logo direction and a working site he can edit himself, and he and Steve have a regular check-in.
- **Right now:** Steve OKed the website plan on November 16, and a sample of the new site is live at https://sgordon1024.github.io/lssq-site/ (repo `sgordon1024/lssq-site`), with made-up events. His notes are in, and the new scroll-of-scenes home page went live on November 18 (`lssq-site` #5). Jake can now update it through any AI assistant that works on GitHub: the assistant follows `lssq-site/AGENTS.md`, and a check plus a lock on design code keep mistakes from going live (`lssq-site` #6 and #9). The point-and-click editor's sign-in is on hold. The brand direction (https://sgordon1024.github.io/lssq/brand/) is still waiting on his review, and he hasn't reached out to Jake yet.
- **Live site:** https://sgordon1024.github.io/lssq/
- **Repo:** https://github.com/sgordon1024/lssq (public, `main` is live)
- **New site:** https://sgordon1024.github.io/lssq-site/, repo https://github.com/sgordon1024/lssq-site (public). It has its own README.

## People

| Who | Role | Notes |
| --- | --- | --- |
| Steve Gordon (GitHub `sgordon1024`) | Owner. Product designer who also codes. | Makes every decision. All contact with Jake goes through him. |
| Jake | Leader of LSSQ. Not a web designer. | The person Steve coordinates with. His contact details are kept out of this public repo on purpose; ask Steve. |

**Never contact Jake, post, or publish anything on LSSQ's behalf** unless Steve asks for that exact thing.

## Handoff

Steve built everything so far with Claude. On November 5 he handed the work to ChatGPT, and on November 12 Claude picked it back up for the brand direction. Whoever picks it up next: this file and the repo are the whole record; there's no other shared doc.

**Where it stands (November 18)**

- Steve picked F, the striped ribbon. The still logo is the default; the draw-in animation is for special moments only.
- The [brand direction page](https://sgordon1024.github.io/lssq/brand/) (`brand/index.html`) sets the logo rules, motion, color, type, patterns, sample layouts and voice. It's draft 1, for Steve's review.
- The [website plan](https://sgordon1024.github.io/lssq/presentations/2026-11-13-website-plan/) (`presentations/2026-11-13-website-plan/`) is approved. On November 16 Steve OKed all four calls: Decap CMS with drafts, a small build step (Eleventy) for the new site only, a new `lssq-site` repo, and the page list as proposed.
- The [new site](https://sgordon1024.github.io/lssq-site/) is built (the plan's step 1): home, events, one page per event, contact and a 404, in the brand style, with made-up upcoming events and the two real past ones (SQUS, Shastaween). Every page says it's a sample, not LSSQ's official site, and search engines are told to skip it.
- Steve's first notes on the sample site are done (`lssq-site` #3): the logo draws in on hover, the next-up card leads with photos from past weekends, the pillar cards have icons, Our story is its own page, each event photo has a countdown, and an event's page says the spot is a secret (and when it drops) until it has coordinates. Four photos come from LSSQ's own site; the rest are Unsplash stock, each credited.
- Steve loved sweet-tape.com's home page and page transitions and asked for that feel on the home page only. It's live (`lssq-site` #5, merged November 18): a collage hero of taped photos and stickers, the tagline riding a ribbon, the pillars sliding sideways, a photo wall of past weekends, the next weekend's photo opening up, and the donate Q turning like a record. Every page gets a stripe wipe between pages and a light grain. It uses GSAP (ScrollTrigger) and Lenis, home page only; with reduced motion it's a plain scroll. Steve's first notes on it are folded in (even, roomier ribbon lines with useful copy in Urbanist; full scrapbook pillar pages with three photos, four solid stickers and tags each; solid story page numbers; the Q stops upright). His second notes are in too: the leaf sticker is now a sprout, the Q makes one slow turn and rests upright, every page's main headline gets the stripe echo hover, and the echo has wider ink gaps so it reads.
- Editing (step 2) is done through an AI assistant. Steve wanted Jake to use whichever assistant he likes, and said it has to be dead simple for him. In `lssq-site`:
  - `AGENTS.md` is the guide every assistant reads first. It talks to Jake in plain words, does the whole job, always sends a preview and publishes only on his yes. `CLAUDE.md` and `GEMINI.md` point to it.
  - `HOW-TO-UPDATE.md` is Jake's one page: say what you want, look at the preview, say "publish it".
  - `npm run check` checks every event and the site's words against the editor's own field rules (`src/admin/config.yml`) plus photo rules, in plain words, and runs on every pull request.
  - `npm run photos` gets phone photos ready: upright, 2000px and 1 MB at most, location data stripped (the repo is public), and HEIC turned into JPEG on a Mac.
  - `main` is protected. It only takes pull requests that pass the check. Content can go live on that alone; anything else needs Steve's review (`.github/CODEOWNERS`). Steve's own pull requests aren't held for review, so they merge normally once the check passes.
  - Tested end to end with a made-up event and a phone-sized photo, and with two previews published at once (that race is fixed in #9). The tests were closed, not merged.
  - Photos from a phone (`lssq-site` #10): most assistants can only see photos attached in the chat, not save them. So the assistant sends Jake an upload link for his change, and he taps "choose your files", picks the photos and taps "Commit changes". Phones drop location data on browser uploads. The assistant names the photos, picks where they go, writes their descriptions and deletes the unused ones. HEIC photos only turn into JPEGs on a Mac. Making that work anywhere needs a new package (`heic-decode`), which waits on Steve's OK. One catch: a photo uploaded from a computer keeps its location in that change's history, even though it's stripped before going live.
- The point-and-click editor at `/admin/` (Decap) is still there but can't sign in, and that's on hold until we know whether Jake wants it too. Sign-in needs the helper in `lssq-site/auth/` deployed, which needs Steve's Cloudflare and GitHub accounts. If it comes back, its photo uploads would need shrinking at build time, since Jake can't run `npm run photos` from it.
- The six round 1 options (A to F) stay in the [deck](https://sgordon1024.github.io/lssq/presentations/2026-11-04-logo-marks/) and the [prototype](https://sgordon1024.github.io/lssq/prototypes/logo-marks/) as the record.
- Jake hasn't seen anything yet. Steve has a short intro email drafted to send from his personal email. It links the deck and this site, says it's a passion project with no strings attached, and asks Jake for a call and a regular check-in. The draft lives with Steve, not in this repo.

**Waiting on Steve**

1. Review the brand direction page and send notes.
2. When Jake is in, set him up for editing (about 15 minutes, together): a free GitHub account, add him as a collaborator on `lssq-site`, connect his AI assistant to GitHub, sign him in to GitHub on his phone's browser, and walk him through `HOW-TO-UPDATE.md`.
3. Send the intro email to Jake and set up the check-in. The draft links the deck; it could link the brand page or the sample site instead.
4. Sign in to his personal Gmail in the Claude app's browser so Jake's newsletters can be found. The connected Gmail is his work account.
5. OK or skip adding `heic-decode` to `lssq-site`, so HEIC photos convert on any computer, not just a Mac.

**What to do next**

1. On Jake's first change, check that a content change can go live without review and that anything beyond content waits for Steve. That second part couldn't be tested with only Steve's account, because GitHub doesn't hold an owner's own pull requests.
2. If Steve brings the point-and-click editor back: he deploys the sign-in helper and sends its address (steps in the `lssq-site` README under "Set up sign-in"). Then set `base_url` in `lssq-site/src/admin/config.yml`, add a build step that shrinks uploaded photos, sign in and save a test draft.
3. Fold Steve's notes on the brand page and the sample site in. If the brand files change, copy the changed SVGs into `lssq-site/src/brand/`.
4. The plan's step 3 (show Jake, fill in real events, links and photos) waits on Steve and Jake. Don't add Jake as a collaborator or share the site with him until Steve says so.

**Good to know**

- F, its Q, its one-color versions and the patterns in `brand/patterns/` are all generated by `tools/make-stripes.py`. Don't hand-edit those SVGs; change the script and run it.
- To check an animation frame by frame, fetch the SVG's text into a page, set it as `innerHTML`, then pause every animation from `document.getAnimations()` and set its `currentTime`. You can't pause a plain `<img>`, and a hidden browser tab may not advance it at all.
- The PNG export needs macOS with Google Chrome. If you can't run it, say so in the pull request and Steve will re-export.
- Steve asked for Firecrawl to find event photos. It isn't set up for this project, so the photos were found with the browser instead (LSSQ's Instagram needs a sign-in, so nothing came from there). Add the Firecrawl connector to this project if you want it next time.
- Every change so far is one merged pull request: #1 the deck and this file, #2 Steve's first notes on A and D plus badge E, #3 mark F, #4 F as one ribbon, #5 F polish, #6 the handoff notes, #7 the homepage timeline, #8 the brand direction, #9 the stripe echo hover, #10 the On site photos, #11 trimming them to Steve's picks, #12 the website plan, #13 pointing the workshop at the new site, #14 dropping colored card edges in the plan deck, #15 noting Steve's first sample site notes, #16 the swell, #17 noting the new home page preview, #18 noting the first notes on it, #19 the wider echo gaps and the second notes, #20 noting the new home page is live, #21 noting the AI editing setup, #22 noting phone photos and newsletters. The new site's repo started with one commit to `main`; from there it's pull requests too.

## About LSSQ

- **Last Saturday Side Quest** is a monthly weekend gathering for nomads, held somewhere new each month (a desert lot, a mountain forest, the Baja coast). The tagline: "Different location every month. Same family every time."
- It started as single-day meetups on the last Saturday of the month and grew into weekend-long events. It's funded almost entirely by donations (Patreon, Venmo, PayPal).
- **Four pillars:** wellness, play, music and connection. Attendees share their own gifts and talents.
- **Voice:** warm, playful, communal. "Your people are out here."
- **Current site:** https://lastsaturdaysidequest.odoo.com/ (Odoo free plan). One home page plus a Contact page. Sections: hero, What is LSSQ, Upcoming events, Our journey, Donate.
- **Instagram:** @lastsaturdaysidequest
- **Event chat today:** each event gets its own WhatsApp group, linked by hand from the site.

### Problems with the current site (reviewed Nov 4, 2026)

- The events list is out of date (September and Halloween 2026 events have passed) and Shastaween is listed twice.
- The hero image doesn't load.
- Yellow text on cyan in "Our journey" is hard to read.
- The header logo is too small to read, and each event's WhatsApp link is added by hand.

### The current logo

A retro 80s badge: a yellow record on a turntable, a pink banner with "Last Saturday Side Quest" in striped lettering, stars, triangles, a lightning bolt and a cyan outline. It's fun at full size, but there is no simple mark, so it's unreadable as an Instagram avatar, a WhatsApp group icon or a browser tab icon. That's the problem round 1 solves.

## The plan

Work happens in this order. Don't jump ahead.

1. **Logo mark (now).** One simple shape that keeps LSSQ's colors and 80s feel and still reads at 16px.
2. **A site Jake can edit (now).** Everything on the current site, rebuilt so Jake can change it, preview it and publish it without help. Jake isn't a web designer, so it has to be very simple. In its own repo, `lssq-site`. A sample is live, and Jake updates it by asking any AI assistant, which follows `lssq-site/AGENTS.md`. The Decap editor stays as an option.
3. **Event chat (later).** Something like WhatsApp, but just for LSSQ events. An existing service may be a better fit than a new app; decide when we get there.

Steve also wants a regular check-in with Jake. Setting that up is Steve's job.

## Status

November 19: adding photos from a phone is simpler (`lssq-site` #10). Jake sends newsletters, and Steve wants a template for them, maybe automated. Finding past issues waits on Steve signing in to his personal email.

November 18, night: Jake can update the sample site through any AI assistant (`lssq-site` #6 and #9). Tested end to end. The point-and-click editor's sign-in is on hold.

November 18, evening: Steve OKed the new home page and it's live (`lssq-site` #5). Next he wants to work on editing, with guidelines so Jake can update the site through any AI assistant.

November 18, later still: Steve's first and second notes on the new home page are in the preview (`lssq-site` #5). Still waiting on his OK to ship it.

November 18, later: the sweet-tape-style home page is built and waiting on Steve's review (`lssq-site` #5, preview link above).

November 18: the stripes sit into the site better (the swell under the home page's top section and on the story page, the big Q behind Donate).

November 16, later: Steve's first notes on the sample site are live (`lssq-site` #3). See Decisions.

November 16: Steve OKed the website plan. The new site is built and live at https://sgordon1024.github.io/lssq-site/ with sample content. Previews work (checked with a test pull request, closed). The editor loads but can't sign in until Steve sets up the sign-in helper. The workshop's home page Now card and plan point to the new site, and the plan opens on the Website stage.

November 13: the website plan deck is drafted and the home page's Now card and plan point to it. The logo marks deck is marked "F picked" in the deck list.

November 12: Steve picked F. The brand direction page is live at `brand/` and the home page's Now card and plan point to it. The nav on the home, brand and presentations pages is Home, Brand, Presentations, GitHub, and the Q is the site's browser tab icon.

Homepage refreshed November 5: shorter public copy, LSSQ-only header, and a compact interactive plan immediately after the intro.

The timeline uses `assets/timeline.js` to enhance readable stage details into tabs. Check click/repeated selection, Left/Right/Home/End, visible focus, phone widths and reduced motion when changing it. Without JavaScript all stage details remain readable. No build or CI test suite is configured.

| Step | State | Where |
| --- | --- | --- |
| Review the current site and logo | Done | Findings above |
| Sketch logo mark options (round 1) | Done | `prototypes/logo-marks/`, `brand/marks/` |
| Steve's first review notes (A, D, new E) | Done | See Decisions |
| Striped LSSQ wordmark (F), with animation and decorations | Done | `brand/marks/f-*.svg`, `tools/make-stripes.py` |
| F reworked into one ribbon: three thicker stripes, no black, slower animation, one-color version | Done | Same files, plus `f-stripes-mono.svg` |
| F polished: clean Q bowl end, curved tail, gradients, glint and sparkle ending, a bit faster | Done | Same files |
| Public repo and project site | Done | This repo, GitHub Pages |
| Logo marks review deck | Done | `presentations/2026-11-04-logo-marks/` |
| Steve reviews each mark and picks a direction | Done (F, Nov 12) | See Decisions |
| Brand direction: logo rules, motion, color, type, patterns, samples, voice | Draft 1 done | `brand/index.html` |
| Steve reviews the brand direction | **Waiting on Steve** | https://sgordon1024.github.io/lssq/brand/ |
| Refine the chosen mark, plus one-color and small versions | In progress | Q mark and cream version added (`f-q*.svg`, `f-stripes-cream.svg`) |
| Show Jake the logo | In progress (Steve) | Intro email drafted; Steve sends it from his personal email |
| Set a regular check-in with Jake | In progress (Steve) | The intro email asks for one |
| Plan the site: pages, home page sketches, editing options, recommendation | Draft 1 done | `presentations/2026-11-13-website-plan/` |
| Steve reviews the website plan | Done (OKed Nov 16) | See Decisions |
| Build the new site's pages with sample content (plan step 1) | Done | `lssq-site` repo, https://sgordon1024.github.io/lssq-site/ |
| Editing with drafts and previews (plan step 2) | Done (Nov 18), through an AI assistant | `lssq-site` #6 and #9, `AGENTS.md` and `HOW-TO-UPDATE.md` there. The point-and-click editor's sign-in is on hold |
| Steve's first notes on the sample site | Done (Nov 16) | `lssq-site` #3 |
| Steve looks over the updated sample site | **Waiting on Steve** | https://sgordon1024.github.io/lssq-site/ |
| Home page as a scroll of scenes, stripe wipe between pages | Done (live Nov 18) | `lssq-site` #5 |
| Walk Jake through editing | Not started (Steve) | |
| Compare event chat options, then decide with Jake | Not started | |

Steve also tracks this in his own task app (Master Tasker). You can't see it, so this table is the shared record.

## Round 1 logo marks

All six keep LSSQ's colors. SVGs are in `brand/marks/`, PNG exports in `brand/marks/png/`. A to D are marks, E is a badge for stickers and patches, and F is a wordmark.

| Option | File | Idea | Why it could work | Watch out |
| --- | --- | --- | --- | --- |
| A, Record Q | `a-record-q.svg` | The record from today's badge becomes the Q in LSSQ; the tonearm (pivot, arm, angled headshell and needle) is its tail. | Closest to what people know, so it reads as a cleanup, not a rebrand. | Yellow needs its dark outline on light backgrounds. |
| B, Quest Marker | `b-quest-marker.svg` | The "!" that floats over a side quest in a video game. | Boldest and simplest; easiest to spot in a feed. | Drops the record, so music isn't in the mark. |
| C, Four Pillars | `c-four-pillars.svg` | A compass star, one point per pillar (pink music, yellow play, cyan wellness, lavender connection). | Tells the whole LSSQ story; colors can carry into the site. | Hard to print in one ink; needs a one-color version. |
| D, Last Saturday Patch | `d-patch.svg` (full), `d-sunset.svg` (small) | A striped sunset over mountains with the road in, ringed like a camp patch. | Most outdoors and nomad. Small version is just the sunset. | The full patch's text is too small for avatars. |
| E, Record Sunset | `e-record-sunset.svg` | A's record sets like a sun behind pink mountains, in a cyan arch that reads LAST SATURDAY, under a yellow SIDE QUEST banner like today's. Cream die-cut border. | Made for stickers and embroidered patches: thick outlines, flat colors, big type. Steve loves the badge idea. | Merch only. Pair it with A for avatars and the browser tab. |
| F, Stripe Letters | `f-stripes.svg`, `f-stripes-animated.svg`, `f-stripes-mono.svg` | LSSQ written in one unbroken ribbon of three stripes (pink, yellow, cyan), like a 70s racing stripe that never lifts off. The L runs along the baseline into the first S, each S's top runs straight down into the next letter, and the Q's tail curves out along the baseline. | The most retro option. In the animated file each stripe writes the whole word in turn, then a glint runs across it. No outline, so it works in one ink, and the same stripes make decorations (`f-stripe-band.svg`, `f-stripe-corner.svg`). | A wordmark, so too wide for avatars. Pair it with A. |

The starting recommendation was A for the mark and E for stickers. **Steve picked F on November 12**, with the Q on its own as the small mark. The other options stay here as the record.

### The stripes (F)

F is generated, not drawn by hand. Edit `tools/make-stripes.py` (letter shapes, stripe colors, widths) and run `python3 tools/make-stripes.py`, then `zsh tools/export-marks.sh`. The whole word is one center line of straight runs and circular turns, and each stripe is that line offset to one side, so the stripes stay parallel through every curve.

- **Shape:** down the L, along the baseline into the first S, out of its top and straight down into the second S, then the same into the Q. The links run at 41 degrees, the angle that just clears each S's lower bowl, and that sets the letter spacing. The Q's bowl closes by tucking under the link, all three stripes stopping on one straight edge. Its tail crosses the bowl at 45 degrees, then curves down to run along the baseline, so the word ends the way the L starts.
- **Crossings without black:** the ribbon is drawn once under an SVG mask that cuts it away wherever another part passes over it (the link into the Q and the tail), then those parts are drawn again on top. That's what lets the gaps stay see-through and the one-color version work. The cut under the link starts far enough back that the bowl's end meets one straight edge, and the cut under the tail follows each tail stripe as it draws, so the bowl stays whole until the tail covers it.
- **Stripe spec:** three stripes, each 8 units wide, with a 3-unit clear gap between them and no outline. On a straight run, top to bottom: cyan, yellow, pink. Cap height is 88 units on the center line.
- **Color:** in the color files, each stripe fades from a lighter tint at the top of the letters to a deeper shade at the baseline (the shades are `SHADES` in the generator). The one-color version and the decorations stay flat.
- **Animation:** every path in `f-stripes-animated.svg` has `pathLength="1"` and a CSS dash animation inside the file, so it plays even as a plain `<img>`. Each stripe takes 2.7 seconds to write the word, 0.4 seconds after the last. Once the bowl is complete, the tail sweeps over it, a glint runs across the word, and a star twinkles on the end of the tail and fades, so it's clear it's over. About 5 seconds in all. It respects reduced motion. To replay it, reload the image with a new query string (the deck does this when you land on the slide).
- **The Q on its own** (`f-q.svg`, `f-q-mono.svg`): the Q's ring plus a short tail flick, in a square viewBox. Its ring starts and ends under the tail, so there's no seam. This is the mark for avatars, app icons, stickers and the browser tab, down to 16px.
- **Patterns** (`brand/patterns/`): `road.svg` (the ribbon snaking along, tiles sideways), `swell.svg` (a long, low wave of it, made of wide shallow arcs; the site's section edge), `arches.svg` (a row of three-stripe arches) and `glints.svg` (the closing star, scattered). All use the same stripe widths and gaps.
- **Decoration in CSS:** for a quick divider without the SVG, `background: linear-gradient(#36E2E6 0 8px, transparent 8px 11px, #F2C230 11px 19px, transparent 19px 22px, #E2397A 22px 30px);` on a 30px-tall element.

### Centering lettering

Lettering in the badges (D and E) sits on curved paths. To center it in a band, put the baseline half a cap height off the band's middle radius (Urbanist's cap height is 0.7 of the font size): inward for text on top, outward for text along the bottom.

## Brand

| Name | Hex | Use |
| --- | --- | --- |
| Banner pink | `#E2397A` | Stripes, shapes, big type (4.3:1 on black, so not for small text) |
| Record yellow | `#F2C230` | Primary buttons, numbers |
| Outline cyan | `#36E2E6` | Labels, links |
| Deep pink | `#C42566` | Pink text on cream (5.2:1) |
| Confetti lavender | `#B79CF0` | A rare extra; not in the ribbon |
| Turntable black | `#141818` | Background |
| Panel | `#1c2323` | Cards and panels |
| Line | `#2a3333` | Borders |
| Cream | `#FFF6E8` | Text |
| Muted | `#a9b7b4` | Secondary text |

- **Type:** headlines in Fraunces (Google Fonts) at Black 900 with Soft 100 and Wonky on (`font-variation-settings: "SOFT" 100, "WONK" 1`). Everything else in Urbanist, the font on LSSQ's current site. Labels are Urbanist 800, caps, +16% tracking. The "stripe echo" headline treatment is a CSS `text-shadow` stack in `brand/index.html`. On screen it rests in solid cream with a glimmer, and on hover the stripes spring out one at a time (registered custom properties `--e1` to `--e3` with a `linear()` spring easing); in print it's used finished. Monoton appears only in the prototype's wordmark lockups.
- **On site photos** (`brand/on-site/`): the scenes are AI-made. The projector party came from Nano Banana Pro in Weave with the real logo as input. The others came from Figma's image generator with a blank surface, and the real logo was then placed in with a Python script (perspective, lighting, texture). The page says they're AI samples, not real LSSQ events. Keep that label.
- **The full brand rules** (logo use, sizes, color pairs, type scale, patterns, voice) are on the brand direction page, `brand/index.html`.
- **Look:** dark background, bright 80s colors, rounded shapes. The site uses one dark theme on purpose.
- **Cards:** never a colored border or stripe on one edge of a card (top, left or any side). On a rounded card it bends into a curve. Steve's rule for this project and everything else. To color-code a card, put a small colored dot by its title.

## What's where

| Path | What it is |
| --- | --- |
| `index.html` | Home: what this is, the "Now" card, the plan, how to pitch in |
| `presentations/index.html` | List of every deck, newest first |
| `presentations/YYYY-MM-DD-name/index.html` | One deck. Self-contained HTML slides |
| `brand/index.html` | The brand direction page: logo, motion, color, type, patterns, samples and voice |
| `brand/patterns/*.svg` | Generated stripe patterns (road, arches, glints) |
| `brand/on-site/*.jpg` | Sample event photos for the brand page's On site section |
| `prototypes/logo-marks/index.html` | The round 1 prototype: every option at real sizes |
| `brand/marks/*.svg` | Each mark, 100 × 100 viewBox (D's full patch is 200 × 200, E is 222 × 222 to leave room for its die-cut border, and F's wordmark is wide, sized by its generator) |
| `brand/marks/png/*.png` | 1024px transparent PNG exports of each SVG. Use these, not the SVGs, wherever a mark with lettering (D's patch, E) is shown as an image, since an SVG in an `<img>` can't load Urbanist |
| `assets/timeline.js` | Homepage plan tabs and keyboard interaction |
| `assets/site.css` | Shared styles for the home and presentations pages |
| `tools/export-marks.sh` | Re-exports every SVG to PNG (needs Google Chrome and python3, macOS) |
| `tools/make-stripes.py` | Generates mark F, its Q, one-color versions, stripe decorations and patterns |
| `tools/render.html` | Used by the export script |
| `README.md` | Short public intro for contributors |
| `AGENTS.md` | This file |

This workshop site is plain HTML and CSS with a small vanilla JavaScript timeline, no build step and no dependencies. The new LSSQ site is a separate repo, `sgordon1024/lssq-site`, built by Eleventy with GitHub Actions; its README covers how it works. GitHub Pages serves `main` from the repo root, so a merge to `main` goes live in about a minute. Links between pages are relative because the site lives under `/lssq/`.

## How to do common things

**Preview locally**

```bash
python3 -m http.server 8000
```

Then open http://localhost:8000.

**Make a new deck**

1. Copy `presentations/2026-11-04-logo-marks/` to `presentations/<date>-<short-name>/`.
2. Edit the slides. Each slide is a `<section class="slide">` on a 1280 × 720 stage. Every slide after the first has the `hidden` attribute, and each `aria-label` says "Slide N of M". The counter, Back and Next buttons, arrow keys and `#N` slide links work out the slide count on their own.
3. Keep one message per slide and reuse the slide types already there: cover, two-column, one mark per slide, comparison table.
4. Add the deck to the top of the list in `presentations/index.html` (copy the existing `<li class="deck">`).
5. Point the home page's "Now" card at it if it's the current work.
6. Check it at desktop size and at phone width (under 760px the slides stack and scroll).

Decks are HTML in this repo, not Google Slides or PowerPoint. That's Steve's call for this project.

**Add or change a mark**

1. Put the SVG in `brand/marks/` with a 100 × 100 viewBox, using only the brand colors.
2. Run `zsh tools/export-marks.sh` to make the PNGs.
3. Add it to `prototypes/logo-marks/index.html`. That page draws each mark from inline SVG symbols at the top of the file, so copy the shapes into a new `<symbol>`. (F is the exception: the page shows its generated files as images.)

**Update the "Now" card**

Edit the `<!-- Keep this card pointed at whatever is being worked on right now. -->` section in `index.html`.

## How Steve works

- **Writing:** plain English, short. Lead with the result and anything he has to do. No walls of text or long lists of caveats. Avoid em dashes.
- **Git:** work on a branch, open a pull request, and merge it yourself once checks pass. There are no CI checks yet. Stop and ask only for something risky or destructive.
- **Public repo:** anyone can read it. Keep personal contact details, private notes and anything Jake hasn't agreed to share out of it.
- **Labeling:** the site always says it isn't LSSQ's official site and links to theirs.
- **Scope:** finish the current step before starting the next. Write ideas for later down under Open questions rather than building them.

## Decisions so far

| Date | Decision |
| --- | --- |
| Nov 4, 2026 | This is a personal project for Steve, not a paid one. |
| Nov 4, 2026 | The repo is public so other people can contribute. |
| Nov 4, 2026 | Plain HTML and CSS on GitHub Pages, no build step. |
| Nov 4, 2026 | Decks are HTML pages in `presentations/`, not Google Slides. |
| Nov 4, 2026 | Every mark keeps the current logo's colors and 80s feel. Urbanist is the type. |
| Nov 4, 2026 | Coordinate with Jake through Steve only. |
| Nov 4, 2026 | Steve's first notes: make A's tonearm smaller and look like an arm with a needle, not a pill; center D's lettering in the pink ring; he loves the badge idea, so add one made for stickers and patches (became E). All three are done. |
| Nov 4, 2026 | Steve asked for an LSSQ letters option that feels like one set of multicolored stripes, very retro, in the same colors, that can animate stripe by stripe and double as decoration (became F). |
| Nov 4, 2026 | Steve's notes on F: remove the black, connect all the letters as organically as possible, slow the animation, thicker lines (three stripes is fine), and make it one shape that works in black and white. Done: one continuous ribbon, three stripes, no outline, about 5.4 seconds. Looping the ribbon over and under the second S was tried and dropped because it read as "LS3P". |
| Nov 4, 2026 | Steve's second notes on F: fix the pointed pink end where the bowl tucks under the link, curve the tail, add a tasteful vintage look (he loves the animation, it reminds him of 80s PBS idents), speed it up a bit, draw the whole bowl before the tail covers it, and end clearly. Done: one straight edge for the bowl's end, a tail that lands on the baseline, soft gradients, a glint and a closing star, about 5 seconds. |
| Nov 5, 2026 | Steve hands the work from Claude to ChatGPT. He'll reach out to Jake himself, from his personal email. |
| Nov 12, 2026 | Steve picks F, the striped ribbon, and asks for a brand direction page covering colors, custom type and patterns. |
| Nov 12, 2026 | The logo is still by default. The draw-in animation is for special moments only (first visit, event announcements, video intros). |
| Nov 12, 2026 | Steve loves the stripe echo. It becomes a hover state: solid cream with a glimmer at rest, then the stripes bounce out in a friendly, not cheesy, way. |
| Nov 12, 2026 | Steve asked for an On site section with realistic photos of the brand at events. Ten sample photos were made; Steve kept the dance-party projection, blacklight banner, tattoo, patch and window cling. |
| Nov 12, 2026 | Draft 1 choices: Fraunces (soft, wonky) for headlines over Urbanist; the Q alone as the small mark; ink and cream as the two grounds; lavender only as a rare extra; deep pink for pink text on cream. All open to Steve's notes. |
| Nov 16, 2026 | Steve OKs the website plan as proposed: Decap CMS with drafts, a small build step (Eleventy) for the new site only, a new `lssq-site` repo in his GitHub, and the page list (home, events, one page per event, contact). The workshop itself stays plain HTML with no build step. |
| Nov 16, 2026 | Steve's first notes on the sample site: animate the logo on hover; make the next-up card about the experience, with photos from past events (stock from Unsplash or Pexels if none); give the cards icons; make Our story its own page with photos; add a fun countdown on the event photo; and handle locations that aren't picked until about a month out. All done in `lssq-site` #3. |
| Nov 16, 2026 | No colored edge borders on cards, ever. The pillar cards on the new site and two spots in the website plan deck now use a small dot by the title instead. |
| Nov 18, 2026 | Steve asked for the stripes to sit into the site better. The road at the bottom of the home page's top section became the swell (lower, longer waves) and replaced the divider line under it; the story page uses it too. The donate band's arches became the Q, blown up and running off the edge (hanging from the top right on phones). |
| Nov 18, 2026 | Steve loves sweet-tape.com, especially its page transitions, and OKed a plan to bring its feel over: only the home page becomes the big scrolling, parallax scene; the rest of the site stays straightforward and just gets the stripe wipe between pages and a light grain. Built on a branch with a preview link so he can review it before it goes live. |
| Nov 18, 2026 | Steve's notes on the new home page, round 2: the stripe echo hover goes on every page's main headline, not just the story page, and its colors get more space between them (wider ink gaps, slightly thinner stripes, here and on the brand page). The donate Q should turn once, not twice, and rest upright. |
| Nov 18, 2026 | Steve OKs the new home page; `lssq-site` #5 is merged and live. He wants Jake to be able to update the site through whatever AI assistant he likes, guided by written rules in the repo. |
| Nov 18, 2026 | Steve: build the AI editing setup, and make it dead simple for Jake, who doesn't know any of this. Built in `lssq-site` #6: the assistant guide, Jake's one page, the content check, the photo fixer and the lock on design code. The point-and-click editor's sign-in (Cloudflare and OAuth) is on hold until we know whether Jake wants it too. |
| Nov 18, 2026 | No database for now. If LSSQ needs sign-ups or RSVPs later, link a sign-up service from each event (a new field) instead of storing people's details in the site. |

## Open questions

- **Brand direction notes:** Steve is reviewing draft 1. Open bits: is Fraunces the right headline face, and does the stripe echo earn its place?
- **Sample site notes:** the new home page is live. More notes from Steve as they come.
- **Jake's assistant:** which one he uses decides small things, like whether it can merge or save photo attachments itself. `lssq-site/AGENTS.md` covers both cases. Try it with him during setup.
- **Point-and-click editor:** does Jake want Decap as well? If yes, set up sign-in and shrink its photo uploads at build time.
- **Sign-ups:** if events need RSVPs or sign-ups, pick a service with Jake (a form or an RSVP tool) and add a sign-up link field to events. A database only makes sense if LSSQ wants its own accounts, which means holding people's details and looking after them.
- **Real photos:** the sample uses Unsplash stock where LSSQ has no photo. Swap in Jake's photos when he shares them.
- **Newsletters:** Jake sends newsletters. Steve wants a template Jake can fill in, and maybe automation, like a draft built from the site's upcoming events. First, read a few past issues to see what they cover and what sends them. LSSQ's site has no sign-up form and nothing turns up on the web, so they're probably in Steve's personal inbox, maybe as Patreon posts.
- **Event photo galleries:** a past event's page shows one photo, and the home page has a few more. A strip of photos from each weekend could hold the rest. Steve's call.
- **Where will the rebuilt site live?** It could stay on GitHub Pages, with or without a custom domain. Jake decides.
- **Event chat:** WhatsApp Communities, Discord, Geneva or something custom. Decide with Jake later.
- **License:** none has been chosen yet. Ask Steve before adding one.

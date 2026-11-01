---
name: Munim
version: 2.0.0
format: DESIGN.md (Google Stitch format, sections as in VoltAgent/awesome-design-md)
description: >
  Design system for Munim, an open-source tool that turns phone photos of
  invoices, delivery challans and purchase orders into a checked evidence file
  for a small supplier chasing a late payment. A modern, confident product
  interface on a deep navy shell, with the working vocabulary of the paper trail
  kept where it carries meaning: carbon sheet colours, the red-pen correction and
  the rubber stamp.
colors:
  bond: "#F5F6FA"            # page canvas
  sheet: "#FFFFFF"           # cards, tables, forms
  ink: "#111827"             # primary text
  ink-2: "#3B4354"           # secondary text
  muted: "#596173"           # captions, helper text
  hairline: "#E4E7EF"        # card edges and dividers, never the only edge of a control
  hairline-strong: "#868FA3" # control edges
  ballpoint: "#2F45D8"       # the one accent: actions, links, selection, corrections
  ballpoint-pressed: "#2233AE" # hover and pressed state of the primary button
  ballpoint-wash: "#EDF0FE"  # selected row, active tab
  red-pen: "#C4281C"         # a check failed; strike-through of a wrong value
  red-wash: "#FDECEA"
  tick: "#157347"            # a check passed
  tick-wash: "#E5F6ED"
  highlighter: "#F2B92E"     # needs a human; a fill, never text
  highlighter-wash: "#FEF5DA"
  carbon-pink: "#F6C9C1"     # delivery challan
  carbon-yellow: "#F6DF8E"   # purchase order
  night: "#0D1230"           # app sidebar, hero and summary surfaces
  night-2: "#1C2350"         # raised surface on night
  on-night: "#F4F6FF"        # text on night
  on-night-muted: "#B7BFDD"  # secondary text on night
  sky: "#9DB0FF"             # links and marks on night
typography:
  family-ui: "'Inter Variable', Mukta, 'Noto Sans Devanagari', system-ui, sans-serif"
  family-hand: "Kalam, 'Noto Sans Devanagari', cursive"
  display-hero: { family: ui, size: 56px, line: 62px, weight: 600, tracking: -0.03em }
  display-amount: { family: ui, size: 44px, line: 50px, weight: 600, tracking: -0.02em, features: [tnum, lnum] }
  display: { family: ui, size: 30px, line: 36px, weight: 600, tracking: -0.02em }
  h1: { family: ui, size: 28px, line: 36px, weight: 600, tracking: -0.02em }
  h2: { family: ui, size: 19px, line: 28px, weight: 600, tracking: -0.01em }
  h3: { family: ui, size: 15px, line: 22px, weight: 600 }
  body: { family: ui, size: 15px, line: 24px, weight: 400 }
  body-sm: { family: ui, size: 13px, line: 20px, weight: 400 }
  label: { family: ui, size: 13px, line: 18px, weight: 500, case: sentence }
  number: { family: ui, size: 15px, line: 22px, weight: 500, features: [tnum, lnum] }
  check: { family: ui, size: 13px, line: 18px, weight: 500 }
  hand: { family: hand, size: 20px, line: 28px, weight: 400 }
rounded:
  field: 10px     # buttons, inputs
  panel: 16px     # cards
  stamp: 3px
  pill: 999px     # status badges, step marks, small sheet marks and meters
  none: 0px
shadow:
  card: "0 1px 2px rgba(13, 18, 48, 0.05), 0 1px 3px rgba(13, 18, 48, 0.06)"
  raised: "0 4px 8px -2px rgba(13, 18, 48, 0.08), 0 12px 28px -8px rgba(13, 18, 48, 0.16)"
  hero: "0 24px 64px -16px rgba(0, 0, 0, 0.55)"
gradient:
  night: "linear-gradient(135deg, #0D1230 0%, #151C4B 62%, #24349F 130%)"
  glow: "radial-gradient(60% 80% at 80% 10%, rgba(47, 69, 216, 0.55) 0%, rgba(13, 18, 48, 0) 70%)"
spacing: { base: 4px, scale: [4, 8, 12, 16, 24, 32, 48, 64, 96] }
motion:
  ease: { duration: 160ms, easing: "cubic-bezier(.2,.7,.2,1)" }
  rise: { duration: 360ms, easing: "cubic-bezier(.2,.7,.2,1)", from: "translateY(10px)", to: "translateY(0)" }
  stamp: { duration: 160ms, easing: "cubic-bezier(.2,.9,.3,1.2)", from: "scale(1.18) rotate(-4deg)", to: "scale(1) rotate(-2deg)" }
  strike: { duration: 220ms, easing: "ease-out" }
  write: { duration: 380ms, easing: "steps(18, end)" }
  reduced-motion: "every animation and transition becomes an instant state change"
---

# Munim design system

This file is the single source of truth for how Munim looks and reads. A coding agent must treat it as a contract: tokens are exported to CSS custom properties by `scripts/build_tokens.py`, and `scripts/design_lint.py` fails the build when the UI drifts from it (section 12).

Version 2.0 replaces the flat paper-desk look of version 1 at the owner's request (1 November 2026 redesign): shadows, larger radii, gradients through tokens, Lucide icons, Inter for Latin text, a landing page, dashboard figures and subtle motion are now part of the system.

---

## 1. Visual theme

**Subject.** A small supplier, an accountant at a cyber cafe, or a shopkeeper's son, holding a pile of WhatsApp photos. They need to know three things: is each paper readable and consistent, what does the law say they are owed, and can they hand someone a file that proves it.

**Concept: a serious modern finance tool that still knows paper.** A deep navy shell, white cards on a cool canvas, and one blue accent. The challan book survives where it means something:

- Sheet colours encode paper type everywhere: invoice neutral, delivery challan `carbon-pink`, purchase order `carbon-yellow`.
- Anything corrected is written in `ballpoint` in the handwriting face, with the old value struck through in `red-pen`.
- A rubber stamp lands when the person confirms the values.

**Atmosphere words:** confident, clear, precise, calm. The amount owed is always the loudest thing on the screen.

---

## 2. Colour palette and roles

| Token | Hex | Role | Notes |
| --- | --- | --- | --- |
| `bond` | `#F5F6FA` | Page canvas | Text on it must be `ink`, `ink-2` or `muted`. |
| `sheet` | `#FFFFFF` | Cards, tables, forms | Controls sit only on `sheet`. |
| `ink` | `#111827` | Primary text | 16.4:1 on bond, 17.7:1 on sheet |
| `ink-2` | `#3B4354` | Secondary text | 9.2:1 on bond |
| `muted` | `#596173` | Captions, helper text | 5.7:1 on bond, 6.2:1 on sheet |
| `hairline` | `#E4E7EF` | Card edges and dividers | Never the only boundary of a control |
| `hairline-strong` | `#868FA3` | Input borders | 3.2:1 on sheet, 3.0:1 on bond (both clear the 3:1 minimum for UI edges) |
| `ballpoint-pressed` | `#2233AE` | Primary button hover and pressed | White text on it 9.8:1 |
| `ballpoint` | `#2F45D8` | Primary actions, links, selection, handwritten corrections | 7.1:1 on sheet |
| `ballpoint-wash` | `#EDF0FE` | Selected row, active tab | Text on it is `ink` |
| `red-pen` | `#C4281C` | Failed check, strike-through | 5.7:1 on sheet, 5.3:1 on bond, 5.0:1 on its own wash |
| `red-wash` | `#FDECEA` | Background of a failed row | Text on it is `ink` |
| `tick` | `#157347` | Passed check | 5.9:1 on sheet, 5.4:1 on bond, 5.2:1 on its own wash |
| `tick-wash` | `#E5F6ED` | Background of a passed row | Text on it is `ink` |
| `highlighter` | `#F2B92E` | A mark that says "check by hand" | A fill only, never text colour |
| `highlighter-wash` | `#FEF5DA` | Background of a needs-review row | Text on it is `ink` |
| `carbon-pink` | `#F6C9C1` | Delivery challan mark | Text on it is `ink` |
| `carbon-yellow` | `#F6DF8E` | Purchase order mark | Text on it is `ink` |
| `night` | `#0D1230` | Sidebar, hero, summary | Text on it must be `on-night`, `on-night-muted` or `sky` |
| `night-2` | `#1C2350` | Raised surface on night | Text on it must be `on-night`, `on-night-muted` or `sky` |
| `on-night` | `#F4F6FF` | Text on night | 17.0:1 on night |
| `on-night-muted` | `#B7BFDD` | Secondary text on night | 10.0:1 on night |
| `sky` | `#9DB0FF` | Links and marks on night | 8.8:1 on night |

**Rules**
1. Every colour in CSS, templates and SVG is one of these tokens, read through `var(--…)`. Raw hex outside `tokens.css` fails the design lint.
2. Status is never colour alone. Each status pairs colour with a word and a mark.
3. Status text (`red-pen`, `tick`) appears only on `sheet`, `bond` or its own wash, never on the carbon colours.
4. `scripts/check_contrast.py` tests every pair in this table and fails below 4.5:1 for text and 3:1 for UI edges.
5. No dark mode. The product prints on paper and the owner chose not to add one in the redesign. Do not add `prefers-color-scheme` rules.

---

## 3. Typography

- **Interface: Inter** (variable, Latin and Latin Extended, Rasmus Andersson, SIL OFL), with **Mukta** (Ek Type, SIL OFL) supplying Devanagari through the font stack. Inter has `tnum`; its figures are lining by default.
- **Hand: Kalam** (Indian Type Foundry, SIL OFL), for corrections only.
- All fonts are self-hosted WOFF2 files in `static/fonts/`, so the app works offline. Licences are in `static/fonts/LICENSES/`.

| Style | Size / line | Weight | Use |
| --- | --- | --- | --- |
| display-hero | 56 / 62 | 600 | Landing page headline only |
| display-amount | 44 / 50 | 600, tabular | The amount owed |
| display | 30 / 36 | 600 | Dashboard figures, verdict word |
| h1 | 28 / 36 | 600 | Page title |
| h2 | 19 / 28 | 600 | Card titles |
| h3 | 15 / 22 | 600 | Group titles |
| body | 15 / 24 | 400 | Running text |
| body-sm | 13 / 20 | 400 | Table detail, helper text |
| label | 13 / 18 | 500 | Form labels, table headers |
| number | 15 / 22 | 500, tabular | Amounts, dates, identifiers |
| hand | 20 / 28 | 400 | Corrections, never below 18px |

**Principles**
- Text inputs use 16px so mobile browsers do not zoom.
- Running text stays under 72 characters. Amounts are right-aligned in tables.
- Money format: Indian digit grouping, rupee sign, two decimals: `₹1,25,000.00`, from the tested formatter only.
- Devanagari gets +0.1 line-height and no letter-spacing (`:lang(hi)` resets tracking).
- Sentence case everywhere. No all-caps labels. The only capitals are in the stamp.
- Identifiers are copyable, show a group rhythm with adjacent spans and no spaces, never wrap mid-token and are never truncated.

---

## 4. Components

Macros live in `templates/components/macros.html`, icons in `templates/components/icons.html`, styles in `static/css/app.css`.

- **Button.** Primary (`ballpoint`, white text, `shadow-card`), secondary (`sheet`, `hairline-strong` edge), quiet (text only), danger (`red-pen` edge and text). `rounded.field`, at least 44px tall (40px allowed only for table-row actions on pointer devices). One primary per view. Labels name the action. Icons are optional and sit before the label; a forward arrow on a landing page action may follow it.
- **Card.** `sheet`, 1px `hairline`, `rounded.panel`, `shadow-card`. Padding 24px. Cards that are links may lift to `shadow-raised` on hover.
- **Stat card.** Label, `display` figure, optional helper line and a Lucide icon in a washed square. Every figure is computed from real case data. Never invent or round a figure for effect.
- **App shell.** 248px `night` sidebar on screens from 1024px: brand, navigation with icons, reader badge and language switch at the bottom. Below 1024px, a `night` top bar with a menu button opening the same navigation.
- **Badge.** `rounded.pill`, status wash, `ink` text, a mark at the left. Status badges only.
- **Verdict.** A badge with a mark and word: Passed, Doesn't match, Check by hand, Accepted. Never "Verified".
- **Inputs.** Label above, helper below in `muted`. `sheet`, `hairline-strong`, `rounded.field`, 44px tall, focus ring in `ballpoint`. Errors name the rule and what to do.
- **Dropzone.** A dashed `hairline-strong` area wrapping a real file input, focusable, with drag-over state in `ballpoint-wash`. After choosing, it shows the file name and size.
- **Document viewer.** Photo at its own aspect ratio, zoom by button and keyboard (`+`, `-`, `0`). Field boxes are SVG outlines with a white inner gap: solid `tick`, solid `red-pen`, dashed `ink` for Check by hand. Selecting a row selects its box and the other way round.
- **Claims list.** A real table with rows laid out as blocks: field and verdict on the first line, value and crop beneath, then actions. A non-passed row takes its status wash. Inputs keep a `sheet` background on washed rows.
- **Red-pen correction.** Failed value with its message, then a wavy `red-pen` strike draws across it (`motion.strike`), then the corrected value is revealed in the hand face (`motion.write`), then a `muted` line says what happened. If the re-read still fails, no handwriting appears and the row becomes Check by hand.
- **The stamp.** SVG with a double `ballpoint` border, rotated -2 degrees, real `<text>`: "CHECKED" and the date. It appears only when every blocking finding is passed or accepted and the person pressed "Confirm these values". It prints.
- **Summary band.** A `gradient-night` card at the top of the workbench holding the amount owed (`display-amount`), delivered, due, days late, interest and the link "How this is worked out". It states every clock case: input missing, no Bank Rate, provisional, not yet late, interest off, rate not confirmed. It never fills a default the person did not give.
- **Progress steps.** A numbered sequence on the workbench derived from real state: papers, values, terms, confirm. Numbers are allowed here because the content is a sequence.
- **Messages.** A wash background, a 4px left rule in the status colour and `ink` text. Toasts only for "Copied" and "Saved", auto-dismiss after 4 seconds, `aria-live="polite"`.

---

## 5. Pages

1. **Landing** (`/`): hero with the product claim and a drawn sample, how it works, what it checks, honest limits, footer with the legal notice. Sample figures are labelled as sample. No testimonials, logos or usage numbers.
2. **Cases** (`/cases`): dashboard figures, then the case table. Empty state with a next action.
3. **New case** (`/cases/new`): one focused form next to what to keep ready.
4. **Workbench** (`/cases/{id}`): header, summary band, steps, then papers rail, viewer and claims (three columns from 1280px), then terms, payments and delete.
5. **Evidence file** (`/cases/{id}/dossier`): screen preview and A4 print layout (18mm margins; parts: summary, evidence table, working, originals, draft notice; each original fits its own sheet). Print is plain: no shell, shadows or backgrounds.
6. **Discrepancy map, Samadhaan companion, Working:** case sub-pages with a back link in the header.
7. **Rules and sources, How well it reads, Settings, About:** single column of cards, 880px wide. A replay run is labelled as recorded responses, never as a live read.

**Responsive.** Test widths 360, 768, 1024, 1440. Touch targets at least 44px. No sideways page scroll; wide tables scroll inside their card. Hindi and English are equal citizens on every screen.

---

## 6. Elevation and motion

| Level | Treatment | Use |
| --- | --- | --- |
| 0 | `bond` | Canvas |
| 1 | `sheet`, `hairline`, `shadow-card` | Cards |
| 2 | `shadow-raised` | Hovered link cards, menus |
| 3 | `shadow-hero` | The landing illustration only |

Motion is subtle and purposeful: `motion.ease` for hover and focus, `motion.rise` once as a page's cards appear, htmx view transitions between pages, and the two product moments (red pen, stamp). Nothing animates on scroll. With `prefers-reduced-motion: reduce`, every animation and transition is instant.

---

## 7. Do's and Don'ts

**Do**
- Show the evidence next to every number: a crop of the box, the rule that checked it, the rule version.
- Say "Passed" or "Doesn't match", never "Verified" or "Correct".
- Keep corrections visible: original struck through, new value in ballpoint, reason beneath.
- Write sentence case, active voice, plain verbs.
- Give each empty state a next action and each error a cause and a fix.
- Keep demo data clearly synthetic.

**Don't**
- No glass, neon, mesh backgrounds or `backdrop-filter`. Gradients come from tokens only and appear only on `night` surfaces.
- No all-caps tracked eyebrow labels. No arrows typed into strings (draw a Lucide icon).
- No emoji, sparkle or magic-wand icons, robot imagery, "AI-powered", "magic", "supercharge", "seamless".
- No fake testimonials, logos, usage numbers, lorem ipsum or stock photographs.
- No raw `box-shadow` values, no radius above 16px except the pill token on badges.
- No scroll-triggered animation or parallax. No hard-coded strings.

---

## 8. Icons

Lucide 0.460.0 (ISC; the licence is `templates/components/LUCIDE-LICENSE.txt`), inlined as SVG through the `icon` macro with `currentColor`. Only icons the product uses are included. `strike` and `bracket-hand` are drawn for Munim because no Lucide icon carries their meaning. No icon font and no remote requests.

---

## 9. Content and voice

- Name things by what the user does: paper, case, evidence file, check, due date, amount owed. Not "documents processed", "pipeline", "inference", "agent".
- Refer to the model plainly: "Gemma read this paper". Never imply it is certain.
- Every number has a source: a box on a paper, a rule, or a setting.
- All strings live in `i18n/en.json` and `i18n/hi.json` and are listed in `docs/CONTENT.md`. There are no hard-coded strings in templates.
- Munim explains and calculates; it does not give legal advice. This sentence appears on the landing page, the evidence file, the rules page and the About page.

---

## 12. Design lint (enforced)

`scripts/design_lint.py` runs in CI and in `make check`. It scans templates, `static/css`, `static/js` (except `static/js/vendor/`) and i18n, and fails on:

1. Any hex colour outside `tokens.css`.
2. `box-shadow` other than a `var(--shadow-*)` token, `none` or a focus ring marked `/* focus-ring */`; `text-shadow`; `backdrop-filter`; blur and drop-shadow filters; raw gradient functions (use `var(--gradient-*)`).
3. `border-radius` above 16px, percentages and raw `9999px` (use `var(--radius-pill)`).
4. `text-transform: uppercase` outside `.stamp`, and `letter-spacing` above `0.02em`.
5. Emoji, arrows and separator characters in strings.
6. Fonts other than the declared families.
7. Devanagari without a Hindi `lang` attribute.
8. `IntersectionObserver` and scroll-driven animation.
9. Banned words: "AI-powered", "magic", "seamless", "supercharge", "unlock", "revolutionary", "lorem".

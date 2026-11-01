---
name: Munim
version: 3.0.0
format: DESIGN.md (Google Stitch format, sections as in VoltAgent/awesome-design-md)
description: >
  Design system for Munim, an open-source tool that turns phone photos of
  invoices, delivery challans and purchase orders into a checked evidence file
  for a small supplier chasing a late payment. Based on VoiceBox: a stark,
  flat, magazine-style system of black, white and one red, with huge headlines
  and borders doing the structural work. The working vocabulary of the paper
  trail stays where it carries meaning: carbon sheet colours, the red-pen
  correction and the rubber stamp.
colors:
  bond: "#FAFAFA"            # page canvas
  sheet: "#FAFAFA"           # cards, tables, forms, and white text on black or red
  ink: "#0A0A0A"             # primary text
  ink-2: "#525252"           # secondary text
  muted: "#525252"           # captions, helper text
  hairline: "#E5E5E5"        # card edges and dividers, never the only edge of a control
  hairline-strong: "#737373" # control edges
  ballpoint: "#0A0A0A"       # actions, links, selection, handwritten corrections
  ballpoint-pressed: "#DC2626" # primary button hover and pressed
  ballpoint-wash: "#E5E5E5"  # selected row, active tab
  accent: "#EF4444"          # VoiceBox red: rules and underlines only, never text
  red-pen: "#B91C1C"         # a check failed; strike-through of a wrong value
  red-wash: "#FEF2F2"
  tick: "#15803D"            # a check passed
  tick-wash: "#F0FDF4"
  highlighter: "#CA8A04"     # needs a human; a fill or edge, never text
  highlighter-wash: "#FEFCE8"
  carbon-pink: "#F6C9C1"     # delivery challan
  carbon-yellow: "#F6DF8E"   # purchase order
  night: "#0A0A0A"           # app sidebar, hero and summary surfaces
  night-2: "#262626"         # raised surface on night
  on-night: "#FAFAFA"        # text on night
  on-night-muted: "#D4D4D4"  # secondary text on night
  sky: "#FAFAFA"             # links and marks on night
typography:
  family-ui: "'Work Sans', Mukta, 'Noto Sans Devanagari', system-ui, sans-serif"
  family-display: "'Archivo Black', Mukta, 'Noto Sans Devanagari', Impact, 'Arial Black', sans-serif"
  family-mono: "'Space Mono', 'Courier New', monospace"
  family-hand: "Kalam, 'Noto Sans Devanagari', cursive"
  display-hero: { family: display, size: 56px, line: 60px, weight: 400, tracking: -0.03em }
  display-amount: { family: display, size: 44px, line: 48px, weight: 400, tracking: -0.02em }
  display: { family: display, size: 38px, line: 42px, weight: 400, tracking: -0.02em }
  h1: { family: display, size: 38px, line: 42px, weight: 400, tracking: -0.02em }
  h2: { family: display, size: 24px, line: 29px, weight: 400, tracking: -0.01em }
  h3: { family: ui, size: 16px, line: 24px, weight: 700 }
  body: { family: ui, size: 16px, line: 27px, weight: 400 }
  body-sm: { family: ui, size: 14px, line: 22px, weight: 400 }
  label: { family: ui, size: 12px, line: 16px, weight: 700, tracking: 0.06em, case: upper }
  number: { family: ui, size: 16px, line: 24px, weight: 500, features: [tnum, lnum] }
  check: { family: ui, size: 11px, line: 16px, weight: 700, tracking: 0.06em, case: upper }
  hand: { family: hand, size: 20px, line: 28px, weight: 400 }
rounded:
  field: 0px
  panel: 0px
  stamp: 0px
  pill: 0px
  none: 0px
shadow:
  card: none
  raised: none
  hero: none
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

Version 3.0 applies the VoiceBox system supplied by the owner (1 November 2026): flat surfaces, square corners, 2px borders, Archivo Black headlines, Work Sans text and capital labels. Lucide icons, the landing page, dashboard figures and subtle motion stay from version 2.

---

## 1. Visual theme

**Subject.** A small supplier, an accountant at a cyber cafe, or a shopkeeper's son, holding a pile of WhatsApp photos. They need to know three things: is each paper readable and consistent, what does the law say they are owed, and can they hand someone a file that proves it.

**Concept: a blunt editorial page that still knows paper.** A black shell, white pages, huge headlines and one red. The challan book survives where it means something, and these colours are the only additions to black, white and red, because they carry meaning:

- Sheet colours encode paper type everywhere: invoice neutral, delivery challan `carbon-pink`, purchase order `carbon-yellow`.
- Anything corrected is written in `ballpoint` in the handwriting face, with the old value struck through in `red-pen`.
- A rubber stamp lands when the person confirms the values.

**Atmosphere words:** bold, blunt, precise, unapologetic. The amount owed is always the loudest thing on the screen.

---

## 2. Colour palette and roles

VoiceBox's listed hex values are used wherever they meet the 4.5:1 text and 3:1 edge minimums below. Where one does not, the nearest passing shade replaces it: `#EF4444` text and white-on-red are 3.6:1, `#A3A3A3` text is 2.4:1, the `#D4D4D4` input edge is 1.4:1, and the status chip colours are 2.8 to 3.4:1.

| Token | Hex | Role | Notes |
| --- | --- | --- | --- |
| `bond` | `#FAFAFA` | Page canvas | Text on it must be `ink`, `ink-2` or `muted`. |
| `sheet` | `#FAFAFA` | Cards, tables, forms | Controls sit only on `sheet`. |
| `ink` | `#0A0A0A` | Primary text | 19.0:1 on bond, 19.0:1 on sheet |
| `ink-2` | `#525252` | Secondary text | 7.5:1 on bond |
| `muted` | `#525252` | Captions, helper text | 7.5:1 on bond, 7.5:1 on sheet |
| `hairline` | `#E5E5E5` | Card edges and dividers | Never the only boundary of a control |
| `hairline-strong` | `#737373` | Input borders | 4.5:1 on sheet, 4.5:1 on bond |
| `ballpoint-pressed` | `#DC2626` | Primary button hover and pressed | White text on it 4.6:1 |
| `ballpoint` | `#0A0A0A` | Primary actions, links, selection, handwritten corrections | 19.0:1 on sheet |
| `ballpoint-wash` | `#E5E5E5` | Selected row, active tab | Text on it is `ink` |
| `accent` | `#EF4444` | Rules and underlines on the active item | Never text; at most one per view |
| `red-pen` | `#B91C1C` | Failed check, strike-through | 6.2:1 on sheet, 6.2:1 on bond, 5.9:1 on its own wash |
| `red-wash` | `#FEF2F2` | Background of a failed row | Text on it is `ink` |
| `tick` | `#15803D` | Passed check | 4.8:1 on sheet, 4.8:1 on bond, 4.8:1 on its own wash |
| `tick-wash` | `#F0FDF4` | Background of a passed row | Text on it is `ink` |
| `highlighter` | `#CA8A04` | A mark that says "check by hand" | A fill or edge only, never text colour |
| `highlighter-wash` | `#FEFCE8` | Background of a needs-review row | Text on it is `ink` |
| `carbon-pink` | `#F6C9C1` | Delivery challan mark | Text on it is `ink` |
| `carbon-yellow` | `#F6DF8E` | Purchase order mark | Text on it is `ink` |
| `night` | `#0A0A0A` | Sidebar, hero, summary | Text on it must be `on-night`, `on-night-muted` or `sky` |
| `night-2` | `#262626` | Raised surface on night | Text on it must be `on-night`, `on-night-muted` or `sky` |
| `on-night` | `#FAFAFA` | Text on night | 19.0:1 on night |
| `on-night-muted` | `#D4D4D4` | Secondary text on night | 13.4:1 on night |
| `sky` | `#FAFAFA` | Links and marks on night | 19.0:1 on night |

**Rules**
1. Every colour in CSS, templates and SVG is one of these tokens, read through `var(--…)`. Raw hex outside `tokens.css` fails the design lint.
2. Status is never colour alone. Each status pairs colour with a word and a mark.
3. Status text (`red-pen`, `tick`) appears only on `sheet`, `bond` or its own wash, never on the carbon colours.
4. `scripts/check_contrast.py` tests every pair in this table and fails below 4.5:1 for text and 3:1 for UI edges.
5. No dark mode. The product prints on paper and the owner chose not to add one in the redesign. Do not add `prefers-color-scheme` rules.

---

## 3. Typography

- **Headlines: Archivo Black. Interface: Work Sans. Code: Space Mono** (all SIL OFL, Latin and Latin Extended). **Mukta** (Ek Type, SIL OFL) supplies Devanagari through the font stacks, at weight 600 for Hindi headlines because Mukta has no black weight. Archivo Black has no rupee sign, so Work Sans 900 draws it. Work Sans has `tnum`. Synthetic bold is off.
- **Hand: Kalam** (Indian Type Foundry, SIL OFL), for corrections only.
- All fonts are self-hosted WOFF2 files in `static/fonts/`, so the app works offline. Licences are in `static/fonts/LICENSES/`.

| Style | Size / line | Weight | Use |
| --- | --- | --- | --- |
| display-hero | 56 / 60 | Archivo Black | Landing page headline only |
| display-amount | 44 / 48 | Archivo Black | The amount owed |
| display | 38 / 42 | Archivo Black | Landing section titles, verdict word |
| h1 | 38 / 42 | Archivo Black | Page title |
| h2 | 24 / 29 | Archivo Black | Card titles, dashboard figures |
| h3 | 16 / 24 | Work Sans 700 | Group titles |
| body | 16 / 27 | Work Sans 400 | Running text |
| body-sm | 14 / 22 | Work Sans 400 | Table detail, helper text |
| label | 12 / 16 | Work Sans 700, capitals, 0.06em | Form labels, table headers |
| number | 16 / 24 | Work Sans 500, tabular | Amounts, dates, identifiers |
| check | 11 / 16 | Work Sans 700, capitals, 0.06em | Status badges |
| hand | 20 / 28 | Kalam 400 | Corrections, never below 18px |

**Principles**
- Text inputs use 16px so mobile browsers do not zoom.
- Running text stays under 72 characters. Amounts are right-aligned in tables.
- Money format: Indian digit grouping, rupee sign, two decimals: `₹1,25,000.00`, from the tested formatter only.
- Devanagari gets +0.1 line-height and no letter-spacing (`:lang(hi)` resets tracking).
- Strings are stored in sentence case. CSS sets capitals on buttons, badges, form labels, table headers and fact terms, and in the stamp. Choice labels, running text, identifiers and values never get capitals. Hindi resets tracking.
- Identifiers are copyable, show a group rhythm with adjacent spans and no spaces, never wrap mid-token and are never truncated.

---

## 4. Components

Macros live in `templates/components/macros.html`, icons in `templates/components/icons.html`, styles in `static/css/app.css`.

- **Button.** Primary (black fill, white text, 2px edge; hover `ballpoint-pressed`), secondary (transparent, 2px `ink` edge; hover inverts), quiet (text only; hover `red-pen`), danger (`red-pen` fill, white text). Work Sans 14px 700 in capitals. Square, at least 44px tall (40px allowed only for table-row actions on pointer devices). One primary per view. Labels name the action. Icons are optional and sit before the label; a forward arrow on a landing page action may follow it.
- **Card.** `sheet`, 2px `hairline`, square, no shadow. Padding 24px.
- **Stat card.** Label, `display` figure, optional helper line and a Lucide icon in a washed square. Every figure is computed from real case data. Never invent or round a figure for effect.
- **App shell.** 248px black sidebar; the active item has a 3px `accent` underline on screens from 1024px: brand, navigation with icons, reader badge and language switch at the bottom. Below 1024px, a `night` top bar with a menu button opening the same navigation.
- **Badge.** Square, status wash, 2px status edge, status-colour text (`ink` for Check by hand), a mark at the left. Status badges only.
- **Verdict.** A badge with a mark and word: Passed, Doesn't match, Check by hand, Accepted. Never "Verified".
- **Inputs.** Label above, helper below in `muted`. `sheet`, 2px `hairline-strong`, square, 44px tall, black focus ring. Errors name the rule and what to do.
- **Dropzone.** A dashed `hairline-strong` area wrapping a real file input, focusable, with drag-over state in `ballpoint-wash`. After choosing, it shows the file name and size.
- **Document viewer.** Photo at its own aspect ratio, zoom by button and keyboard (`+`, `-`, `0`). Field boxes are SVG outlines with a white inner gap: solid `tick`, solid `red-pen`, dashed `ink` for Check by hand. Selecting a row selects its box and the other way round.
- **Claims list.** A real table with rows laid out as blocks: field and verdict on the first line, value and crop beneath, then actions. A non-passed row takes its status wash. Inputs keep a `sheet` background on washed rows.
- **Red-pen correction.** Failed value with its message, then a wavy `red-pen` strike draws across it (`motion.strike`), then the corrected value is revealed in the hand face (`motion.write`), then a `muted` line says what happened. If the re-read still fails, no handwriting appears and the row becomes Check by hand.
- **The stamp.** SVG with a double `ballpoint` border, rotated -2 degrees, real `<text>`: "CHECKED" and the date. It appears only when every blocking finding is passed or accepted and the person pressed "Confirm these values". It prints.
- **Summary band.** A flat `night` card at the top of the workbench holding the amount owed (`display-amount`), delivered, due, days late, interest and the link "How this is worked out". It states every clock case: input missing, no Bank Rate, provisional, not yet late, interest off, rate not confirmed. It never fills a default the person did not give.
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

Everything is flat. Hierarchy comes from weight, scale and black-white contrast, never from elevation. The shadow tokens are `none`.

Motion is subtle and purposeful: `motion.ease` for hover and focus, `motion.rise` once as a page's cards appear, htmx view transitions between pages, and the two product moments (red pen, stamp). Nothing animates on scroll. With `prefers-reduced-motion: reduce`, every animation and transition is instant.

---

## 7. Do's and Don'ts

**Do**
- Show the evidence next to every number: a crop of the box, the rule that checked it, the rule version.
- Say "Passed" or "Doesn't match", never "Verified" or "Correct".
- Keep corrections visible: original struck through, new value in ballpoint, reason beneath.
- Write sentence case in strings, active voice, plain verbs.
- Give each empty state a next action and each error a cause and a fix.
- Keep demo data clearly synthetic.

**Don't**
- No glass, neon, gradients, textures or `backdrop-filter`.
- `accent` is a scalpel: at most one per view. `red-pen` is status, not decoration, and appears wherever a check failed.
- No arrows typed into strings (draw a Lucide icon).
- No emoji, sparkle or magic-wand icons, robot imagery, "AI-powered", "magic", "supercharge", "seamless".
- No fake testimonials, logos, usage numbers, lorem ipsum or stock photographs.
- No raw `box-shadow` values and no rounded corners.
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
3. `border-radius` above 0, percentages and raw `9999px`. Radius tokens are all 0.
4. `text-transform: uppercase` outside the stamp and label styles, and `letter-spacing` above `0.12em`.
5. Emoji, arrows and separator characters in strings.
6. Fonts other than the declared families.
7. Devanagari without a Hindi `lang` attribute.
8. `IntersectionObserver` and scroll-driven animation.
9. Banned words: "AI-powered", "magic", "seamless", "supercharge", "unlock", "revolutionary", "lorem".

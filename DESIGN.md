# DESIGN.md — Landing Page Prompts for Google Stitch

Working doc, not a spec for a finished export. Content language: **English** (matches the README and the global hackathon audience) — say the word and I'll translate later.

**Design direction: white background, one clear accent color, friendly and easy to read.** Simple and light reads as more approachable than a dark/technical theme — better for a landing page meant to be understood fast by people who aren't necessarily developers.

## How to use this in Stitch (read this before pasting anything)

1. Copy only the text inside the **Master prompt** code block (section 1 below) — not the headings, not the table, not this file's notes — and paste it as your **one and only** generation request in Stitch. It describes all 6 sections in order, as a single page.
2. Look at the result as a whole scroll, not section by section.
3. If one part needs a tweak, don't regenerate from scratch — send a short **follow-up message in that same Stitch thread** naming the section, e.g. *"In the hero section, make the button bigger."* Stitch edits that screen in place, keeping the rest untouched. Section 2 below gives you one ready-made follow-up per section if something drifts from the spec.
4. Only export/share with me once the whole scroll reads as one consistent page.

---

## 0. Color palette — white background, one accent, WCAG-checked

Light, clean, friendly — one background, one accent, nothing competing with it.

| Role | Color | Hex | Contrast on white | Use |
| --- | --- | --- | --- | --- |
| Background | white | `#FFFFFF` | — | page background, everywhere |
| Surface | soft gray | `#F6F7F9` | — | the trust-section band, the browser-mockup chrome — the only two places a fill other than white appears |
| Border | light gray | `#E3E5E8` | — | thin 1px borders/dividers only, never a fill |
| Text primary | near-black | `#16181D` | 17.9:1 (AAA) | headlines, body |
| Text muted | mid gray | `#5B5F66` | 6.6:1 (AA/AAA) | subheads, secondary text |
| **Accent** | **blue** | **`#1D4ED8`** | 6.3:1 (AA, incl. as white-on-blue button text) | primary button, the one highlighted phrase per headline, the one highlighted form field in the hero — nothing else |
| Accent hover | darker blue | `#1E40AF` | — | button hover/active state only |
| Success (rare) | green | `#15803D` | 5.1:1 | only where copy says "approved" |
| Blocked (rare) | red | `#B91C1C` | 6.1:1 | only where copy says "never" / "disabled" |

**Why this palette is "friendly and understandable" (not just pretty):**
- White background + near-black text is the highest-legibility, lowest-effort combination there is — no theme-recognition tax on the reader, works identically in bright rooms and on cheap monitors, and matches how the actual product (a form-filling tool for institutional portals) already looks: plain, official, no dark "hacker" aesthetic that would feel at odds with government/university users.
- One blue accent (`#1D4ED8`) instead of an unusual color: blue-as-primary-action is a convention every internet user already knows — "the blue thing is what I click." That's a real usability win (Nielsen's "match the real world / consistency & standards" heuristic), not just a safe choice.
- Every text/background pairing above is checked against WCAG AA (4.5:1 minimum for body text, 3:1 for large text) — the ratios are listed so Stitch (and you) can verify instead of assume. If Stitch renders a lighter shade than the hex given, that's why it may look like it fails — check it, don't eyeball it.
- Only 2 non-white fills exist (`#F6F7F9` surface, plus the accent on buttons) — this keeps the page calm and prevents it from turning into a multi-color dashboard, which is the opposite of "easy to understand."

Type: one sans-serif for everything (Inter, or Stitch's default geometric sans — something warm and rounded reads friendlier than a sharp grotesk), one monospace used only for a handful of technical tokens (numbers, a URL bar). Don't mix more than these two fonts.

**Global rule to repeat in every Stitch prompt:** *"White background, one visual focal point per section, generous whitespace, no more than one accent-colored element besides the button. No icon rows, no multi-badge rows, no stacked diagrams."*

---

## 0.5 UX/UI criteria (non-negotiable, check every screen against this)

These apply to what Stitch generates *and* to the final build — check both against this list, not just "does it look nice."

**Hierarchy & content**
- One primary action per screen, visually dominant (the blue button). Never two competing CTAs on the same screen.
- One headline per section doing the work — if the subhead repeats the headline's idea, cut the subhead.
- F-pattern / scannability: someone skimming only the headlines (Hero → "no API" → "browser is the API" → "never submits" → CTA) should get the whole pitch without reading body text.
- Plain language throughout — this targets non-developers too (evaluators, LatAm builders, institutional staff), so no unexplained jargon outside the "How it works" section, where the technical terms are the point.

**Consistency**
- One 8px spacing scale across every section (8/16/24/32/48/64/96) — no arbitrary padding values.
- One type scale (e.g. 56/40/24/18/16/14px) reused everywhere, never a one-off font size per section.
- The accent blue means one thing only ("active / call to action") — never reuse it for a decorative border or a random highlight, or it stops signaling anything.

**Accessibility**
- Contrast is pre-checked in the palette table above (all pairs pass WCAG AA); if Stitch substitutes a lighter or brighter shade of any color, re-check it against those ratios before accepting the screen.
- Every interactive element (button, link) needs a visible focus state and a hover state, not just a default state — ask Stitch for this explicitly if it's missing from the export.
- Buttons and links sized for a real tap target (≥44×44px effective area), not just a small text link.
- Images/icons that carry meaning need alt text when this becomes real HTML — flag any icon that *is* the only carrier of information (e.g. a status icon with no text label) so it gets a text equivalent.

**Responsive**
- Every section must have a stated mobile behavior (already noted per-section below: stacks vertically, single column). Verify Stitch actually produces a mobile variant, not just desktop.
- No fixed-width elements wider than a phone screen; side padding maintained at every breakpoint (never edge-to-edge text).

**Feedback & states**
- The one interactive visual (the highlighted form field in the Hero mockup) should read as a *state*, not decoration — if it were real, hovering/approving would visibly change it. Keep that logic in mind if this becomes an animated prototype later.
- Loading/empty/error states aren't needed for a static landing page, but note them now for the real product screens later (side panel idle vs. thinking vs. proposing vs. approved) — out of scope for this landing but don't let the landing imply states the product doesn't have.

**Performance / simplicity**
- No auto-playing video, no heavy background image — the "browser mockup" visual should be built from real DOM/CSS shapes wherever possible, not a large exported image, once this becomes code.

---

## 1. Master prompt — paste this one, as a single page

```
Design one complete landing page, single continuous scroll, 6 sections in this exact order, sharing one consistent light visual system throughout — not 6 separate screens, one page.

GLOBAL STYLE (apply to every section below):
- White background #FFFFFF everywhere except: a soft gray surface #F6F7F9 used only for the trust-section band and the browser-mockup chrome, and a light gray border #E3E5E8 for thin 1px dividers (never a fill). Text primary near-black #16181D, text muted #5B5F66. One accent color, blue #1D4ED8, used sparingly — only on primary buttons, the one highlighted headline phrase, and the one highlighted UI detail in the hero. Never use the accent as a background fill or a decorative border. White text on the blue button.
- One friendly, rounded sans-serif font throughout; one monospace font used only for small technical tokens (numbers, a URL bar, code-like labels).
- One consistent spacing rhythm and type scale reused across all 6 sections — headline size, subhead size, and body size should each look identical wherever they repeat.
- Clean and approachable: one visual focal point per section, generous whitespace, no icon rows, no multi-badge rows, no stacked diagrams, no card-grid clutter, no dark or "hacker" aesthetic.
- Every section stacks to a single column on mobile, side padding maintained, no fixed-width elements wider than a phone screen. Buttons and links sized for real tap targets (44px+). Visible hover and focus states on every button and link (e.g. a darker blue #1E40AF on hover).

SECTION 1 — Hero:
Centered, max-width ~800px, generous top padding. At the very top, a small wordmark line: "Wicket" in bold near-black, with one short muted line right under it in smaller text: "the counter window where paperwork gets done" — this explains the name immediately, since it's not a common word for every reader. Below that, the headline (large, bold, near-black): "The agent that works inside the tab you already have open." One muted subtext line: "Wicket reads and fills legacy forms with no API — with a human approving every action that changes anything." One solid blue button with white text: "Watch the demo." Below the text, a single browser-window mockup on a soft gray card (rounded top corners, three dots, a URL bar) with a plain form on the left and a slim docked side panel on the right — exactly one form field is highlighted with a thin blue outline, everything else is neutral gray/white/black text, no other color.

SECTION 2 — Problem → thesis:
Centered, max-width ~650px, tall vertical padding, white background, no visuals at all. One muted short line: "Government filing desks. University intranets. 15-year-old ERPs. No API, and never will be." Below it, a large bold centered statement in near-black with 3-4 words in accent blue: "When there is no API, the browser is the API."

SECTION 3 — How it works:
Centered heading: "A compact index, not the raw page." One muted subheading: "We never send the HTML to the model — we send a short list of the elements that matter." Below it, exactly 3 steps in a row (stack vertically on mobile), connected by thin blue arrows, no icons or cards — just a number (01/02/03, muted monospace), a short title, one line of description: "Index" (the page becomes a list of at most 150 elements, each with a stable reference), "Reason" (the agent proposes a value for each field, citing its reasoning), "Approve" (a person reviews and approves before anything is written).

SECTION 4 — What it does:
Centered heading: "One agent, three flows." Below it, 3 rows stacked vertically, separated by a thin light-gray 1px border, title on the left + one-line description on the right: "Assisted form filling" with a small blue "live" label (extracts data from a pasted email, maps it to the form on screen, proposes it field by field); "Table reading" with a small muted gray "later" label (answers questions about a case tray extracted from the page); "Pre-submission review" with a small muted gray "later" label (flags empty fields and inconsistencies before the system rejects them).

SECTION 5 — Trust principle:
A full-width rounded band with soft gray background #F6F7F9 and a thin border, no accent color in this section at all — calm and reassuring, not exciting. Centered: large bold near-black statement "The agent never submits." One muted line below: "It reads, it proposes, it writes fields after approval — but a person presses submit. The submit tool isn't disabled. It isn't implemented."

SECTION 6 — Closing / footer:
White background, centered heading: "See it fill a real form." One solid blue button with white text: "Watch the 2-minute demo." Below it, after a thin top border, one small centered muted monospace line: "Wicket — built in 4h15 for Agents, Everywhere, AI Tinkerers Lima · Sept 12 2026" and one row of 3 plain muted text links (underline on hover only, no icons): "GitHub" · "Architecture" · "Demo video."

Render this as one page top to bottom, section 1 flowing directly into section 2 into 3 into 4 into 5 into 6, with consistent vertical rhythm between them, on a white background throughout — not as isolated cards or disconnected screens, and not dark-themed.
```

---

## 2. Refinement prompts — only if one section drifts, sent as follow-ups in the same Stitch thread

Don't regenerate the whole page with these — send them as a chat follow-up on the page you already have, naming the section: *"In [section], do this: ..."*

**Rename to Wicket** (use this one now, on whatever Stitch already generated)
```
Rename the product everywhere on this page from "Ventana" to "Wicket." At the top of the hero section, above the existing headline, add a small wordmark: "Wicket" in bold near-black, with one short muted line right under it: "the counter window where paperwork gets done" — this explains the name since it isn't a common word for every reader. In the hero subtext, change "Ventana reads and fills..." to "Wicket reads and fills..." In the footer credit line, change "Ventana — built in 4h15..." to "Wicket — built in 4h15..." Don't change anything else on the page — same layout, same colors, same copy everywhere else.
```

**Hero**
```
In the hero section: keep the headline "The agent that works inside the tab you already have open." and the solid blue "Watch the demo" button with white text. Simplify the browser-window visual so only one form field is highlighted in blue — remove any other colored element, badge, or extra button in this section. Background must stay white.
```

**Problem → thesis**
```
In the problem/thesis section: keep it centered, single column, white background, no visuals. Make sure only the 3-4 word phrase "the browser is the API" is blue — the rest of the text stays near-black or muted gray. Remove any icon, card, or column layout if present.
```

**How it works**
```
In the "how it works" section: keep exactly 3 steps (Index, Reason, Approve) in a row connected by thin blue arrows on a white background. Remove icons or card backgrounds if Stitch added them — steps should be just a number, a title, and one line of text.
```

**What it does**
```
In the "what it does" section: keep the 3 flows as plain rows separated by a thin light-gray border, not cards, on white background. Only "Assisted form filling" gets the blue "live" label; the other two get a muted gray "later" label. Remove any icons or extra colors.
```

**Trust principle**
```
In the trust section: keep this section calm — no blue accent at all here, just the soft gray band, the border, and the two lines of text ("The agent never submits." + the explanation). Remove any icon or decorative element if present.
```

**Closing / footer**
```
In the closing section: keep the white background, one solid blue button ("Watch the 2-minute demo"), the small monospace credit line, and the 3 plain text links (GitHub, Architecture, Demo video). Remove any logo mark, extra columns, or tech-stack badges if Stitch added them — this should be the quietest section on the page.
```

---

## Assembly notes

- The whole landing is 6 sections in one page, white background throughout: Hero → Problem/Thesis → How it works → What it does → Trust → Closing.
- Bilingual (EN/ES) and "built with" tech credits were cut as standalone sections — happy to add either back as a small addition once we see the full page, rather than risk clutter again.
- I have **not** created any landing page files yet. That happens once you share the Stitch output.

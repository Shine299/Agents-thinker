---
name: Ventana System
colors:
  surface: '#f8f9ff'
  surface-dim: '#d7dae2'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f1f3fc'
  surface-container: '#ebeef6'
  surface-container-high: '#e5e8f0'
  surface-container-highest: '#dfe2eb'
  on-surface: '#181c22'
  on-surface-variant: '#434655'
  inverse-surface: '#2d3137'
  inverse-on-surface: '#eef1f9'
  outline: '#747686'
  outline-variant: '#c4c5d7'
  surface-tint: '#2151da'
  primary: '#0037b0'
  on-primary: '#ffffff'
  primary-container: '#1d4ed8'
  on-primary-container: '#cad3ff'
  inverse-primary: '#b7c4ff'
  secondary: '#5d5e64'
  on-secondary: '#ffffff'
  secondary-container: '#dfdfe6'
  on-secondary-container: '#616268'
  tertiary: '#7f2500'
  on-tertiary: '#ffffff'
  tertiary-container: '#a73400'
  on-tertiary-container: '#ffc9b7'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dce1ff'
  primary-fixed-dim: '#b7c4ff'
  on-primary-fixed: '#001551'
  on-primary-fixed-variant: '#0039b5'
  secondary-fixed: '#e2e2e9'
  secondary-fixed-dim: '#c6c6cd'
  on-secondary-fixed: '#1a1b21'
  on-secondary-fixed-variant: '#45474c'
  tertiary-fixed: '#ffdbcf'
  tertiary-fixed-dim: '#ffb59c'
  on-tertiary-fixed: '#390c00'
  on-tertiary-fixed-variant: '#832700'
  background: '#f8f9ff'
  on-background: '#181c22'
  surface-variant: '#dfe2eb'
typography:
  display:
    fontFamily: Plus Jakarta Sans
    fontSize: 56px
    fontWeight: '700'
    lineHeight: 64px
    letterSpacing: -0.03em
  display-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 40px
    fontWeight: '600'
    lineHeight: 48px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
    letterSpacing: -0.015em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.005em
  body-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  code-md:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
    letterSpacing: -0.01em
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.01em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 2rem
  gutter-mobile: 1rem
  margin: 3rem
  margin-mobile: 1.25rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
  space-2xl: 4rem
  space-3xl: 6rem
---

## Brand & Style

This design system delivers a calm, approachable, and disciplined aesthetic designed to instill trust instantly. It rejects loud marketing tropes, dark-mode technical tropes, and excessive visual noise in favor of luminous clarity, generous breathing room, and precise micro-details.

The emotional goal is immediate confidence and clarity. Built for discerning teams who evaluate software on its precision and refinement, the interface pairs open, light-flooded layouts with restrained, surgical applications of vivid royal blue. Typography combines a friendly, structural grotesque with monospace accents to ground technical authenticity without feeling dense or intimidating.

## Colors

The palette operates under absolute discipline, using a high-key light baseline to maximize readability and openness.

- **Canvas & Surfaces:** Primary canvas is `#FFFFFF`. A secondary neutral band `#F6F7F9` is reserved strictly for the trust/logo section and structural browser mockup chrome. It must not be scattered randomly as card fills.
- **Borders & Dividers:** Single-pixel hairline strokes rendered in `#E3E5E8` provide boundary clarity without heavy outlines.
- **Text & Content:** Headers and body text default to near-black `#16181D` for crisp contrast. Secondary descriptions, labels, and supporting metadata use `#5B5F66`.
- **Accent Rules:** Royal blue `#1D4ED8` (hovering to `#1E40AF`) is an intentional focal trigger. Its use is limited to primary calls-to-action, selective hero headline emphasis, and interactive focal points in product mockups (e.g., active input rings or active progress state).

## Typography

Typography establishes an airy, human feel paired with technical precision. 

- **Primary Typeface:** Plus Jakarta Sans provides clean geometric shapes with friendly, open apertures. Large titles feature tight tracking (`-0.02em` to `-0.03em`) to keep words unified, while body text maintains standard tracking for long-form comfort.
- **Monospace Accent:** JetBrains Mono is strictly used for functional signals: index indicators (`01`, `02`), live browser URL bars, badge pills, and system metrics. It balances the warm tone of Plus Jakarta Sans with engineering rigor.
- **Visual Weight:** Avoid excessive font weights. Reserve `700` purely for `display`, using `600` for mid-tier hierarchy and `400` for all running text.

## Layout & Spacing

Layouts follow a structured 12-column grid constrained to a maximum content width of 1200px, centering the visual flow while leaving wide, calm margins on wide screens.

- **Vertical Cadence:** Landing page sections must breathe. Section dividers and layout transitions rely on `space-3xl` (96px) on desktop and `space-2xl` (64px) on mobile. Micro-gaps between headers and their descriptive subtitles adhere to `space-sm` or `space-md`.
- **Breakpoints:**
  - **Desktop (≥ 1024px):** 12 columns, 32px gutters, outer padding starting at 48px.
  - **Tablet (768px – 1023px):** 8 columns, 24px gutters, outer padding at 32px.
  - **Mobile (< 768px):** 4 columns, 16px gutters, outer padding at 20px. Multi-column cards collapse to single-column stacks with `space-md` separation.

## Elevation & Depth

This design system deliberately eschews heavy drop shadows, dark glows, and layered glass blur. Depth is established through crisp structural containment:

- **Borders over Shadows:** Cards, panels, and mockups rely primarily on 1px `#E3E5E8` hairline borders against the `#FFFFFF` canvas.
- **Subtle Surface Lift:** When an element requires floating emphasis (such as an interactive dropdown, sticky navigation header, or elevated preview card), use a single featherlight ambient shadow: `0 4px 20px -2px rgba(22, 24, 29, 0.04), 0 2px 6px -1px rgba(22, 24, 29, 0.02)`.
- **Chrome Contrast:** Complex product previews use the `#F6F7F9` surface fill for the top browser/application toolbar, bounded by an interior border divider to create logical nesting without dimensional skew.

## Shapes

Corner radii balance geometric rigor with a welcoming, soft-touch product feel:

- **Standard Containers:** Cards, modal viewports, and primary mockup windows use `rounded-lg` (16px) to frame content softly.
- **Controls & Form Elements:** Buttons, text inputs, and navigation links use standard `rounded` (8px), maintaining clean alignment with tabular content.
- **Pills & Status Indicators:** Badges, category labels, and technical chips use continuous fully-rounded pill shapes (`9999px`) to immediately separate metadata from actionable interactive elements.

## Components

### Buttons
- **Primary:** Background `#1D4ED8`, text `#FFFFFF`, radius 8px, padding 10px 20px, font weight 600. Hover shifts background to `#1E40AF`. Active state slightly scales down (`scale(0.98)`).
- **Secondary / Outline:** Background `#FFFFFF`, border 1px solid `#E3E5E8`, text `#16181D`. Hover shifts border color to `#16181D` and background to `#F6F7F9`.

### Badges & Technical Chips
- Inline metadata chips employ `code-sm` font in JetBrains Mono.
- Background `#F6F7F9`, border 1px solid `#E3E5E8`, text `#5B5F66`, 4px 10px padding, fully rounded (`rounded-full`).

### Cards & Grid Containers
- Background `#FFFFFF`, 1px solid `#E3E5E8`, radius 16px, padding 32px.
- No default box shadow; hover states introduce the featherlight ambient shadow and shift border to a subtly darker gray `#D1D5DB`.

### Input Fields (Mockup & Real)
- Background `#FFFFFF`, border 1px solid `#E3E5E8`, text `#16181D`, radius 8px, padding 10px 14px.
- **Focal Active Input:** Border `#1D4ED8` with an ambient glow ring: `box-shadow: 0 0 0 3px rgba(29, 78, 216, 0.12)`.

### Mockup Chrome & Windows
- Upper tab/header bar rendered with `#F6F7F9` background, 44px height, separated by a bottom border of 1px solid `#E3E5E8`.
- Contains 3 window control dots (diameter 10px, soft grays `#E3E5E8` or muted tones) and a central simulated address pill featuring `code-sm` typography.

### Checkboxes & List Items
- Checkboxes: 18x18px box, border 1px solid `#E3E5E8`, radius 4px. When selected, solid `#1D4ED8` fill with an optically centered white check icon.
- Feature lists: Accompanied by circular 20px pill badges with a 1px border and a crisp `#1D4ED8` check glyph, offset from copy with `space-md`.
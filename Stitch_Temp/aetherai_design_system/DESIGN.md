---
name: AetherAI Design System
colors:
  surface: '#f8f9ff'
  surface-dim: '#cbdbf5'
  surface-bright: '#f8f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#eff4ff'
  surface-container: '#e5eeff'
  surface-container-high: '#dce9ff'
  surface-container-highest: '#d3e4fe'
  on-surface: '#0b1c30'
  on-surface-variant: '#3d4947'
  inverse-surface: '#213145'
  inverse-on-surface: '#eaf1ff'
  outline: '#6d7a77'
  outline-variant: '#bcc9c6'
  surface-tint: '#006a61'
  primary: '#00685f'
  on-primary: '#ffffff'
  primary-container: '#008378'
  on-primary-container: '#f4fffc'
  inverse-primary: '#6bd8cb'
  secondary: '#545f73'
  on-secondary: '#ffffff'
  secondary-container: '#d5e0f8'
  on-secondary-container: '#586377'
  tertiary: '#924628'
  on-tertiary: '#ffffff'
  tertiary-container: '#b05e3d'
  on-tertiary-container: '#fffbff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#89f5e7'
  primary-fixed-dim: '#6bd8cb'
  on-primary-fixed: '#00201d'
  on-primary-fixed-variant: '#005049'
  secondary-fixed: '#d8e3fb'
  secondary-fixed-dim: '#bcc7de'
  on-secondary-fixed: '#111c2d'
  on-secondary-fixed-variant: '#3c475a'
  tertiary-fixed: '#ffdbce'
  tertiary-fixed-dim: '#ffb59a'
  on-tertiary-fixed: '#370e00'
  on-tertiary-fixed-variant: '#773215'
  background: '#f8f9ff'
  on-background: '#0b1c30'
  surface-variant: '#d3e4fe'
typography:
  display:
    fontFamily: Inter
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.02em
  mono-sm:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  container-max: 1440px
  gutter: 20px
---

## Brand & Style

The brand personality is clinical, authoritative, and hyper-efficient. It is designed for high-stakes pharmaceutical environments where speed and accuracy are paramount. The aesthetic follows a **Corporate / Modern** style with a focus on systematic clarity and technical precision. 

The visual language communicates reliability through a rigorous grid, generous white space to reduce cognitive load, and a strict information hierarchy. The interface avoids decorative elements, ensuring that every visual cue—from a border-radius to a color shift—serves a specific functional purpose in the triage workflow.

## Colors

The palette is rooted in medical professionalism. The **Primary Teal (#0D9488)** is used for primary actions and brand presence, while **Deep Blue (#1E293B)** provides a grounded, sophisticated secondary tone for navigation and headers.

### Functional Palette
- **Primary:** Medical Teal for growth and core interaction.
- **Secondary:** Deep Slate Blue for structure and grounding.
- **Backgrounds:** Slate 50 (#F8FAFC) for canvas depth and White (#FFFFFF) for component surfaces.
- **Text:** Slate 900 (#0F172A) for maximum legibility in body content and Slate 600 for metadata.

### Traffic Light Triage (Semantic)
A dedicated semantic system is used for patient and medication status:
- **Emerald 500:** Low risk / Routine.
- **Amber 500:** Medium risk / Review required.
- **Crimson 600:** High risk / Immediate intervention.

## Typography

This design system utilizes **Inter** for all UI elements to ensure maximum legibility and a neutral, systematic tone. For technical data—such as prescription IDs or dosage calculations—a secondary monospaced font (JetBrains Mono) is permitted for precision.

- **Scale:** High contrast between headlines and body text to allow for quick scanning of patient charts.
- **Hierarchy:** Use Semibold (600) for interactive elements and Medium (500) for labels. 
- **Mobile:** Headlines larger than 24px should scale down by 15% on mobile viewports to maintain density.

## Layout & Spacing

The layout utilizes a **fixed-fluid hybrid grid**. The main navigation is a fixed sidebar (240px), while the content area is a fluid 12-column grid.

- **Grid:** 12 columns for desktop, 8 for tablet, and 4 for mobile.
- **Rhythm:** An 8px linear scale (4, 8, 16, 24, 32, 48, 64) governs all padding and margins. 
- **Density:** High density is preferred for data-heavy triage views. Use `md` (16px) for standard gaps and `sm` (8px) for related grouping within cards.

## Elevation & Depth

To maintain a "clinical" feel, depth is achieved through **low-contrast outlines** rather than heavy shadows. 

- **Level 0 (Canvas):** Slate 50 background.
- **Level 1 (Cards/Panels):** White surface with a 1px border in Slate 200 (#E2E8F0).
- **Level 2 (Active/Modals):** White surface with a subtle 1px border and an extra-diffused 8% opacity shadow (0 4px 12px) to suggest focus.
- **Backdrop:** A 4px blur is applied to overlays to keep the context of the pharmacy dashboard visible while focusing on specific patient data.

## Shapes

The design system uses a **Soft (1)** shape language. The subtle rounding (4px - 12px) softens the clinical coldness without sacrificing the professional, structured feel.

- **Components (Buttons, Inputs):** 4px (0.25rem).
- **Containers (Cards, Modals):** 8px (0.5rem).
- **Triage Badges:** 12px (0.75rem) or fully rounded pill-shape for quick identification.

## Components

Components follow the **shadcn/ui** structural patterns, emphasizing accessibility and keyboard navigation.

### Buttons & Controls
- **Primary:** Filled Medical Teal with white text.
- **Secondary:** Outlined Slate 200 with Slate 900 text.
- **Destructive:** Crimson 600 background for critical triage actions.

### Triage Alerts
- Use the **Alert** component for system-wide notifications. 
- High-priority triage items must use a left-border accent (4px) in the corresponding Traffic Light color (Emerald/Amber/Crimson) to ensure status is visible at a glance.

### Data Cards
- Cards feature a Slate 200 border and no shadow. 
- Group related patient metrics using `mono-sm` typography for precise readability of measurements (e.g., mg/dL).

### Input Fields
- Inputs must have clear, persistent labels and high-contrast focus rings in Medical Teal. 
- Error states utilize Crimson 600 text and borders.
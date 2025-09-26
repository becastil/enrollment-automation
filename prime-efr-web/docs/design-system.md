# Design System Overview

The Prime EFR web client uses a token-driven design system. Tokens are defined once and consumed via semantic Tailwind classes that resolve to CSS variables. This document outlines the categories, naming, and usage patterns.

## Token Source of Truth

- File: `client/src/theme/designTokens.ts`
- Light/dark palettes extend a shared base covering colors, spacing, typography, radii, shadows, and z-index.
- Themes are applied at runtime by `client/src/theme/ThemeProvider.tsx`, which sets CSS variables on `document.documentElement` and toggles the `data-theme="light|dark"` attribute.

## Naming Conventions

| Category    | Prefix Example        | Notes |
|-------------|-----------------------|-------|
| Colors      | `--color-surface`     | Semantic names (`surface`, `text-muted`, `primary-soft`, etc.). 8 categorical chart colors are exposed as `--color-chart-categorical-N`. |
| Spacing     | `--space-md`          | Scale: `2xs`, `xs`, `sm`, `md`, `lg`, `xl`, `2xl`. Used via Tailwind classes like `px-md` or `space-y-sm`. |
| Radii       | `--radius-lg`         | Matches Tailwind keys (`rounded-lg`, etc.). |
| Typography  | `--font-size-lg`      | Includes family (`sans`, `mono`), size, line-height, and weight tokens. |
| Shadows     | `--shadow-md`         | Applied through Tailwind `shadow`, `shadow-md`, etc. |
| Z-Index     | `--z-index-modal`     | Values for UI layers (`dropdown`, `overlay`, `popover`, `toast`). |

## Tailwind Integration

- `tailwind.config.js` maps semantic keys to the tokens (e.g., `bg-surface`, `text-text-muted`, `border-border`).
- Default numeric spacing utilities are replaced by token shorthands (`p-md`, `px-xs`, `gap-xl`).
- Alerts, buttons, cards, and table states use `primary`, `success`, `warning`, and `danger` token families.

## Theming Helpers

- `useTheme()` hook exposes `{ theme, setTheme, toggleTheme }` for components.
- `ThemeProvider` persists the user’s choice in `localStorage` and falls back to `prefers-color-scheme`.
- Charts read palette tokens via `getChartPalette()` in `client/src/utils/theme.ts`.

## Extending Tokens

1. Add the new value to `designTokens.ts` (base or theme-specific section).
2. Expose the variable to Tailwind by updating `tailwind.config.js` (e.g., new color or spacing key).
3. Consume via Tailwind utilities or `useTheme` helpers—never hard-code literal values in components.

Following this workflow keeps light/dark modes and custom themes in sync without touching individual components.

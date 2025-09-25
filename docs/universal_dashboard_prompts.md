# Universal Dashboard Prompts

**Tip:** Work within the existing codebase and adapt solutions to the current `[stack]`, `[chart_lib]`, `[router]`, and `[test_framework]`. If a feature already exists, consolidate and standardize it. Provide any necessary adapters and brief docs in `README.md`.

1. **Design Tokens & Theming (Light/Dark)**
   - **Prompt:** Create a centralized design-token system (colors, spacing, typography, radii, shadows, z-index) exposed as CSS variables and a theme object. Implement light/dark modes with a single source of truth.
   - **Acceptance criteria:**
     * Tokens live in one module; components consume variables only (no hard-coded hex).
     * `data-theme="light|dark"` toggles update all components without layout shift.
     * Token names are semantic (e.g., `--color-surface`) and documented.

2. **Responsive Grid Layout & Breakpoints**
   - **Prompt:** Refactor the dashboard layout to a CSS Grid–based system with named areas (sidebar, header, filters, content). Define mobile, tablet, desktop breakpoints.
   - **Acceptance criteria:**
     * Sidebar collapses to an icon rail on small screens.
     * Charts/tables reflow into a single column on mobile.
     * No horizontal scroll at any breakpoint.

3. **Nav & Breadcrumbs with Current View Highlight**
   - **Prompt:** Implement a left navigation + top breadcrumbs. Persist the expanded/collapsed nav state.
   - **Acceptance criteria:**
     * Active route is visually distinguished and accessible via ARIA.
     * Breadcrumbs reflect deep filters where applicable (e.g., “Sales › Q3 › West”).
     * Keyboard navigation works (arrow keys, Enter, Esc).

4. **Loading, Empty, and Error States (Charts & Tables)**
   - **Prompt:** Add consistent skeleton loaders and friendly empty/error states for all widgets. Include a Retry action.
   - **Acceptance criteria:**
     * Shared `<AsyncState>` wrapper standardizes UI.
     * Empty states show why (no data vs. filter excluded) and a next action.
     * Errors are logged and redacted of sensitive data.

5. **Global Filter Bar with URL Sync**
   - **Prompt:** Build a global filter bar (date range presets, search, multi-select tags) that syncs to the URL query string and restores on page load.
   - **Acceptance criteria:**
     * Debounced inputs (250–400ms) to avoid thrash.
     * “Clear all” resets filters and URL.
     * Deep links reproduce the same state on reload/share.

6. **Saved Views (Named, Default, Shareable)**
   - **Prompt:** Enable users to save the current state (filters, sorting, visible columns, chart settings) as named views.
   - **Acceptance criteria:**
     * Save, rename, set default, delete.
     * Shareable link restores the exact state.
     * Server or local persistence behind an abstraction.

7. **Table Enhancements: Sticky, Resize, Reorder, Pin**
   - **Prompt:** Upgrade the main table with sticky header/first column, column resize, drag-to-reorder, and pin left/right.
   - **Acceptance criteria:**
     * Preferences persist per user.
     * Works with virtualized rows (10k+).
     * Accessible resize handles with keyboard support.

8. **Column-Level Filters & Quick Chips**
   - **Prompt:** Add per-column filters (text, numeric range, date range, enum multi-select) with “active filter” chips above the table.
   - **Acceptance criteria:**
     * Clear individual filters via chip “x”.
     * Server/client mode supported via adapter.
     * Filter UI never blocks scrolling.

9. **Multi-Column Sort with Reset**
   - **Prompt:** Implement shift-click multi-column sorting with stable sort and a one-click “Reset sorting.”
   - **Acceptance criteria:**
     * Sort indicators show priority (1, 2, 3).
     * Persist in URL/state.
     * Matches server sort when available.

10. **Drill-Down & Cross-Filtering**
    - **Prompt:** Enable click on chart elements or KPI tiles to apply contextual filters (“click to drill”), with a breadcrumb to step back.
    - **Acceptance criteria:**
      * Visual affordance for interactive elements.
      * Drill states are reflected in URL.
      * “Back” crumb restores previous state without re-fetch.

11. **Chart Tooltips, Legends & Formatting**
    - **Prompt:** Standardize tooltip and legend behavior across all charts: number formatting, date formatting, units, and percent of total.
    - **Acceptance criteria:**
      * One shared formatter module (currency, percent, compact).
      * Legends support toggle to show/hide series.
      * Tooltips remain readable on small screens.

12. **Export Center (CSV, PNG/SVG, PDF)**
    - **Prompt:** Add an Export menu per widget and for the whole page (underlying data as CSV; charts as PNG/SVG; print-to-PDF stylesheet).
    - **Acceptance criteria:**
      * File naming: `dashboard-name_YYYY-MM-DD_hhmm`.
      * 2× pixel ratio for raster exports.
      * Disabled for unauthorized roles.

13. **Time-Series Zoom/Pan & Range Selector**
    - **Prompt:** For all time-series charts, add drag-to-zoom, pan, and quick range presets (7D, 30D, QTD, YTD, 1Y).
    - **Acceptance criteria:**
      * Keyboard accessible zoom reset.
      * Timezone-aware rendering; consistent tick formatting.
      * Brush/mini-map on desktop; simple presets on mobile.

14. **KPI Tiles with Sparklines & Deltas**
    - **Prompt:** Create standardized KPI tiles showing current value, delta vs. previous period, and a sparkline. Threshold colors are semantically named.
    - **Acceptance criteria:**
      * Up/down arrows with accessible text (“+4.2% vs last week”).
      * Graceful handling of missing prior data.
      * Tiles align in a responsive row.

15. **Annotations & Notes on Charts**
    - **Prompt:** Allow users to add dated annotations (text markers) to charts (e.g., “Campaign launch”).
    - **Acceptance criteria:**
      * Hover shows note; click to edit/delete.
      * Persisted per dataset/series.
      * Toggle to show/hide all annotations.

16. **Accessibility Pass (A11y)**
    - **Prompt:** Perform an accessibility pass for the dashboard: landmarks, ARIA labels, focus order, and skip-to-content.
    - **Acceptance criteria:**
      * Meets WCAG AA contrast.
      * Keyboard-only users can operate filters, charts, and tables.
      * Screen reader announces changes (live regions where needed).

17. **Internationalization & Localization**
    - **Prompt:** Introduce i18n with message catalogs and locale-aware number/date formats. Support RTL layout.
    - **Acceptance criteria:**
      * Language switcher persists selection.
      * No truncated labels post-translation.
      * All dates/numbers respect locale.

18. **Performance: Virtualization & Code-Split**
    - **Prompt:** Optimize rendering: row virtualization for large tables, memoization for heavy charts, and route-level code splitting.
    - **Acceptance criteria:**
      * Time-to-interactive and interaction latency targets documented and met.
      * No layout thrash during rapid filter changes.
      * Lighthouse performance score improved and recorded.

19. **Data Freshness & Auto-Refresh**
    - **Prompt:** Add a “Last updated” indicator with manual refresh and optional auto-refresh intervals. Detect offline/online states.
    - **Acceptance criteria:**
      * Auto-refresh respects active edits (no UI yank).
      * Tooltip shows data timestamp and source.
      * Offline banner with retry logic.

20. **Print/PDF Styles & Page Breaks**
    - **Prompt:** Create print styles that remove chrome, optimize spacing, and insert page breaks between sections.
    - **Acceptance criteria:**
      * Charts/tables fit on pages without clipping.
      * Optional “Confidential” watermark toggle.
      * Print preview matches exported PDF.

21. **Guided Tour & Contextual Help**
    - **Prompt:** Add a first-run guided tour and inline help icons for complex controls.
    - **Acceptance criteria:**
      * Tour is dismissible and re-launchable.
      * Steps are focus-trapped and accessible.
      * Short “What’s new” modal for recent releases.

22. **User Preferences (Density, Theme, Date Preset)**
    - **Prompt:** Persist user UI preferences: table density (compact/cozy), theme, default date range, number format (e.g., “1,234.56” vs “1 234,56”).
    - **Acceptance criteria:**
      * Stored via a preferences service (local or server).
      * Immediate application without reload.
      * Export respects number format preference.

23. **Role-Based Access Control (RBAC)**
    - **Prompt:** Gate actions (export, edit annotations, admin settings) behind roles/permissions.
    - **Acceptance criteria:**
      * UI hides or disables restricted controls.
      * Server guards validated; no client-only security.
      * Reusable `can(permission)` helper.

24. **Audit Trail (Filters, Exports, Views)**
    - **Prompt:** Instrument an audit trail for key actions: filter changes, exports, saved view events.
    - **Acceptance criteria:**
      * Standard event schema with timestamps and user id.
      * Can be toggled off in dev/test.
      * Minimal PII; documented retention policy.

25. **Quality Gates: Unit & E2E Tests**
    - **Prompt:** Add tests for core flows: filtering, pagination, sorting, exporting, and theme switching. Integrate into CI.
    - **Acceptance criteria:**
      * Deterministic fixtures for charts/tables.
      * Smoke test suite runs under 5 minutes.
      * Coverage thresholds enforced for critical modules.

26. **Error Boundaries & Telemetry**
    - **Prompt:** Wrap pages/widgets with error boundaries and send errors + performance metrics to a telemetry sink (pluggable).
    - **Acceptance criteria:**
      * User-friendly fallback UIs with “Try again.”
      * Redaction ensures no raw data in logs.
      * Dashboard of key error/perf metrics exists.

27. **Unified Formatters for Data Display**
    - **Prompt:** Centralize formatting for currency, percent, large numbers (K/M/B), and durations in one module.
    - **Acceptance criteria:**
      * Single import used across charts/tables/tooltips.
      * Locale-aware and unit-aware.
      * Snapshot tests for edge cases (very small/large values).

28. **Color System: Accessible & Color-Blind Safe**
    - **Prompt:** Define categorical and sequential palettes that meet contrast guidelines and are color-blind safe.
    - **Acceptance criteria:**
      * Provide at least 8 categorical colors + 3 sequential ramps.
      * Works in both light/dark themes.
      * Legend and tooltip examples verified.

29. **Shareable, Bookmarkable URLs (State Encoding)**
    - **Prompt:** Encode dashboard state (filters, sorts, visible columns, chart toggles) in the URL with a compact serializer.
    - **Acceptance criteria:**
      * Robust to long states (hash-based or compressed).
      * Back/forward navigation restores state accurately.
      * Unknown params are ignored safely.

30. **Mobile UX & Touch Gestures**
    - **Prompt:** Optimize the dashboard for small screens: bottom-sheet filters, larger tap targets, sticky actions, and swipe-friendly tables.
    - **Acceptance criteria:**
      * Tables support horizontal scroll with visual cue and column snap.
      * Filters open in a modal sheet with apply/reset.
      * All controls meet minimum touch target size.

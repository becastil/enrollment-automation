export type ThemeName = 'light' | 'dark';

type TokenDictionary = Record<string, string>;

type DesignTokenRegistry = {
  spacing: TokenDictionary;
  radii: TokenDictionary;
  typography: {
    fontFamily: TokenDictionary;
    fontSize: TokenDictionary;
    lineHeight: TokenDictionary;
    fontWeight: TokenDictionary;
  };
  shadows: TokenDictionary;
  zIndex: TokenDictionary;
};

type ThemeTokens = {
  colors: TokenDictionary;
};

const baseTokens: DesignTokenRegistry = {
  spacing: {
    '2xs': '0.25rem',
    xs: '0.5rem',
    sm: '0.75rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
    '2xl': '3rem',
  },
  radii: {
    sm: '0.375rem',
    md: '0.5rem',
    lg: '0.75rem',
    xl: '1rem',
    full: '9999px',
  },
  typography: {
    fontFamily: {
      sans: '"Inter", "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif',
      mono: '"Fira Code", "SFMono-Regular", Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace',
    },
    fontSize: {
      xs: '0.75rem',
      sm: '0.875rem',
      base: '1rem',
      lg: '1.125rem',
      xl: '1.25rem',
      '2xl': '1.5rem',
      '3xl': '1.875rem',
    },
    lineHeight: {
      xs: '1rem',
      sm: '1.25rem',
      base: '1.5rem',
      lg: '1.75rem',
      xl: '1.75rem',
      '2xl': '2rem',
      '3xl': '2.25rem',
    },
    fontWeight: {
      regular: '400',
      medium: '500',
      semibold: '600',
      bold: '700',
    },
  },
  shadows: {
    sm: '0 1px 2px rgba(16, 24, 40, 0.08)',
    md: '0 4px 8px rgba(16, 24, 40, 0.1)',
    lg: '0 12px 24px rgba(16, 24, 40, 0.12)',
  },
  zIndex: {
    base: '1',
    dropdown: '1000',
    overlay: '1200',
    modal: '1400',
    popover: '1500',
    toast: '1600',
  },
};

const themePalettes: Record<ThemeName, ThemeTokens> = {
  light: {
    colors: {
      surface: '#ffffff',
      'surface-subtle': '#f8fafc',
      'surface-raised': '#ffffff',
      'surface-inverse': '#111827',
      border: '#e2e8f0',
      'border-strong': '#cbd5f5',
      text: '#0f172a',
      'text-muted': '#475569',
      'text-inverse': '#f8fafc',
      primary: '#2563eb',
      'primary-strong': '#1d4ed8',
      'primary-soft': '#dbeafe',
      success: '#16a34a',
      warning: '#f97316',
      danger: '#dc2626',
      'danger-soft': '#fee2e2',
      'warning-soft': '#fef3c7',
      'success-soft': '#dcfce7',
      'chart-categorical-1': '#2563eb',
      'chart-categorical-2': '#7c3aed',
      'chart-categorical-3': '#059669',
      'chart-categorical-4': '#ea580c',
      'chart-categorical-5': '#db2777',
      'chart-categorical-6': '#0ea5e9',
      'chart-categorical-7': '#6d28d9',
      'chart-categorical-8': '#047857',
      overlay: 'rgba(15, 23, 42, 0.55)',
    },
  },
  dark: {
    colors: {
      surface: '#111827',
      'surface-subtle': '#0b1120',
      'surface-raised': '#1f2937',
      'surface-inverse': '#f8fafc',
      border: '#1e293b',
      'border-strong': '#334155',
      text: '#e2e8f0',
      'text-muted': '#94a3b8',
      'text-inverse': '#0f172a',
      primary: '#60a5fa',
      'primary-strong': '#3b82f6',
      'primary-soft': 'rgba(96, 165, 250, 0.15)',
      success: '#4ade80',
      warning: '#fb923c',
      danger: '#f87171',
      'danger-soft': 'rgba(248, 113, 113, 0.18)',
      'warning-soft': 'rgba(251, 146, 60, 0.18)',
      'success-soft': 'rgba(74, 222, 128, 0.18)',
      'chart-categorical-1': '#60a5fa',
      'chart-categorical-2': '#c4b5fd',
      'chart-categorical-3': '#34d399',
      'chart-categorical-4': '#fb7185',
      'chart-categorical-5': '#fbbf24',
      'chart-categorical-6': '#38bdf8',
      'chart-categorical-7': '#a855f7',
      'chart-categorical-8': '#22d3ee',
      overlay: 'rgba(15, 23, 42, 0.75)',
    },
  },
};

const tokenNamespaceMap: Record<string, string> = {
  spacing: 'space',
  radii: 'radius',
  fontFamily: 'font-family',
  fontSize: 'font-size',
  lineHeight: 'line-height',
  fontWeight: 'font-weight',
  shadows: 'shadow',
  zIndex: 'z-index',
  colors: 'color',
};

type FlattenedTokens = Record<string, string>;

const flattenBaseTokens = (): FlattenedTokens => {
  const entries: [string, string][] = [];

  Object.entries(baseTokens.spacing).forEach(([key, value]) => {
    entries.push([`--${tokenNamespaceMap.spacing}-${key}`, value]);
  });

  Object.entries(baseTokens.radii).forEach(([key, value]) => {
    entries.push([`--${tokenNamespaceMap.radii}-${key}`, value]);
  });

  Object.entries(baseTokens.typography.fontFamily).forEach(([key, value]) => {
    entries.push([`--${tokenNamespaceMap.fontFamily}-${key}`, value]);
  });

  Object.entries(baseTokens.typography.fontSize).forEach(([key, value]) => {
    entries.push([`--${tokenNamespaceMap.fontSize}-${key}`, value]);
  });

  Object.entries(baseTokens.typography.lineHeight).forEach(([key, value]) => {
    entries.push([`--${tokenNamespaceMap.lineHeight}-${key}`, value]);
  });

  Object.entries(baseTokens.typography.fontWeight).forEach(([key, value]) => {
    entries.push([`--${tokenNamespaceMap.fontWeight}-${key}`, value]);
  });

  Object.entries(baseTokens.shadows).forEach(([key, value]) => {
    entries.push([`--${tokenNamespaceMap.shadows}-${key}`, value]);
  });

  Object.entries(baseTokens.zIndex).forEach(([key, value]) => {
    entries.push([`--${tokenNamespaceMap.zIndex}-${key}`, value]);
  });

  return Object.fromEntries(entries);
};

const baseCssVariables = flattenBaseTokens();

export const getThemeVariableMap = (themeName: ThemeName): FlattenedTokens => {
  const palette = themePalettes[themeName];

  const colorEntries = Object.entries(palette.colors).map(([key, value]) => [
    `--${tokenNamespaceMap.colors}-${key}`,
    value,
  ] as [string, string]);

  return {
    ...baseCssVariables,
    ...Object.fromEntries(colorEntries),
  };
};

export const applyTheme = (themeName: ThemeName): void => {
  if (typeof document === 'undefined') return;
  const root = document.documentElement;
  const variables = getThemeVariableMap(themeName);

  root.setAttribute('data-theme', themeName);

  Object.entries(variables).forEach(([name, value]) => {
    root.style.setProperty(name, value);
  });
};

export const designTokens = {
  base: baseTokens,
  themes: themePalettes,
};

export const AVAILABLE_THEMES: ThemeName[] = ['light', 'dark'];

export type ThemeVariableEntry = {
  name: string;
  value: string;
};

export const listThemeVariables = (themeName: ThemeName): ThemeVariableEntry[] => {
  const variables = getThemeVariableMap(themeName);
  return Object.entries(variables).map(([name, value]) => ({ name, value }));
};

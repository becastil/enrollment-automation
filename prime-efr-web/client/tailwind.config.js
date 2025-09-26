/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        surface: 'var(--color-surface)',
        'surface-subtle': 'var(--color-surface-subtle)',
        'surface-raised': 'var(--color-surface-raised)',
        'surface-inverse': 'var(--color-surface-inverse)',
        border: 'var(--color-border)',
        'border-strong': 'var(--color-border-strong)',
        text: 'var(--color-text)',
        'text-muted': 'var(--color-text-muted)',
        'text-inverse': 'var(--color-text-inverse)',
        primary: 'var(--color-primary)',
        'primary-strong': 'var(--color-primary-strong)',
        'primary-soft': 'var(--color-primary-soft)',
        success: 'var(--color-success)',
        'success-soft': 'var(--color-success-soft)',
        warning: 'var(--color-warning)',
        'warning-soft': 'var(--color-warning-soft)',
        danger: 'var(--color-danger)',
        'danger-soft': 'var(--color-danger-soft)',
        overlay: 'var(--color-overlay)',
      },
      borderColor: {
        DEFAULT: 'var(--color-border)',
        strong: 'var(--color-border-strong)',
      },
      borderRadius: {
        sm: 'var(--radius-sm)',
        md: 'var(--radius-md)',
        lg: 'var(--radius-lg)',
        xl: 'var(--radius-xl)',
        full: 'var(--radius-full)',
      },
      spacing: {
        '2xs': 'var(--space-2xs)',
        xs: 'var(--space-xs)',
        sm: 'var(--space-sm)',
        md: 'var(--space-md)',
        lg: 'var(--space-lg)',
        xl: 'var(--space-xl)',
        '2xl': 'var(--space-2xl)',
      },
      fontFamily: {
        sans: 'var(--font-family-sans)',
        mono: 'var(--font-family-mono)',
      },
      fontSize: {
        xs: ['var(--font-size-xs)', 'var(--line-height-xs)'],
        sm: ['var(--font-size-sm)', 'var(--line-height-sm)'],
        base: ['var(--font-size-base)', 'var(--line-height-base)'],
        lg: ['var(--font-size-lg)', 'var(--line-height-lg)'],
        xl: ['var(--font-size-xl)', 'var(--line-height-xl)'],
        '2xl': ['var(--font-size-2xl)', 'var(--line-height-2xl)'],
        '3xl': ['var(--font-size-3xl)', 'var(--line-height-3xl)'],
      },
      boxShadow: {
        sm: 'var(--shadow-sm)',
        DEFAULT: 'var(--shadow-md)',
        md: 'var(--shadow-md)',
        lg: 'var(--shadow-lg)',
      },
      zIndex: {
        base: 'var(--z-index-base)',
        dropdown: 'var(--z-index-dropdown)',
        overlay: 'var(--z-index-overlay)',
        modal: 'var(--z-index-modal)',
        popover: 'var(--z-index-popover)',
        toast: 'var(--z-index-toast)',
      },
      animation: {
        'spin-slow': 'spin 3s linear infinite',
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}

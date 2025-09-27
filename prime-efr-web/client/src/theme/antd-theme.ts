import type { ThemeConfig } from 'antd';

export const antdTheme: ThemeConfig = {
  token: {
    // Colors
    colorPrimary: '#3b82f6', // blue-500
    colorSuccess: '#10b981', // emerald-500
    colorWarning: '#f59e0b', // amber-500
    colorError: '#ef4444', // red-500
    colorInfo: '#06b6d4', // cyan-500
    
    // Neutral colors
    colorTextBase: '#111827', // gray-900
    colorTextSecondary: '#6b7280', // gray-500
    colorTextTertiary: '#9ca3af', // gray-400
    colorTextQuaternary: '#d1d5db', // gray-300
    
    // Background colors
    colorBgBase: '#ffffff',
    colorBgContainer: '#ffffff',
    colorBgElevated: '#ffffff',
    colorBgLayout: '#f9fafb', // gray-50
    colorBgSpotlight: '#f3f4f6', // gray-100
    
    // Border colors
    colorBorder: '#e5e7eb', // gray-200
    colorBorderSecondary: '#f3f4f6', // gray-100
    
    // Typography
    fontSize: 14,
    fontSizeHeading1: 30,
    fontSizeHeading2: 24,
    fontSizeHeading3: 20,
    fontSizeHeading4: 16,
    fontSizeHeading5: 14,
    fontSizeLG: 16,
    fontSizeSM: 12,
    fontSizeXL: 20,
    
    // Spacing
    padding: 16,
    paddingLG: 24,
    paddingSM: 12,
    paddingXL: 32,
    paddingXS: 8,
    paddingXXS: 4,
    
    margin: 16,
    marginLG: 24,
    marginSM: 12,
    marginXL: 32,
    marginXS: 8,
    marginXXS: 4,
    
    // Border radius
    borderRadius: 6,
    borderRadiusLG: 8,
    borderRadiusSM: 4,
    borderRadiusXS: 2,
    
    // Shadows
    boxShadow: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
    boxShadowSecondary: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
    boxShadowTertiary: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
    
    // Line height
    lineHeight: 1.5,
    lineHeightLG: 1.5,
    lineHeightSM: 1.5,
    
    // Motion
    motionDurationFast: '0.1s',
    motionDurationMid: '0.2s',
    motionDurationSlow: '0.3s',
  },
  components: {
    Layout: {
      siderBg: '#ffffff',
      headerBg: '#ffffff',
      bodyBg: '#f9fafb',
      headerHeight: 64,
    },
    Menu: {
      itemBg: 'transparent',
      subMenuItemBg: 'transparent',
      itemSelectedBg: '#eff6ff', // blue-50
      itemSelectedColor: '#3b82f6', // blue-500
      itemHoverBg: '#f3f4f6', // gray-100
    },
    Card: {
      borderRadiusLG: 8,
      boxShadowTertiary: '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
    },
    Button: {
      borderRadius: 6,
      controlHeight: 36,
      controlHeightLG: 40,
      controlHeightSM: 32,
    },
    Input: {
      borderRadius: 6,
      controlHeight: 36,
      controlHeightLG: 40,
      controlHeightSM: 32,
    },
    Table: {
      borderRadius: 6,
      headerBg: '#f9fafb',
    },
    Upload: {
      colorPrimaryHover: '#2563eb', // blue-600
    },
    Tabs: {
      itemSelectedColor: '#3b82f6',
      itemHoverColor: '#2563eb',
      inkBarColor: '#3b82f6',
    },
  },
  algorithm: undefined, // Use default algorithm (light theme)
};

// Dark theme variant
export const antdDarkTheme: ThemeConfig = {
  ...antdTheme,
  token: {
    ...antdTheme.token,
    colorTextBase: '#f9fafb', // gray-50
    colorTextSecondary: '#9ca3af', // gray-400
    colorTextTertiary: '#6b7280', // gray-500
    colorTextQuaternary: '#4b5563', // gray-600
    
    colorBgBase: '#111827', // gray-900
    colorBgContainer: '#1f2937', // gray-800
    colorBgElevated: '#374151', // gray-700
    colorBgLayout: '#0f172a', // slate-900
    colorBgSpotlight: '#1e293b', // slate-800
    
    colorBorder: '#374151', // gray-700
    colorBorderSecondary: '#4b5563', // gray-600
  },
  components: {
    ...antdTheme.components,
    Layout: {
      ...antdTheme.components?.Layout,
      siderBg: '#1f2937',
      headerBg: '#1f2937',
      bodyBg: '#111827',
    },
    Menu: {
      ...antdTheme.components?.Menu,
      itemSelectedBg: '#1e40af', // blue-800
      itemHoverBg: '#374151', // gray-700
    },
    Table: {
      ...antdTheme.components?.Table,
      headerBg: '#374151',
    },
  },
};
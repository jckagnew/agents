/**
 * Platform-Aware Design Tokens for Landing Page Components
 *
 * These tokens follow platform conventions:
 * - iOS: Human Interface Guidelines
 * - Android: Material Design 3
 * - Web: Modern web best practices
 *
 * Generated for the Design-First Software Factory landing page
 */

import { Platform } from 'react-native';

/**
 * Platform-specific value selector
 */
export function platformValue<T>(values: { ios: T; android: T; web: T }): T {
  return Platform.select(values) as T;
}

/**
 * Color System
 * WCAG AA compliant (4.5:1 contrast ratio minimum)
 */
export const colors = {
  // Primary brand colors
  primary: {
    main: platformValue({
      ios: '#007AFF',      // iOS Blue
      android: '#6200EE',  // Material Purple
      web: '#0066CC',      // Web Blue
    }),
    light: platformValue({
      ios: '#5AC8FA',
      android: '#BB86FC',
      web: '#4D94FF',
    }),
    dark: platformValue({
      ios: '#0051D5',
      android: '#3700B3',
      web: '#0047A3',
    }),
  },

  // Secondary accent colors
  secondary: {
    main: platformValue({
      ios: '#5856D6',      // iOS Purple
      android: '#03DAC6',  // Material Teal
      web: '#7C3AED',      // Web Purple
    }),
    light: platformValue({
      ios: '#8E8DD8',
      android: '#66FFF9',
      web: '#A78BFA',
    }),
    dark: platformValue({
      ios: '#3634A3',
      android: '#00A896',
      web: '#5B21B6',
    }),
  },

  // Background colors
  background: {
    primary: platformValue({
      ios: '#FFFFFF',
      android: '#FFFFFF',
      web: '#FFFFFF',
    }),
    secondary: platformValue({
      ios: '#F2F2F7',      // iOS grouped background
      android: '#F5F5F5',  // Material surface variant
      web: '#F9FAFB',      // Web gray-50
    }),
    tertiary: platformValue({
      ios: '#E5E5EA',
      android: '#EEEEEE',
      web: '#F3F4F6',
    }),
  },

  // Surface colors (cards, modals)
  surface: {
    elevated: platformValue({
      ios: '#FFFFFF',
      android: '#FFFFFF',
      web: '#FFFFFF',
    }),
    overlay: platformValue({
      ios: 'rgba(0, 0, 0, 0.4)',
      android: 'rgba(0, 0, 0, 0.5)',
      web: 'rgba(0, 0, 0, 0.4)',
    }),
  },

  // Text colors
  text: {
    primary: platformValue({
      ios: '#000000',
      android: '#000000',
      web: '#111827',      // Web gray-900
    }),
    secondary: platformValue({
      ios: '#3C3C43',      // iOS secondary label
      android: '#757575',  // Material on-surface variant
      web: '#6B7280',      // Web gray-500
    }),
    tertiary: platformValue({
      ios: '#8E8E93',
      android: '#9E9E9E',
      web: '#9CA3AF',
    }),
    inverse: platformValue({
      ios: '#FFFFFF',
      android: '#FFFFFF',
      web: '#FFFFFF',
    }),
  },

  // Semantic colors
  success: '#10B981',
  warning: '#F59E0B',
  error: '#EF4444',
  info: '#3B82F6',

  // Border colors
  border: {
    light: platformValue({
      ios: '#E5E5EA',
      android: '#E0E0E0',
      web: '#E5E7EB',
    }),
    medium: platformValue({
      ios: '#C6C6C8',
      android: '#BDBDBD',
      web: '#D1D5DB',
    }),
    dark: platformValue({
      ios: '#8E8E93',
      android: '#9E9E9E',
      web: '#9CA3AF',
    }),
  },
};

/**
 * Typography System
 * Font sizes optimized for each platform's reading distance
 */
export const typography = {
  fontFamily: {
    heading: platformValue({
      ios: 'System',
      android: 'Roboto',
      web: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    }),
    body: platformValue({
      ios: 'System',
      android: 'Roboto',
      web: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
    }),
    monospace: platformValue({
      ios: 'Menlo',
      android: 'Roboto Mono',
      web: '"Fira Code", "Courier New", monospace',
    }),
  },

  fontSize: {
    // Display sizes (marketing headlines)
    display: {
      large: platformValue({
        ios: 48,
        android: 45,
        web: 56,
      }),
      medium: platformValue({
        ios: 40,
        android: 38,
        web: 48,
      }),
      small: platformValue({
        ios: 36,
        android: 34,
        web: 40,
      }),
    },

    // Heading sizes
    h1: platformValue({
      ios: 34,
      android: 32,
      web: 36,
    }),
    h2: platformValue({
      ios: 28,
      android: 24,
      web: 30,
    }),
    h3: platformValue({
      ios: 22,
      android: 20,
      web: 24,
    }),
    h4: platformValue({
      ios: 20,
      android: 18,
      web: 20,
    }),
    h5: platformValue({
      ios: 17,
      android: 16,
      web: 18,
    }),
    h6: platformValue({
      ios: 15,
      android: 14,
      web: 16,
    }),

    // Body sizes
    body: {
      large: platformValue({
        ios: 19,
        android: 18,
        web: 18,
      }),
      medium: platformValue({
        ios: 17,
        android: 16,
        web: 16,
      }),
      small: platformValue({
        ios: 15,
        android: 14,
        web: 14,
      }),
    },

    // Utility sizes
    caption: platformValue({
      ios: 13,
      android: 12,
      web: 12,
    }),
    overline: platformValue({
      ios: 11,
      android: 10,
      web: 10,
    }),
  },

  fontWeight: {
    light: '300' as const,
    regular: '400' as const,
    medium: '500' as const,
    semibold: '600' as const,
    bold: '700' as const,
    black: '900' as const,
  },

  lineHeight: {
    tight: 1.25,
    normal: 1.5,
    relaxed: 1.75,
    loose: 2,
  },

  letterSpacing: {
    tight: -0.5,
    normal: 0,
    wide: 0.5,
    wider: 1,
  },
};

/**
 * Spacing System
 * Based on 4px base unit, platform-adjusted
 */
export const spacing = {
  xs: platformValue({
    ios: 4,
    android: 4,
    web: 4,
  }),
  sm: platformValue({
    ios: 8,
    android: 8,
    web: 8,
  }),
  md: platformValue({
    ios: 16,
    android: 12,
    web: 16,
  }),
  lg: platformValue({
    ios: 24,
    android: 20,
    web: 24,
  }),
  xl: platformValue({
    ios: 32,
    android: 28,
    web: 32,
  }),
  '2xl': platformValue({
    ios: 48,
    android: 40,
    web: 48,
  }),
  '3xl': platformValue({
    ios: 64,
    android: 56,
    web: 64,
  }),
  '4xl': platformValue({
    ios: 96,
    android: 80,
    web: 96,
  }),
};

/**
 * Border Radius System
 */
export const borderRadius = {
  none: 0,
  xs: platformValue({
    ios: 4,
    android: 4,
    web: 4,
  }),
  sm: platformValue({
    ios: 8,
    android: 4,
    web: 6,
  }),
  md: platformValue({
    ios: 12,
    android: 8,
    web: 8,
  }),
  lg: platformValue({
    ios: 16,
    android: 12,
    web: 12,
  }),
  xl: platformValue({
    ios: 20,
    android: 16,
    web: 16,
  }),
  '2xl': platformValue({
    ios: 24,
    android: 20,
    web: 24,
  }),
  full: 9999,
};

/**
 * Shadow System
 */
export const shadows = {
  sm: platformValue({
    ios: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 1 },
      shadowOpacity: 0.05,
      shadowRadius: 2,
      elevation: 1,
    },
    android: {
      elevation: 2,
    },
    web: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 1 },
      shadowOpacity: 0.05,
      shadowRadius: 2,
    },
  }),
  md: platformValue({
    ios: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 4 },
      shadowOpacity: 0.1,
      shadowRadius: 6,
      elevation: 4,
    },
    android: {
      elevation: 4,
    },
    web: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 4 },
      shadowOpacity: 0.1,
      shadowRadius: 6,
    },
  }),
  lg: platformValue({
    ios: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 8 },
      shadowOpacity: 0.15,
      shadowRadius: 12,
      elevation: 8,
    },
    android: {
      elevation: 8,
    },
    web: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 8 },
      shadowOpacity: 0.15,
      shadowRadius: 12,
    },
  }),
  xl: platformValue({
    ios: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 12 },
      shadowOpacity: 0.2,
      shadowRadius: 16,
      elevation: 12,
    },
    android: {
      elevation: 12,
    },
    web: {
      shadowColor: '#000',
      shadowOffset: { width: 0, height: 12 },
      shadowOpacity: 0.2,
      shadowRadius: 16,
    },
  }),
};

/**
 * Animation/Transition Durations
 */
export const animation = {
  duration: {
    fast: 150,
    normal: 250,
    slow: 350,
  },
  easing: {
    easeIn: 'ease-in',
    easeOut: 'ease-out',
    easeInOut: 'ease-in-out',
    spring: platformValue({
      ios: 'spring',
      android: 'ease-out',
      web: 'cubic-bezier(0.68, -0.55, 0.265, 1.55)',
    }),
  },
};

/**
 * Breakpoints for Responsive Design
 */
export const breakpoints = {
  mobile: 375,     // iPhone SE, small phones
  tablet: 768,     // iPad, tablets
  desktop: 1024,   // Desktop minimum
  wide: 1440,      // Large desktop
  ultrawide: 1920, // 1080p displays
};

/**
 * Touch Target Sizes (Accessibility)
 * WCAG minimum: 44x44px
 */
export const touchTargets = {
  minimum: 44,
  comfortable: 48,
  large: 56,
};

/**
 * Z-Index Layers
 */
export const zIndex = {
  base: 0,
  dropdown: 1000,
  sticky: 1020,
  fixed: 1030,
  modalBackdrop: 1040,
  modal: 1050,
  popover: 1060,
  tooltip: 1070,
};

/**
 * Opacity Values
 */
export const opacity = {
  disabled: 0.38,
  divider: 0.12,
  hover: 0.08,
  focus: 0.12,
  selected: 0.16,
};

// Export all tokens as default
export default {
  colors,
  typography,
  spacing,
  borderRadius,
  shadows,
  animation,
  breakpoints,
  touchTargets,
  zIndex,
  opacity,
};

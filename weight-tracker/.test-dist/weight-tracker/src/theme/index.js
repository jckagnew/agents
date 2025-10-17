"use strict";
/**
 * Weight Tracker Design System
 * Google-inspired theme with bright, friendly colors and approachable typography
 * Following Codex design direction recommendations
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.theme = exports.components = exports.animations = exports.shadows = exports.borderRadius = exports.spacing = exports.typography = exports.colors = void 0;
exports.colors = {
    // Primary palette - Google-inspired
    primary: '#4285F4', // Google blue
    secondary: '#FBBC04', // Warm yellow accent
    success: '#0F9D58', // Supporting green
    // Surface colors
    surface: '#FFFFFF',
    background: '#F5F7FA',
    muted: '#6B7280',
    // Pastel tints for card backgrounds
    tintBlue: '#E3F2FD',
    tintGreen: '#E6F4EA',
    tintYellow: '#FEEFC3',
    // Neutral grays
    gray50: '#F9FAFB',
    gray100: '#F3F4F6',
    gray200: '#E5E7EB',
    gray300: '#D1D5DB',
    gray400: '#9CA3AF',
    gray500: '#6B7280',
    gray600: '#4B5563',
    gray700: '#374151',
    gray800: '#1F2937',
    gray900: '#111827',
    // Semantic colors
    error: '#EF4444',
    warning: '#F59E0B',
    info: '#3B82F6',
    // Chart colors
    chartPrimary: '#4285F4',
    chartSecondary: '#0F9D58',
    chartAccent: '#FBBC04',
    chartArea: 'rgba(66, 133, 244, 0.3)',
    chartGoal: '#0F9D58',
    // Text colors
    textPrimary: '#111827',
    textSecondary: '#6B7280',
    textMuted: '#9CA3AF',
    textInverse: '#FFFFFF',
    // Border colors
    border: '#E5E7EB',
    borderLight: '#F3F4F6',
    borderDark: '#D1D5DB',
};
exports.typography = {
    // Font families
    fontFamily: {
        heading: 'Poppins_600SemiBold', // or B612 for headlines
        body: 'Nunito_400Regular',
        bodyMedium: 'Nunito_500Medium',
        label: 'Nunito_600SemiBold',
    },
    // Font sizes (in rem, converted to pixels for React Native)
    fontSize: {
        h1: 36, // 2.25rem
        h2: 28, // 1.75rem  
        h3: 24, // 1.5rem
        bodyLg: 18, // 1.125rem
        body: 16, // 1rem
        label: 14, // 0.875rem
        small: 12, // 0.75rem
        tiny: 10, // 0.625rem
    },
    // Font weights
    fontWeight: {
        normal: '400',
        medium: '500',
        semibold: '600',
        bold: '700',
    },
    // Line heights
    lineHeight: {
        tight: 1.2,
        normal: 1.4,
        relaxed: 1.6,
    },
    // Letter spacing
    letterSpacing: {
        tight: -1,
        normal: 0,
        wide: 0.5,
    },
};
exports.spacing = {
    // 8pt base system
    xs: 4, // 0.5rem
    sm: 8, // 1rem
    md: 12, // 1.5rem
    lg: 16, // 2rem
    xl: 20, // 2.5rem
    '2xl': 24, // 3rem
    '3xl': 32, // 4rem
    '4xl': 40, // 5rem
    '5xl': 48, // 6rem
};
exports.borderRadius = {
    none: 0,
    sm: 4,
    md: 8,
    lg: 12,
    xl: 16, // Cards
    '2xl': 20,
    full: 9999,
};
exports.shadows = {
    // Material Design level 2 shadows
    sm: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 1 },
        shadowOpacity: 0.05,
        shadowRadius: 2,
        elevation: 1,
    },
    md: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
        elevation: 3,
    },
    lg: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.15,
        shadowRadius: 8,
        elevation: 5,
    },
    xl: {
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 8 },
        shadowOpacity: 0.2,
        shadowRadius: 16,
        elevation: 8,
    },
};
exports.animations = {
    // Animation durations (in milliseconds)
    duration: {
        fast: 150,
        normal: 300,
        slow: 500,
    },
    // Easing functions
    easing: {
        easeIn: 'ease-in',
        easeOut: 'ease-out',
        easeInOut: 'ease-in-out',
    },
    // Common animation presets
    presets: {
        // Card press animation
        cardPress: {
            scale: 0.98,
            duration: 150,
        },
        // Fade in animation
        fadeIn: {
            opacity: 1,
            duration: 300,
        },
        // Slide up animation
        slideUp: {
            translateY: 0,
            duration: 300,
        },
    },
};
// Component-specific theme tokens
exports.components = {
    // Metric Card styling
    metricCard: {
        backgroundColor: exports.colors.surface,
        borderRadius: exports.borderRadius.xl,
        padding: exports.spacing.lg,
        ...exports.shadows.md,
        // Pastel tint background will be applied conditionally
    },
    // Button styling
    button: {
        primary: {
            backgroundColor: exports.colors.primary,
            borderRadius: exports.borderRadius.lg,
            paddingVertical: exports.spacing.md,
            paddingHorizontal: exports.spacing.lg,
            ...exports.shadows.sm,
        },
        secondary: {
            backgroundColor: exports.colors.surface,
            borderColor: exports.colors.primary,
            borderWidth: 1,
            borderRadius: exports.borderRadius.lg,
            paddingVertical: exports.spacing.md,
            paddingHorizontal: exports.spacing.lg,
            ...exports.shadows.sm,
        },
    },
    // Chart styling
    chart: {
        primaryLine: {
            stroke: exports.colors.chartPrimary,
            strokeWidth: 2,
        },
        goalLine: {
            stroke: exports.colors.chartGoal,
            strokeWidth: 2,
            strokeDasharray: '5,5',
        },
        area: {
            fill: exports.colors.chartArea,
        },
    },
    // Form styling
    input: {
        backgroundColor: exports.colors.surface,
        borderColor: exports.colors.border,
        borderWidth: 1,
        borderRadius: exports.borderRadius.lg,
        paddingVertical: exports.spacing.md,
        paddingHorizontal: exports.spacing.lg,
        fontSize: exports.typography.fontSize.body,
        fontFamily: exports.typography.fontFamily.body,
    },
};
// Export default theme object
exports.theme = {
    colors: exports.colors,
    typography: exports.typography,
    spacing: exports.spacing,
    borderRadius: exports.borderRadius,
    shadows: exports.shadows,
    animations: exports.animations,
    components: exports.components,
};
exports.default = exports.theme;

"use strict";
/**
 * Shared Google-inspired design system tokens.
 * Used by both React Native (weight-tracker) and web experiences.
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.theme = exports.components = exports.animations = exports.shadows = exports.borderRadius = exports.spacing = exports.typography = exports.colors = void 0;
exports.colors = {
    primary: '#4285F4',
    secondary: '#FBBC04',
    success: '#0F9D58',
    surface: '#FFFFFF',
    background: '#F5F7FA',
    muted: '#6B7280',
    tintBlue: '#E3F2FD',
    tintGreen: '#E6F4EA',
    tintYellow: '#FEEFC3',
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
    error: '#EF4444',
    warning: '#F59E0B',
    info: '#3B82F6',
    chartPrimary: '#4285F4',
    chartSecondary: '#0F9D58',
    chartAccent: '#FBBC04',
    chartArea: 'rgba(66, 133, 244, 0.3)',
    chartGoal: '#0F9D58',
    textPrimary: '#111827',
    textSecondary: '#6B7280',
    textMuted: '#9CA3AF',
    textInverse: '#FFFFFF',
    border: '#E5E7EB',
    borderLight: '#F3F4F6',
    borderDark: '#D1D5DB',
};
exports.typography = {
    fontFamily: {
        heading: 'Poppins_600SemiBold',
        body: 'Nunito_400Regular',
        bodyMedium: 'Nunito_500Medium',
        label: 'Nunito_600SemiBold',
    },
    fontSize: {
        h1: 36,
        h2: 28,
        h3: 24,
        bodyLg: 18,
        body: 16,
        label: 14,
        small: 12,
        tiny: 10,
    },
    fontWeight: {
        normal: '400',
        medium: '500',
        semibold: '600',
        bold: '700',
    },
    lineHeight: {
        tight: 1.2,
        normal: 1.4,
        relaxed: 1.6,
    },
    letterSpacing: {
        tight: -1,
        normal: 0,
        wide: 0.5,
    },
};
exports.spacing = {
    xs: 4,
    sm: 8,
    md: 12,
    lg: 16,
    xl: 20,
    '2xl': 24,
    '3xl': 32,
    '4xl': 40,
    '5xl': 48,
};
exports.borderRadius = {
    none: 0,
    sm: 4,
    md: 8,
    lg: 12,
    xl: 16,
    '2xl': 20,
    full: 9999,
};
exports.shadows = {
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
    duration: {
        fast: 150,
        normal: 300,
        slow: 500,
    },
    easing: {
        easeIn: 'ease-in',
        easeOut: 'ease-out',
        easeInOut: 'ease-in-out',
    },
    presets: {
        cardPress: {
            scale: 0.98,
            duration: 150,
        },
        fadeIn: {
            opacity: 1,
            duration: 300,
        },
        slideUp: {
            translateY: 0,
            duration: 300,
        },
    },
};
exports.components = {
    metricCard: {
        backgroundColor: exports.colors.surface,
        borderRadius: exports.borderRadius.xl,
        padding: exports.spacing.lg,
        ...exports.shadows.md,
    },
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

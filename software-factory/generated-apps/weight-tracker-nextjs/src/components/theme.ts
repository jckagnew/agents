/**
 * Design Tokens - Centralized styling constants for Weight Tracker
 */

export const theme = {
  colors: {
    // Brand colors
    primary: '#1976D2', // Blue (improved contrast)
    secondary: '#FBBC04', // Yellow/Orange
    success: '#0F9D58', // Green
    error: '#EF4444', // Red
    warning: '#F59E0B', // Orange
    
    // Surface colors
    surface: '#FFFFFF',
    background: '#F5F7FA',
    muted: '#6B7280',
    
    // Semantic colors
    textPrimary: '#111827',
    textSecondary: '#6B7280',
    textMuted: '#6B7280', // Improved contrast
    textInverse: '#FFFFFF',
    
    // Border colors
    border: '#E5E7EB',
    borderLight: '#F3F4F6',
    borderDark: '#D1D5DB',
  },
  
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '12px',
    lg: '16px',
    xl: '20px',
    '2xl': '24px',
    '3xl': '32px',
    '4xl': '40px',
    '5xl': '48px',
  },
  
  borderRadius: {
    none: '0px',
    sm: '4px',
    md: '8px',
    lg: '12px',
    xl: '16px',
    '2xl': '20px',
    full: '9999px',
  },
  
  typography: {
    fontSans: '"Nunito", "Helvetica Neue", sans-serif',
    fontHeading: '"Poppins", "Helvetica Neue", sans-serif',
    fontBody: '"Nunito", "Helvetica Neue", sans-serif',
  },
  
  fontSize: {
    h1: '36px',
    h2: '28px',
    h3: '24px',
    bodyLg: '18px',
    body: '16px',
    label: '14px',
    small: '12px',
  },
  
  shadows: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
    xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
    '2xl': '0 24px 48px rgba(17, 24, 39, 0.08)',
  },
  
  breakpoints: {
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px',
  },
  
  layout: {
    maxWidth: '1200px',
    padding: {
      mobile: '16px',
      tablet: '24px',
      desktop: '32px',
    },
    sectionSpacing: {
      mobile: '24px',
      tablet: '32px',
      desktop: '48px',
    },
  },
};

export default theme;

/**
 * Button Component
 * Primary and secondary buttons with Google Material Design styling
 * Full-width primary blue with rounded corners
 */

import React from 'react';
import {
  TouchableOpacity,
  Text,
  StyleSheet,
  ViewStyle,
  TextStyle,
  ActivityIndicator,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { theme } from '../theme';

interface ButtonProps {
  title: string;
  onPress: () => void;
  variant?: 'primary' | 'secondary' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  icon?: keyof typeof Ionicons.glyphMap;
  iconPosition?: 'left' | 'right';
  disabled?: boolean;
  loading?: boolean;
  fullWidth?: boolean;
  style?: ViewStyle;
  textStyle?: TextStyle;
}

export const Button: React.FC<ButtonProps> = ({
  title,
  onPress,
  variant = 'primary',
  size = 'md',
  icon,
  iconPosition = 'left',
  disabled = false,
  loading = false,
  fullWidth = false,
  style,
  textStyle,
}) => {
  const getButtonStyle = (): ViewStyle => {
    const baseStyle = {
      ...theme.components.button[variant],
      ...getSizeStyle(),
      ...(fullWidth && { width: '100%' }),
      ...(disabled && { opacity: 0.5 }),
    };

    return baseStyle;
  };

  const getSizeStyle = (): ViewStyle => {
    switch (size) {
      case 'sm':
        return {
          paddingVertical: theme.spacing.sm,
          paddingHorizontal: theme.spacing.md,
        };
      case 'lg':
        return {
          paddingVertical: theme.spacing.lg,
          paddingHorizontal: theme.spacing.xl,
        };
      default: // md
        return {
          paddingVertical: theme.spacing.md,
          paddingHorizontal: theme.spacing.lg,
        };
    }
  };

  const getTextStyle = (): TextStyle => {
    const baseStyle = {
      fontSize: getTextSize(),
      fontFamily: theme.typography.fontFamily.label,
      textAlign: 'center' as const,
    };

    switch (variant) {
      case 'primary':
        return { ...baseStyle, color: theme.colors.textInverse };
      case 'secondary':
        return { ...baseStyle, color: theme.colors.primary };
      case 'outline':
        return { ...baseStyle, color: theme.colors.textPrimary };
      default:
        return baseStyle;
    }
  };

  const getTextSize = (): number => {
    switch (size) {
      case 'sm':
        return theme.typography.fontSize.label;
      case 'lg':
        return theme.typography.fontSize.bodyLg;
      default: // md
        return theme.typography.fontSize.body;
    }
  };

  const renderIcon = () => {
    if (loading) {
      return (
        <ActivityIndicator
          size="small"
          color={variant === 'primary' ? theme.colors.textInverse : theme.colors.primary}
          style={styles.icon}
        />
      );
    }

    if (icon) {
      return (
        <Ionicons
          name={icon}
          size={getTextSize()}
          color={variant === 'primary' ? theme.colors.textInverse : theme.colors.primary}
          style={[
            styles.icon,
            iconPosition === 'right' && styles.iconRight,
          ]}
        />
      );
    }

    return null;
  };

  return (
    <TouchableOpacity
      style={[getButtonStyle(), style]}
      onPress={onPress}
      disabled={disabled || loading}
      activeOpacity={0.8}
    >
      <Text style={[getTextStyle(), textStyle]}>
        {title}
      </Text>
      {renderIcon()}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  icon: {
    marginLeft: theme.spacing.sm,
  },
  iconRight: {
    marginLeft: 0,
    marginRight: theme.spacing.sm,
  },
});

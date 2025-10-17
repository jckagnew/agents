import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, ViewStyle } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { theme } from '../theme';

export interface ScreenHeaderProps {
  title: string;
  subtitle?: string;
  leftIcon?: keyof typeof Ionicons.glyphMap;
  rightIcon?: keyof typeof Ionicons.glyphMap;
  onPressLeft?: () => void;
  onPressRight?: () => void;
  leftIconAccessibilityLabel?: string;
  rightIconAccessibilityLabel?: string;
  leftIconTestID?: string;
  rightIconTestID?: string;
  containerStyle?: ViewStyle;
  children?: React.ReactNode;
}

export const ScreenHeader: React.FC<ScreenHeaderProps> = ({
  title,
  subtitle,
  leftIcon,
  rightIcon,
  onPressLeft,
  onPressRight,
  leftIconAccessibilityLabel,
  rightIconAccessibilityLabel,
  leftIconTestID,
  rightIconTestID,
  containerStyle,
  children,
}) => {
  return (
    <View style={[styles.container, containerStyle]}>
      <View style={styles.leading}>
        {onPressLeft && leftIcon ? (
          <TouchableOpacity
            onPress={onPressLeft}
            style={styles.iconButton}
            accessibilityRole="button"
            accessibilityLabel={leftIconAccessibilityLabel}
            testID={leftIconTestID}
          >
            <Ionicons name={leftIcon} size={24} color={theme.colors.textInverse} />
          </TouchableOpacity>
        ) : null}
        <View style={styles.titleGroup}>
          <Text style={styles.title}>{title}</Text>
          {subtitle ? <Text style={styles.subtitle}>{subtitle}</Text> : null}
          {children}
        </View>
      </View>
      {onPressRight && rightIcon ? (
        <TouchableOpacity
          onPress={onPressRight}
          style={styles.iconButton}
          accessibilityRole="button"
          accessibilityLabel={rightIconAccessibilityLabel}
          testID={rightIconTestID}
        >
          <Ionicons name={rightIcon} size={24} color={theme.colors.textInverse} />
        </TouchableOpacity>
      ) : null}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    backgroundColor: theme.colors.primary,
    paddingHorizontal: theme.spacing.xl,
    paddingVertical: theme.spacing.lg,
    borderBottomLeftRadius: theme.borderRadius.xl,
    borderBottomRightRadius: theme.borderRadius.xl,
    ...theme.shadows.lg,
  },
  leading: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: theme.spacing.md,
    flex: 1,
  },
  titleGroup: {
    flexShrink: 1,
  },
  title: {
    fontFamily: theme.typography.fontFamily.heading,
    fontSize: theme.typography.fontSize.h2,
    color: theme.colors.textInverse,
    marginBottom: theme.spacing.xs / 2,
  },
  subtitle: {
    fontFamily: theme.typography.fontFamily.body,
    fontSize: theme.typography.fontSize.body,
    color: 'rgba(255,255,255,0.72)',
  },
  iconButton: {
    padding: theme.spacing.sm,
    borderRadius: theme.borderRadius.lg,
    backgroundColor: 'rgba(255,255,255,0.12)',
  },
});

export default ScreenHeader;

/**
 * MetricCard Component
 * Displays key metrics with pastel tint backgrounds and micro-animations
 * Following Google Material Design principles
 */

import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  Animated,
  Pressable,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { theme } from '../theme';

interface MetricCardProps {
  title: string;
  value: string;
  subtitle?: string;
  delta?: {
    value: string;
    isPositive: boolean;
  };
  icon: keyof typeof Ionicons.glyphMap;
  tintColor: 'blue' | 'green' | 'yellow';
  onPress?: () => void;
  style?: any;
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  subtitle,
  delta,
  icon,
  tintColor,
  onPress,
  style,
}) => {
  const scaleValue = React.useRef(new Animated.Value(1)).current;

  const getTintBackground = () => {
    switch (tintColor) {
      case 'blue':
        return theme.colors.tintBlue;
      case 'green':
        return theme.colors.tintGreen;
      case 'yellow':
        return theme.colors.tintYellow;
      default:
        return theme.colors.gray50;
    }
  };

  const getTintIconColor = () => {
    switch (tintColor) {
      case 'blue':
        return theme.colors.primary;
      case 'green':
        return theme.colors.success;
      case 'yellow':
        return theme.colors.secondary;
      default:
        return theme.colors.muted;
    }
  };

  const handlePressIn = () => {
    Animated.timing(scaleValue, {
      toValue: 0.98,
      duration: theme.animations.duration.fast,
      useNativeDriver: true,
    }).start();
  };

  const handlePressOut = () => {
    Animated.timing(scaleValue, {
      toValue: 1,
      duration: theme.animations.duration.fast,
      useNativeDriver: true,
    }).start();
  };

  const CardContent = () => (
    <View style={[styles.container, { backgroundColor: getTintBackground() }, style]}>
      <View style={styles.header}>
        <View style={[styles.iconContainer, { backgroundColor: getTintIconColor() }]}>
          <Ionicons name={icon} size={24} color="white" />
        </View>
        <Text style={styles.title}>{title}</Text>
      </View>
      
      <View style={styles.content}>
        <Text style={styles.value}>{value}</Text>
        {subtitle && <Text style={styles.subtitle}>{subtitle}</Text>}
        {delta && (
          <View style={[
            styles.deltaPill,
            { backgroundColor: delta.isPositive ? theme.colors.success : theme.colors.error }
          ]}>
            <Text style={styles.deltaText}>
              {delta.isPositive ? '+' : ''}{delta.value}
            </Text>
          </View>
        )}
      </View>
    </View>
  );

  if (onPress) {
    return (
      <Pressable
        onPress={onPress}
        onPressIn={handlePressIn}
        onPressOut={handlePressOut}
      >
        <Animated.View style={{ transform: [{ scale: scaleValue }] }}>
          <CardContent />
        </Animated.View>
      </Pressable>
    );
  }

  return <CardContent />;
};

const styles = StyleSheet.create({
  container: {
    ...theme.components.metricCard,
    marginBottom: theme.spacing.md,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: theme.spacing.sm,
  },
  iconContainer: {
    width: 40,
    height: 40,
    borderRadius: theme.borderRadius.lg,
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: theme.spacing.sm,
  },
  title: {
    fontSize: theme.typography.fontSize.label,
    fontFamily: theme.typography.fontFamily.label,
    color: theme.colors.textSecondary,
    flex: 1,
  },
  content: {
    alignItems: 'flex-start',
  },
  value: {
    fontSize: theme.typography.fontSize.h2,
    fontFamily: theme.typography.fontFamily.heading,
    color: theme.colors.textPrimary,
    marginBottom: theme.spacing.xs,
  },
  subtitle: {
    fontSize: theme.typography.fontSize.body,
    fontFamily: theme.typography.fontFamily.body,
    color: theme.colors.textSecondary,
    marginBottom: theme.spacing.sm,
  },
  deltaPill: {
    paddingHorizontal: theme.spacing.sm,
    paddingVertical: theme.spacing.xs,
    borderRadius: theme.borderRadius.full,
  },
  deltaText: {
    fontSize: theme.typography.fontSize.small,
    fontFamily: theme.typography.fontFamily.label,
    color: 'white',
  },
});

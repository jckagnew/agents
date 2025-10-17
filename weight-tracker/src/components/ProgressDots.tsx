/**
 * ProgressDots Component
 * Multi-step modal progress indicator with pastel accent colors
 * Used in logging flow and other multi-step processes
 */

import React from 'react';
import {
  View,
  StyleSheet,
} from 'react-native';
import { theme } from '../theme';

interface ProgressDotsProps {
  currentStep: number;
  totalSteps: number;
  style?: any;
}

export const ProgressDots: React.FC<ProgressDotsProps> = ({
  currentStep,
  totalSteps,
  style,
}) => {
  return (
    <View style={[styles.container, style]}>
      {Array.from({ length: totalSteps }, (_, index) => {
        const stepNumber = index + 1;
        const isActive = stepNumber === currentStep;
        const isCompleted = stepNumber < currentStep;
        
        return (
          <View
            key={index}
            style={[
              styles.dot,
              isActive && styles.dotActive,
              isCompleted && styles.dotCompleted,
            ]}
          />
        );
      })}
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    justifyContent: 'center',
    alignItems: 'center',
    gap: theme.spacing.sm,
  },
  dot: {
    width: 8,
    height: 8,
    borderRadius: theme.borderRadius.full,
    backgroundColor: theme.colors.border,
  },
  dotActive: {
    backgroundColor: theme.colors.primary,
    width: 12,
    height: 12,
  },
  dotCompleted: {
    backgroundColor: theme.colors.success,
  },
});

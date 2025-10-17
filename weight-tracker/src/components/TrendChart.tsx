/**
 * TrendChart Component
 * Weight trend visualization with Google blue gradient and goal line
 * Area under line with gradient, goal line dashed green
 */

import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  Dimensions,
} from 'react-native';
import { VictoryChart, VictoryLine, VictoryAxis, VictoryArea } from 'victory-native';
import { theme } from '../theme';

const { width: screenWidth } = Dimensions.get('window');

interface TrendChartProps {
  data: Array<{ x: Date; y: number }>;
  goalLine?: number;
  showArea?: boolean;
  height?: number;
  title?: string;
  subtitle?: string;
  style?: any;
}

export const TrendChart: React.FC<TrendChartProps> = ({
  data,
  goalLine,
  showArea = true,
  height = 200,
  title,
  subtitle,
  style,
}) => {
  const chartWidth = screenWidth - (theme.spacing.lg * 2);

  return (
    <View style={[styles.container, style]}>
      {title && <Text style={styles.title}>{title}</Text>}
      {subtitle && <Text style={styles.subtitle}>{subtitle}</Text>}
      
      <View style={styles.chartContainer}>
        <VictoryChart
          height={height}
          width={chartWidth}
          padding={{ left: 50, right: 20, top: 20, bottom: 40 }}
        >
          {/* Area under the line with gradient */}
          {showArea && (
            <VictoryArea
              data={data}
              style={{
                data: {
                  fill: theme.colors.chartArea,
                  stroke: theme.colors.chartPrimary,
                  strokeWidth: 0,
                },
              }}
            />
          )}
          
          {/* Main trend line */}
          <VictoryLine
            data={data}
            style={{
              data: theme.components.chart.primaryLine,
            }}
          />
          
          {/* Goal line */}
          {goalLine && (
            <VictoryLine
              data={data.map(point => ({ ...point, y: goalLine }))}
              style={theme.components.chart.goalLine}
            />
          )}
          
          {/* Y-axis */}
          <VictoryAxis
            dependentAxis
            tickFormat={(x) => `${x.toFixed(0)}`}
            style={{
              axis: { stroke: theme.colors.border },
              tickLabels: { 
                fontSize: theme.typography.fontSize.small,
                fill: theme.colors.textSecondary,
                fontFamily: theme.typography.fontFamily.body,
              },
            }}
          />
          
          {/* X-axis */}
          <VictoryAxis
            tickFormat={(x) => {
              const date = new Date(x);
              return `${date.getMonth() + 1}/${date.getDate()}`;
            }}
            style={{
              axis: { stroke: theme.colors.border },
              tickLabels: { 
                fontSize: theme.typography.fontSize.small,
                fill: theme.colors.textSecondary,
                fontFamily: theme.typography.fontFamily.body,
              },
            }}
          />
        </VictoryChart>
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: theme.colors.surface,
    borderRadius: theme.borderRadius.xl,
    padding: theme.spacing.lg,
    ...theme.shadows.md,
  },
  title: {
    fontSize: theme.typography.fontSize.h3,
    fontFamily: theme.typography.fontFamily.heading,
    color: theme.colors.textPrimary,
    marginBottom: theme.spacing.xs,
  },
  subtitle: {
    fontSize: theme.typography.fontSize.body,
    fontFamily: theme.typography.fontFamily.body,
    color: theme.colors.textSecondary,
    marginBottom: theme.spacing.md,
  },
  chartContainer: {
    alignItems: 'center',
  },
});

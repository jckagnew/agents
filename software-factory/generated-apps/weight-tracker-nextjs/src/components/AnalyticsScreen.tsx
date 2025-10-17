'use client';

import type { CSSProperties } from 'react';
import React from 'react';
import { useWeight } from '../context/WeightContext';
import {
  ArrowLeftIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon,
} from '@heroicons/react/24/outline';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { colors } from '../../../../../design-system/googleTheme';

interface AnalyticsScreenProps {
  onNavigate: (screen: string) => void;
}

const pageStyle: CSSProperties = {
  backgroundColor: 'var(--color-background)',
};

const headerStyle: CSSProperties = {
  background: 'linear-gradient(135deg, var(--color-primary) 0%, var(--color-chart-secondary) 100%)',
  color: 'var(--color-text-inverse)',
  padding: 'var(--spacing-3xl)',
};

const taglineStyle: CSSProperties = {
  fontSize: 'var(--font-size-small)',
  color: 'rgba(255, 255, 255, 0.72)',
  margin: 0,
};

const contentStyle: CSSProperties = {
  display: 'flex',
  flexDirection: 'column',
  gap: 'var(--spacing-xl)',
  padding: 'var(--spacing-xl)',
};

const metricValueStyle: CSSProperties = {
  fontSize: 'var(--font-size-h2)',
  fontWeight: 700,
};

const metricLabelStyle: CSSProperties = {
  fontSize: 'var(--font-size-small)',
  color: 'var(--color-text-secondary)',
};

const chartContainerStyle: CSSProperties = {
  height: '16rem',
};

const trendLabelStyle: CSSProperties = {
  fontSize: 'var(--font-size-small)',
  color: 'var(--color-text-secondary)',
};

const trendValueBaseStyle: CSSProperties = {
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  gap: 'var(--spacing-xs)',
  fontSize: 'var(--font-size-h3)',
  fontWeight: 700,
};

const trendCardStyle: CSSProperties = {
  textAlign: 'center',
};

const chartPalette = {
  weight: colors.chartPrimary,
  bodyFat: colors.chartSecondary,
  accent: colors.chartAccent,
  goal: colors.chartGoal,
  grid: colors.borderLight,
};

const formatNumber = (value: number | string, fractionDigits = 1) => {
  const numeric = typeof value === 'number' ? value : Number(value);
  return Number.isFinite(numeric) ? numeric.toFixed(fractionDigits) : String(value);
};

export const AnalyticsScreen: React.FC<AnalyticsScreenProps> = ({ onNavigate }) => {
  const { entries, goalWeight } = useWeight();

  // Calculate analytics data
  const startWeight = entries[0]?.weight || 0;
  const currentWeight = entries[entries.length - 1]?.weight || 0;
  const totalLoss = startWeight - currentWeight;
  const totalDays = entries.length;
  const weeklyLoss = totalLoss / Math.max(1, Math.floor(totalDays / 7));
  const remainingToGoal = currentWeight - goalWeight;
  const progressBaseline = startWeight - goalWeight;
  const progressPercentage =
    progressBaseline !== 0
      ? Math.max(
          0,
          Math.min(100, ((startWeight - currentWeight) / progressBaseline) * 100),
        )
      : 0;
  const daysToGoal =
    weeklyLoss > 0 ? Math.max(0, Math.ceil(remainingToGoal / weeklyLoss)) : 0;

  // Prepare chart data
  const chartData = entries.map((entry, index) => ({
    date: new Date(entry.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    weight: entry.weight,
    bodyFat: entry.bodyFat,
    day: index + 1,
  }));

  // Calculate weekly averages
  const weeklyData: Array<{ week: number; weight: number; bodyFat: number }> = [];
  for (let i = 0; i < entries.length; i += 7) {
    const weekEntries = entries.slice(i, i + 7);
    if (weekEntries.length === 0) {
      continue;
    }
    const avgWeight =
      weekEntries.reduce((sum, entry) => sum + entry.weight, 0) / weekEntries.length;
    const avgBodyFat =
      weekEntries.reduce((sum, entry) => sum + entry.bodyFat, 0) / weekEntries.length;
    weeklyData.push({
      week: Math.floor(i / 7) + 1,
      weight: avgWeight,
      bodyFat: avgBodyFat,
    });
  }

  // Calculate trends
  const recentEntries = entries.slice(-7);
  const weightTrend = recentEntries.length > 1 ? 
    (recentEntries[recentEntries.length - 1].weight - recentEntries[0].weight) : 0;
  const bodyFatTrend = recentEntries.length > 1 ? 
    (recentEntries[recentEntries.length - 1].bodyFat - recentEntries[0].bodyFat) : 0;
  const weightTrendColor =
    weightTrend < 0
      ? 'var(--color-success)'
      : weightTrend > 0
      ? 'var(--color-error)'
      : 'var(--color-text-muted)';
  const bodyFatTrendColor =
    bodyFatTrend < 0
      ? 'var(--color-success)'
      : bodyFatTrend > 0
      ? 'var(--color-error)'
      : 'var(--color-text-muted)';

  return (
    <div className="min-h-screen" style={pageStyle}>
      <header style={headerStyle}>
        <div className="flex items-center gap-4">
          <button
            type="button"
            aria-label="Back to dashboard"
            onClick={() => onNavigate('dashboard')}
            className="icon-button"
          >
            <ArrowLeftIcon className="h-6 w-6" />
          </button>
          <div>
            <h1 className="section-title section-title--inverse" style={{ marginBottom: 'var(--spacing-xs)' }}>
              Analytics
            </h1>
            <p className="section-subtitle" style={taglineStyle}>
              Track your progress
            </p>
          </div>
        </div>
      </header>

      <main style={contentStyle}>
        <section className="card-surface">
          <h2 className="section-title">Key Metrics</h2>
          <div className="grid grid-cols-2 gap-4">
            <div style={trendCardStyle}>
              <div style={{ ...metricValueStyle, color: 'var(--color-success)' }}>
                {totalLoss.toFixed(1)} lbs
              </div>
              <div style={metricLabelStyle}>Total Loss</div>
            </div>
            <div style={trendCardStyle}>
              <div style={{ ...metricValueStyle, color: 'var(--color-primary)' }}>
                {weeklyLoss.toFixed(1)} lbs
              </div>
              <div style={metricLabelStyle}>Per Week</div>
            </div>
            <div style={trendCardStyle}>
              <div style={{ ...metricValueStyle, color: 'var(--color-chart-accent)' }}>
                {progressPercentage.toFixed(0)}%
              </div>
              <div style={metricLabelStyle}>Goal Progress</div>
            </div>
            <div style={trendCardStyle}>
              <div style={{ ...metricValueStyle, color: 'var(--color-warning)' }}>
                {daysToGoal}
              </div>
              <div style={metricLabelStyle}>Days to Goal</div>
            </div>
          </div>
        </section>

        <section className="card-surface card-surface--chart">
          <h2 className="section-title">Weight Trend</h2>
          <div style={chartContainerStyle}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData} margin={{ top: 8, right: 16, bottom: 8, left: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke={chartPalette.grid} />
                <XAxis dataKey="date" stroke="var(--color-text-muted)" />
                <YAxis domain={['dataMin - 2', 'dataMax + 2']} stroke="var(--color-text-muted)" />
                <Tooltip
                  formatter={(value: number | string) => [`${formatNumber(value)} lbs`, 'Weight']}
                  labelFormatter={(label: string) => `Date: ${label}`}
                  contentStyle={{
                    borderRadius: 12,
                    borderColor: chartPalette.grid,
                    fontSize: 'var(--font-size-small)',
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="weight"
                  stroke={chartPalette.weight}
                  strokeWidth={3}
                  dot={{ fill: chartPalette.weight, strokeWidth: 2, r: 4 }}
                  activeDot={{ r: 6 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="card-surface card-surface--chart">
          <h2 className="section-title">Body Fat Percentage</h2>
          <div style={chartContainerStyle}>
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData} margin={{ top: 8, right: 16, bottom: 8, left: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke={chartPalette.grid} />
                <XAxis dataKey="date" stroke="var(--color-text-muted)" />
                <YAxis domain={['dataMin - 1', 'dataMax + 1']} stroke="var(--color-text-muted)" />
                <Tooltip
                  formatter={(value: number | string) => [`${formatNumber(value)}%`, 'Body Fat']}
                  labelFormatter={(label: string) => `Date: ${label}`}
                  contentStyle={{
                    borderRadius: 12,
                    borderColor: chartPalette.grid,
                    fontSize: 'var(--font-size-small)',
                  }}
                />
                <Line
                  type="monotone"
                  dataKey="bodyFat"
                  stroke={chartPalette.bodyFat}
                  strokeWidth={3}
                  dot={{ fill: chartPalette.bodyFat, strokeWidth: 2, r: 4 }}
                  activeDot={{ r: 6 }}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="card-surface">
          <h2 className="section-title">Weekly Progress</h2>
          <div style={chartContainerStyle}>
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={weeklyData}>
                <CartesianGrid strokeDasharray="3 3" stroke={chartPalette.grid} />
                <XAxis dataKey="week" stroke="var(--color-text-muted)" />
                <YAxis stroke="var(--color-text-muted)" />
                <Tooltip
                  formatter={(value: number | string, name: string) => [
                    `${formatNumber(value)}${name === 'weight' ? ' lbs' : '%'}`,
                    name === 'weight' ? 'Weight' : 'Body Fat',
                  ]}
                  labelFormatter={(label: string | number) => `Week ${label}`}
                  contentStyle={{
                    borderRadius: 12,
                    borderColor: chartPalette.grid,
                    fontSize: 'var(--font-size-small)',
                  }}
                />
                <Bar dataKey="weight" fill={chartPalette.weight} radius={[12, 12, 12, 12]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </section>

        <section className="card-surface">
          <h2 className="section-title">Recent Trends (Last 7 Days)</h2>
          <div className="grid grid-cols-2 gap-4">
            <div style={trendCardStyle}>
              <div style={{ ...trendValueBaseStyle, color: weightTrendColor }}>
                {weightTrend < 0 ? (
                  <>
                    <ArrowTrendingDownIcon className="h-6 w-6" />
                    <span>{Math.abs(weightTrend).toFixed(1)} lbs</span>
                  </>
                ) : weightTrend > 0 ? (
                  <>
                    <ArrowTrendingUpIcon className="h-6 w-6" />
                    <span>+{weightTrend.toFixed(1)} lbs</span>
                  </>
                ) : (
                  <span>No change</span>
                )}
              </div>
              <div style={trendLabelStyle}>Weight Change</div>
            </div>
            <div style={trendCardStyle}>
              <div style={{ ...trendValueBaseStyle, color: bodyFatTrendColor }}>
                {bodyFatTrend < 0 ? (
                  <>
                    <ArrowTrendingDownIcon className="h-6 w-6" />
                    <span>{Math.abs(bodyFatTrend).toFixed(1)}%</span>
                  </>
                ) : bodyFatTrend > 0 ? (
                  <>
                    <ArrowTrendingUpIcon className="h-6 w-6" />
                    <span>+{bodyFatTrend.toFixed(1)}%</span>
                  </>
                ) : (
                  <span>No change</span>
                )}
              </div>
              <div style={trendLabelStyle}>Body Fat Change</div>
            </div>
          </div>
        </section>

        <section className="card-surface">
          <h2 className="section-title">Goal Progress</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-md)' }}>
            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                color: 'var(--color-text-secondary)',
                fontSize: 'var(--font-size-small)',
              }}
            >
              <span>Starting Weight: {startWeight} lbs</span>
              <span>Goal Weight: {goalWeight} lbs</span>
            </div>
            <div className="progress-track">
              <div className="progress-fill" style={{ width: `${progressPercentage}%` }} />
            </div>
            <div style={{ textAlign: 'center' }}>
              <span
                style={{
                  fontSize: 'var(--font-size-bodyLg)',
                  fontWeight: 600,
                  color: 'var(--color-text-primary)',
                }}
              >
                {progressPercentage.toFixed(1)}% Complete
              </span>
              <p style={{ ...metricLabelStyle, marginTop: 'var(--spacing-xs)' }}>
                {remainingToGoal.toFixed(1)} lbs remaining to reach your goal
              </p>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
};

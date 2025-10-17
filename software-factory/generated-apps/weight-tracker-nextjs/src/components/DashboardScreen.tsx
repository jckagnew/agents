'use client';

import type { CSSProperties } from 'react';
import React from 'react';
import { useWeight } from '../context/WeightContext';
import { MetricCard, PillButton } from './design-system';
import {
  PlusIcon,
  ClockIcon,
  ChartBarIcon,
  CogIcon,
  DevicePhoneMobileIcon,
  ComputerDesktopIcon,
  HomeIcon,
} from '@heroicons/react/24/outline';

interface DashboardScreenProps {
  onNavigate: (screen: string) => void;
}

const pageStyle: CSSProperties = {
  backgroundColor: 'var(--color-background)',
};

const contentStyle: CSSProperties = {
  display: 'flex',
  flexDirection: 'column',
  gap: 'var(--spacing-xl)',
  padding: 'var(--spacing-xl)',
};

const headerStyle: CSSProperties = {
  background: 'linear-gradient(135deg, var(--color-primary) 0%, var(--color-chart-secondary) 100%)',
  color: 'var(--color-text-inverse)',
  padding: 'var(--spacing-3xl)',
};

const headerTaglineStyle: CSSProperties = {
  fontSize: 'var(--font-size-small)',
  color: 'rgba(255, 255, 255, 0.72)',
  margin: 0,
};


const metricLabelStyle: CSSProperties = {
  color: 'var(--color-text-secondary)',
  fontSize: 'var(--font-size-small)',
};

const badgeContainerStyle: CSSProperties = {
  display: 'flex',
  flexWrap: 'wrap',
  gap: 'var(--spacing-sm)',
  marginBottom: 'var(--spacing-md)',
};

export const DashboardScreen: React.FC<DashboardScreenProps> = ({ onNavigate }) => {
  const { entries, currentWeight, currentBodyFat, goalWeight } = useWeight();
  
  // Calculate metrics
  const startWeight = entries[0]?.weight || 0;
  const totalLoss = startWeight - currentWeight;
  const weekAvg = entries.slice(-7).reduce((sum, entry) => sum + entry.weight, 0) / Math.min(7, entries.length);
  const weeklyLoss = totalLoss / Math.max(1, Math.floor(entries.length / 7));
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

  return (
    <div className="min-h-screen" style={pageStyle}>
      <header style={headerStyle}>
        <div className="flex items-center justify-between gap-6">
          <div className="flex items-center gap-4">
            <button
              type="button"
              aria-label="Home"
              onClick={() => onNavigate('dashboard')}
              className="icon-button"
              title="Home"
            >
              <HomeIcon className="h-6 w-6" />
            </button>
            <div>
              <h1 className="section-title section-title--inverse" style={{ marginBottom: 'var(--spacing-xs)' }}>
                Weight Tracker Pro
              </h1>
              <p className="section-subtitle" style={headerTaglineStyle}>
                Privacy-first tracking
              </p>
            </div>
          </div>
          <button
            type="button"
            aria-label="Open settings"
            onClick={() => onNavigate('settings')}
            className="icon-button"
          >
            <CogIcon className="h-6 w-6" />
          </button>
        </div>
      </header>

      <main style={contentStyle}>
        <MetricCard
          title="Today's Summary"
          value={`${currentWeight} lbs`}
          variant="summary"
        >
          <div style={{ textAlign: 'center' }}>
            <div style={metricLabelStyle}>Navy BF%: {currentBodyFat}%</div>
            <div style={metricLabelStyle}>7-day avg: {weekAvg.toFixed(1)} lbs</div>
            <div
              style={{
                fontSize: 'var(--font-size-bodyLg)',
                fontWeight: 600,
                color: 'var(--color-success)',
                marginBottom: 'var(--spacing-sm)',
              }}
            >
              -{weeklyLoss.toFixed(1)}% this week
            </div>
            <div style={metricLabelStyle}>
              Total loss: {totalLoss.toFixed(1)} lbs • Goal: {goalWeight} lbs ({remainingToGoal.toFixed(1)} lbs to go)
            </div>
          </div>
        </MetricCard>

        <MetricCard
          title="Weight Trend (Last 30 Days)"
          value=""
          variant="chart"
        >
          <div
            className="flex h-48 flex-col items-center justify-center rounded-lg"
            style={{ background: 'rgba(255, 255, 255, 0.6)' }}
          >
            <ChartBarIcon
              className="h-12 w-12"
              style={{ color: 'var(--color-primary)', marginBottom: 'var(--spacing-sm)' }}
            />
            <p
              style={{
                fontWeight: 600,
                color: 'var(--color-text-primary)',
                marginBottom: 'var(--spacing-xs)',
              }}
            >
              Weight Chart
            </p>
            <p
              style={{
                fontSize: 'var(--font-size-small)',
                color: 'var(--color-text-muted)',
                fontStyle: 'italic',
                marginBottom: 'var(--spacing-sm)',
              }}
            >
              Pro: Unlock smoothing controls
            </p>
            <div
              style={{
                fontSize: 'var(--font-size-small)',
                color: 'var(--color-text-secondary)',
                textAlign: 'center',
              }}
            >
              <div>Start: {startWeight} lbs → Current: {currentWeight} lbs</div>
              <div>Average weekly loss: {weeklyLoss.toFixed(1)} lbs</div>
            </div>
          </div>
        </MetricCard>

        <section
          className="card-surface"
          style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-md)' }}
        >
          <PillButton
            variant="primary"
            onClick={() => onNavigate('log-entry')}
            icon={<PlusIcon className="h-6 w-6" />}
          >
            Log Entry
          </PillButton>
          <div
            style={{
              display: 'grid',
              gap: 'var(--spacing-md)',
              gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))',
            }}
          >
            <PillButton
              variant="secondary"
              onClick={() => onNavigate('history')}
              icon={<ClockIcon className="h-5 w-5" />}
            >
              History
            </PillButton>
            <PillButton
              variant="secondary"
              onClick={() => onNavigate('analytics')}
              icon={<ChartBarIcon className="h-5 w-5" />}
            >
              Analytics
            </PillButton>
          </div>
        </section>

        <section className="card-surface">
          <h3 className="section-title">12-Week Progress</h3>
          <div className="grid grid-cols-2 gap-4" style={{ marginBottom: 'var(--spacing-md)' }}>
            <div style={{ textAlign: 'center' }}>
              <div
                style={{
                  fontSize: 'var(--font-size-h3)',
                  fontWeight: 700,
                  color: 'var(--color-success)',
                }}
              >
                {totalLoss.toFixed(1)} lbs
              </div>
              <div style={metricLabelStyle}>Total Lost</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div
                style={{
                  fontSize: 'var(--font-size-h3)',
                  fontWeight: 700,
                  color: 'var(--color-primary)',
                }}
              >
                {weeklyLoss.toFixed(1)} lbs
              </div>
              <div style={metricLabelStyle}>Per Week</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div
                style={{
                  fontSize: 'var(--font-size-h3)',
                  fontWeight: 700,
                  color: 'var(--color-chart-secondary)',
                }}
              >
                {(15.2 - currentBodyFat).toFixed(1)}%
              </div>
              <div style={metricLabelStyle}>BF Reduction</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div
                style={{
                  fontSize: 'var(--font-size-h3)',
                  fontWeight: 700,
                  color: 'var(--color-warning)',
                }}
              >
                {daysToGoal}
              </div>
              <div style={metricLabelStyle}>Days to Goal</div>
            </div>
          </div>
          <div className="progress-track">
            <div className="progress-fill" style={{ width: `${progressPercentage}%` }} />
          </div>
          <p style={{ ...metricLabelStyle, textAlign: 'center', marginTop: 'var(--spacing-sm)' }}>
            {Math.round(progressPercentage)}% to goal
          </p>
        </section>

        <section className="card-surface">
          <h3 className="section-title">Universal App Demo</h3>
          <p style={{ color: 'var(--color-text-secondary)', marginBottom: 'var(--spacing-md)' }}>
            This sophisticated Weight Tracker app runs natively on:
          </p>
          <div style={badgeContainerStyle}>
            <span className="pill-badge">
              <DevicePhoneMobileIcon className="h-4 w-4" />
              <span>iOS</span>
            </span>
            <span className="pill-badge">
              <DevicePhoneMobileIcon className="h-4 w-4" />
              <span>Android</span>
            </span>
            <span className="pill-badge">
              <ComputerDesktopIcon className="h-4 w-4" />
              <span>Web</span>
            </span>
          </div>
          <p style={{ color: 'var(--color-text-muted)', fontSize: 'var(--font-size-small)' }}>
            Single codebase • Native performance • Consistent UX
          </p>
        </section>
      </main>
    </div>
  );
};

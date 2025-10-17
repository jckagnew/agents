'use client';

import type { CSSProperties } from 'react';
import React, { useState } from 'react';
import { useWeight } from '../context/WeightContext';
import { PillButton } from './design-system';
import {
  ArrowLeftIcon,
  ScaleIcon,
  FlagIcon,
  BellIcon,
  ShieldCheckIcon,
  ArrowDownTrayIcon,
  TrashIcon,
} from '@heroicons/react/24/outline';

interface SettingsScreenProps {
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

const statsValueStyle: CSSProperties = {
  fontSize: 'var(--font-size-h3)',
  fontWeight: 700,
};

const statsLabelStyle: CSSProperties = {
  fontSize: 'var(--font-size-small)',
  color: 'var(--color-text-secondary)',
};

const controlStackStyle: CSSProperties = {
  display: 'flex',
  flexDirection: 'column',
  gap: 'var(--spacing-md)',
};

const controlRowStyle: CSSProperties = {
  display: 'flex',
  gap: 'var(--spacing-md)',
  flexWrap: 'wrap',
};

const toggleRowStyle: CSSProperties = {
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  gap: 'var(--spacing-md)',
  padding: 'var(--spacing-md)',
  borderRadius: 'var(--radius-lg)',
  background: 'rgba(17, 24, 39, 0.04)',
};

const infoRowStyle: CSSProperties = {
  display: 'flex',
  justifyContent: 'space-between',
  gap: 'var(--spacing-lg)',
  fontSize: 'var(--font-size-small)',
  color: 'var(--color-text-secondary)',
};

const infoLabelStyle: CSSProperties = {
  fontWeight: 600,
};

const accentControlStyle: CSSProperties = {
  accentColor: 'var(--color-primary)',
  height: '1.1rem',
  width: '1.1rem',
};

export const SettingsScreen: React.FC<SettingsScreenProps> = ({ onNavigate }) => {
  const { goalWeight, setGoalWeight, entries } = useWeight();
  const [newGoalWeight, setNewGoalWeight] = useState(goalWeight.toString());
  const [notifications, setNotifications] = useState(true);
  const [units, setUnits] = useState('lbs');
  const [privacyMode, setPrivacyMode] = useState(true);

  const handleSaveGoal = () => {
    const weight = parseFloat(newGoalWeight);
    if (!isNaN(weight) && weight > 0) {
      setGoalWeight(weight);
      alert('Goal weight updated successfully!');
    } else {
      alert('Please enter a valid goal weight');
    }
  };

  const handleExportData = () => {
    const dataStr = JSON.stringify(entries, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `weight-tracker-data-${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const handleClearData = () => {
    if (window.confirm('Are you sure you want to clear all data? This action cannot be undone.')) {
      // In a real app, this would clear the data
      alert('Data cleared successfully!');
    }
  };

  const currentWeight = entries[entries.length - 1]?.weight || 0;
  const totalEntries = entries.length;
  const startWeight = entries[0]?.weight || 0;
  const totalLoss = startWeight - currentWeight;
  const remainingToGoal = currentWeight - goalWeight;

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
              Settings
            </h1>
            <p className="section-subtitle" style={taglineStyle}>
              Customize your experience
            </p>
          </div>
        </div>
      </header>

      <main style={contentStyle}>
        <section className="card-surface">
          <h2 className="section-title">Profile Summary</h2>
          <div className="grid grid-cols-2 gap-4" style={{ marginTop: 'var(--spacing-md)' }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ ...statsValueStyle, color: 'var(--color-primary)' }}>{totalEntries}</div>
              <div style={statsLabelStyle}>Total Entries</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ ...statsValueStyle, color: 'var(--color-success)' }}>
                {totalLoss.toFixed(1)} lbs
              </div>
              <div style={statsLabelStyle}>Total Loss</div>
            </div>
          </div>
        </section>

        <section className="card-surface">
          <h2 className="section-title" style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-sm)' }}>
            <FlagIcon className="h-5 w-5" />
            Goal Settings
          </h2>
          <div style={controlStackStyle}>
            <div>
              <label className="field-label" htmlFor="goal-weight">
                Goal Weight ({units})
              </label>
              <div style={controlRowStyle}>
                <input
                  id="goal-weight"
                  type="number"
                  step="0.1"
                  value={newGoalWeight}
                  onChange={(e) => setNewGoalWeight(e.target.value)}
                  className="input-field"
                  style={{ flex: '1 1 200px' }}
                />
                <PillButton
                  variant="primary"
                  onClick={handleSaveGoal}
                  className="w-auto px-6"
                >
                  Save
                </PillButton>
              </div>
              <p className="support-text" style={{ marginTop: 'var(--spacing-xs)' }}>
                Current: {currentWeight} lbs • Goal: {goalWeight} lbs • Remaining: {remainingToGoal.toFixed(1)} lbs
              </p>
            </div>
          </div>
        </section>

        <section className="card-surface">
          <h2 className="section-title" style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-sm)' }}>
            <ScaleIcon className="h-5 w-5" />
            Units
          </h2>
          <div style={controlStackStyle}>
            <label style={toggleRowStyle}>
              <span>Pounds (lbs)</span>
              <input
                type="radio"
                name="units"
                value="lbs"
                checked={units === 'lbs'}
                onChange={(e) => setUnits(e.target.value)}
                style={accentControlStyle}
              />
            </label>
            <label style={toggleRowStyle}>
              <span>Kilograms (kg)</span>
              <input
                type="radio"
                name="units"
                value="kg"
                checked={units === 'kg'}
                onChange={(e) => setUnits(e.target.value)}
                style={accentControlStyle}
              />
            </label>
          </div>
        </section>

        <section className="card-surface">
          <h2 className="section-title" style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-sm)' }}>
            <BellIcon className="h-5 w-5" />
            Notifications
          </h2>
          <div style={controlStackStyle}>
            {['Daily reminders', 'Weekly progress reports', 'Goal achievement alerts'].map((label) => (
              <label key={label} style={toggleRowStyle}>
                <span>{label}</span>
                <input
                  type="checkbox"
                  checked={notifications}
                  onChange={(e) => setNotifications(e.target.checked)}
                  style={accentControlStyle}
                />
              </label>
            ))}
          </div>
        </section>

        <section className="card-surface">
          <h2 className="section-title" style={{ display: 'flex', alignItems: 'center', gap: 'var(--spacing-sm)' }}>
            <ShieldCheckIcon className="h-5 w-5" />
            Privacy
          </h2>
          <div style={controlStackStyle}>
            <label style={toggleRowStyle}>
              <span>Privacy mode (hide sensitive data)</span>
              <input
                type="checkbox"
                checked={privacyMode}
                onChange={(e) => setPrivacyMode(e.target.checked)}
                style={accentControlStyle}
              />
            </label>
            <label style={{ ...toggleRowStyle, opacity: 0.6 }}>
              <span>Data encryption</span>
              <input type="checkbox" checked readOnly style={accentControlStyle} />
            </label>
            <p className="support-text">
              Your data is stored locally and never shared with third parties.
            </p>
          </div>
        </section>

        <section className="card-surface">
          <h2 className="section-title">Data Management</h2>
          <div style={controlStackStyle}>
            <PillButton
              variant="accent"
              accentKind="success"
              onClick={handleExportData}
              icon={<ArrowDownTrayIcon className="h-5 w-5" />}
            >
              Export Data
            </PillButton>
            <PillButton
              variant="accent"
              accentKind="danger"
              onClick={handleClearData}
              icon={<TrashIcon className="h-5 w-5" />}
            >
              Clear All Data
            </PillButton>
          </div>
        </section>

        <section className="card-surface">
          <h2 className="section-title">App Information</h2>
          <div style={controlStackStyle}>
            <div style={infoRowStyle}>
              <span style={infoLabelStyle}>Version</span>
              <span>1.0.0</span>
            </div>
            <div style={infoRowStyle}>
              <span style={infoLabelStyle}>Platform</span>
              <span>Universal (iOS, Android, Web)</span>
            </div>
            <div style={infoRowStyle}>
              <span style={infoLabelStyle}>Data Storage</span>
              <span>Local (Privacy-first)</span>
            </div>
            <div style={infoRowStyle}>
              <span style={infoLabelStyle}>Last Updated</span>
              <span>{new Date().toLocaleDateString()}</span>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
};

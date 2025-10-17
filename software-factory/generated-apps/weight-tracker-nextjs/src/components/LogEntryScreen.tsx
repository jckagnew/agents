'use client';

import type { CSSProperties } from 'react';
import React, { useState } from 'react';
import { useWeight } from '../context/WeightContext';
import { PillButton } from './design-system';
import {
  ArrowLeftIcon,
  CheckIcon,
  CalendarIcon,
  ScaleIcon,
  HeartIcon,
} from '@heroicons/react/24/outline';

interface LogEntryScreenProps {
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

const quickActionsGridStyle: CSSProperties = {
  display: 'grid',
  gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))',
  gap: 'var(--spacing-md)',
};

const quickActionStyles: Record<
  'down' | 'same' | 'up',
  CSSProperties
> = {
  down: {
    background: 'var(--color-tintGreen)',
    color: 'var(--color-success)',
    border: '1px solid rgba(15, 157, 88, 0.24)',
  },
  same: {
    background: 'var(--color-tintBlue)',
    color: 'var(--color-primary)',
    border: '1px solid rgba(66, 133, 244, 0.24)',
  },
  up: {
    background: 'var(--color-tintYellow)',
    color: 'var(--color-warning)',
    border: '1px solid rgba(251, 188, 4, 0.24)',
  },
};

const quickActionLabelStyle: CSSProperties = {
  fontSize: 'var(--font-size-small)',
  fontWeight: 600,
};

const formSectionStyle: CSSProperties = {
  display: 'flex',
  flexDirection: 'column',
  gap: 'var(--spacing-lg)',
};

const actionsRowStyle: CSSProperties = {
  display: 'flex',
  gap: 'var(--spacing-md)',
  flexWrap: 'wrap',
};

const statsValueStyle: CSSProperties = {
  fontSize: 'var(--font-size-h3)',
  fontWeight: 700,
};

const statsLabelStyle: CSSProperties = {
  fontSize: 'var(--font-size-small)',
  color: 'var(--color-text-secondary)',
};

export const LogEntryScreen: React.FC<LogEntryScreenProps> = ({ onNavigate }) => {
  const { addEntry, currentWeight, currentBodyFat } = useWeight();
  const [weight, setWeight] = useState(currentWeight.toString());
  const [bodyFat, setBodyFat] = useState(currentBodyFat.toString());
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const [notes, setNotes] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);

    try {
      const weightNum = parseFloat(weight);
      const bodyFatNum = parseFloat(bodyFat);

      if (isNaN(weightNum) || isNaN(bodyFatNum)) {
        alert('Please enter valid numbers for weight and body fat');
        return;
      }

      if (weightNum <= 0 || bodyFatNum < 0 || bodyFatNum > 100) {
        alert('Please enter realistic values for weight and body fat');
        return;
      }

      addEntry({
        date,
        weight: weightNum,
        bodyFat: bodyFatNum,
        notes: notes.trim() || undefined,
      });

      // Show success message
      alert('Weight entry logged successfully!');
      
      // Navigate back to dashboard
      onNavigate('dashboard');
    } catch {
      alert('Error logging entry. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleQuickEntry = (type: 'same' | 'up' | 'down') => {
    const currentWeightNum = parseFloat(weight) || currentWeight;
    let newWeight = currentWeightNum;

    switch (type) {
      case 'up':
        newWeight = currentWeightNum + 0.5;
        break;
      case 'down':
        newWeight = currentWeightNum - 0.5;
        break;
      default:
        newWeight = currentWeightNum;
    }

    setWeight(newWeight.toString());
  };

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
              Log Weight Entry
            </h1>
            <p className="section-subtitle" style={taglineStyle}>
              Track your progress
            </p>
          </div>
        </div>
      </header>

      <main style={contentStyle}>
        <section className="card-surface card-surface--summary">
          <h2 className="section-title">Quick Entry</h2>
          <div style={quickActionsGridStyle}>
            {([
              { key: 'down', icon: '📉', label: '-0.5 lbs' },
              { key: 'same', icon: '➡️', label: 'Same' },
              { key: 'up', icon: '📈', label: '+0.5 lbs' },
            ] as const).map(({ key, icon, label }) => (
              <button
                key={key}
                type="button"
                onClick={() => handleQuickEntry(key)}
                className="quick-action"
                style={quickActionStyles[key]}
              >
                <span className="quick-action__icon" role="img" aria-label={label}>
                  {icon}
                </span>
                <span className="quick-action__label" style={quickActionLabelStyle}>
                  {label}
                </span>
              </button>
            ))}
          </div>
        </section>

        <form onSubmit={handleSubmit} style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-xl)' }}>
          <section className="card-surface">
            <h2 className="section-title">Detailed Entry</h2>
            <div style={formSectionStyle}>
              <div>
                <label className="field-label" htmlFor="entry-date">
                  <CalendarIcon className="h-4 w-4" />
                  Date
                </label>
                <input
                  id="entry-date"
                  type="date"
                  value={date}
                  onChange={(e) => setDate(e.target.value)}
                  className="input-field"
                  required
                />
              </div>

              <div>
                <label className="field-label" htmlFor="entry-weight">
                  <ScaleIcon className="h-4 w-4" />
                  Weight (lbs)
                </label>
                <input
                  id="entry-weight"
                  type="number"
                  step="0.1"
                  value={weight}
                  onChange={(e) => setWeight(e.target.value)}
                  placeholder="Enter your weight"
                  className="input-field"
                  required
                />
              </div>

              <div>
                <label className="field-label" htmlFor="entry-body-fat">
                  <HeartIcon className="h-4 w-4" />
                  Body Fat Percentage
                </label>
                <input
                  id="entry-body-fat"
                  type="number"
                  step="0.1"
                  value={bodyFat}
                  onChange={(e) => setBodyFat(e.target.value)}
                  placeholder="Enter body fat %"
                  className="input-field"
                  required
                />
              </div>

              <div>
                <label className="field-label" htmlFor="entry-notes">
                  Notes (Optional)
                </label>
                <textarea
                  id="entry-notes"
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  placeholder="Add any notes about your measurement..."
                  className="input-field"
                  rows={3}
                />
              </div>
            </div>
          </section>

          <div style={actionsRowStyle}>
            <PillButton
              variant="tertiary"
              onClick={() => onNavigate('dashboard')}
              className="flex-1"
            >
              Cancel
            </PillButton>
            <PillButton
              type="submit"
              variant="primary"
              disabled={isSubmitting}
              className="flex-1"
              icon={isSubmitting ? <div className="spinner" /> : <CheckIcon className="h-5 w-5" />}
            >
              {isSubmitting ? 'Logging...' : 'Log Entry'}
            </PillButton>
          </div>
        </form>

        <section className="card-surface">
          <h3 className="section-title">Current Stats</h3>
          <div className="grid grid-cols-2 gap-4" style={{ marginTop: 'var(--spacing-md)' }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ ...statsValueStyle, color: 'var(--color-primary)' }}>{currentWeight} lbs</div>
              <div style={statsLabelStyle}>Last Weight</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ ...statsValueStyle, color: 'var(--color-chart-secondary)' }}>{currentBodyFat}%</div>
              <div style={statsLabelStyle}>Last Body Fat</div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
};

'use client';

import type { CSSProperties } from 'react';
import React, { useState } from 'react';
import { useWeight } from '../context/WeightContext';
import {
  ArrowLeftIcon,
  MagnifyingGlassIcon,
  CalendarIcon,
  TrashIcon,
  PencilIcon,
} from '@heroicons/react/24/outline';

interface HistoryScreenProps {
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

const searchWrapperStyle: CSSProperties = {
  position: 'relative',
};

const searchIconStyle: CSSProperties = {
  position: 'absolute',
  top: '50%',
  left: 'var(--spacing-lg)',
  transform: 'translateY(-50%)',
  color: 'var(--color-text-muted)',
};

const entryMetaStyle: CSSProperties = {
  display: 'flex',
  flexWrap: 'wrap',
  gap: 'var(--spacing-sm)',
  alignItems: 'center',
  color: 'var(--color-text-secondary)',
  fontSize: 'var(--font-size-small)',
};

const entryWeightStyle: CSSProperties = {
  fontSize: 'var(--font-size-h2)',
  fontWeight: 700,
  color: 'var(--color-primary)',
};

const entryDeltaStyle: CSSProperties = {
  fontSize: 'var(--font-size-small)',
  fontWeight: 600,
};

const emptyStateStyle: CSSProperties = {
  textAlign: 'center',
  padding: 'var(--spacing-4xl)',
  color: 'var(--color-text-secondary)',
};

const calendarIconStyle: CSSProperties = {
  height: '3rem',
  width: '3rem',
  margin: '0 auto var(--spacing-md)',
  color: 'var(--color-text-muted)',
};

const statsValueStyle: CSSProperties = {
  fontSize: 'var(--font-size-h3)',
  fontWeight: 700,
};

const statsLabelStyle: CSSProperties = {
  fontSize: 'var(--font-size-small)',
  color: 'var(--color-text-secondary)',
};

export const HistoryScreen: React.FC<HistoryScreenProps> = ({ onNavigate }) => {
  const { entries, deleteEntry } = useWeight();
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredEntries, setFilteredEntries] = useState(entries);

  React.useEffect(() => {
    const filtered = entries.filter(entry => 
      entry.date.toLowerCase().includes(searchTerm.toLowerCase()) ||
      entry.weight.toString().includes(searchTerm) ||
      entry.bodyFat.toString().includes(searchTerm)
    );
    setFilteredEntries(filtered);
  }, [searchTerm, entries]);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { 
      weekday: 'short', 
      month: 'short', 
      day: 'numeric',
      year: 'numeric'
    });
  };

  const handleDelete = (id: string) => {
    if (window.confirm('Are you sure you want to delete this entry?')) {
      deleteEntry(id);
    }
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
              Weight History
            </h1>
            <p className="section-subtitle" style={taglineStyle}>
              {entries.length} entries captured
            </p>
          </div>
        </div>
      </header>

      <main style={contentStyle}>
        <section className="card-surface">
          <h2 className="section-title">Search Your History</h2>
          <div style={searchWrapperStyle}>
            <MagnifyingGlassIcon className="h-5 w-5" style={searchIconStyle} />
            <input
              type="text"
              placeholder="Search entries by date, weight, or body fat..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="input-field"
              style={{ paddingLeft: 'calc(var(--spacing-xl) + var(--spacing-lg))' }}
            />
          </div>
        </section>

        <section>
          <div className="card-list">
            <div className="card-list__header">
              <h2 className="section-title" style={{ marginBottom: 'var(--spacing-xs)' }}>
                Weight Entries
              </h2>
              <p className="support-text">
                Showing {filteredEntries.length} of {entries.length} entries
              </p>
            </div>
            {filteredEntries.length === 0 ? (
              <div style={emptyStateStyle}>
                <CalendarIcon style={calendarIconStyle} />
                <p style={{ fontWeight: 600, marginBottom: 'var(--spacing-xs)' }}>No entries found</p>
                <p className="support-text">Try adjusting your search terms</p>
              </div>
            ) : (
              filteredEntries.map((entry, index) => {
                const previous = index > 0 ? filteredEntries[index - 1] : undefined;
                const delta = previous ? entry.weight - previous.weight : 0;
                const deltaColor =
                  delta > 0 ? 'var(--color-error)' : delta < 0 ? 'var(--color-success)' : 'var(--color-text-muted)';
                const deltaPrefix = delta > 0 ? '+' : '';
                return (
                  <div key={entry.id} className="card-list__item" style={{ justifyContent: 'space-between' }}>
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ display: 'flex', gap: 'var(--spacing-lg)', alignItems: 'center', flexWrap: 'wrap' }}>
                        <div style={{ fontWeight: 600 }}>{formatDate(entry.date)}</div>
                        <div style={entryWeightStyle}>{entry.weight} lbs</div>
                        <div className="support-text" style={{ fontWeight: 600 }}>
                          {entry.bodyFat}% BF
                        </div>
                      </div>
                      {entry.notes && (
                        <p className="support-text" style={{ marginTop: 'var(--spacing-xs)' }}>
                          {entry.notes}
                        </p>
                      )}
                      {previous && (
                        <div style={{ ...entryMetaStyle, marginTop: 'var(--spacing-xs)' }}>
                          <span style={{ ...entryDeltaStyle, color: deltaColor }}>
                            {deltaPrefix}
                            {Math.abs(delta).toFixed(1)} lbs
                          </span>
                          <span className="muted">from previous entry</span>
                        </div>
                      )}
                    </div>
                    <div style={{ display: 'flex', gap: 'var(--spacing-sm)' }}>
                      <button
                        type="button"
                        onClick={() => onNavigate('log-entry')}
                        title="Edit entry"
                        className="icon-button--ghost"
                      >
                        <PencilIcon className="h-4 w-4" />
                      </button>
                      <button
                        type="button"
                        onClick={() => handleDelete(entry.id)}
                        title="Delete entry"
                        className="icon-button--ghost icon-button--danger"
                      >
                        <TrashIcon className="h-4 w-4" />
                      </button>
                    </div>
                  </div>
                );
              })
            )}
          </div>
        </section>

        <section className="card-surface">
          <h3 className="section-title">Summary Statistics</h3>
          <div className="grid grid-cols-2 gap-4" style={{ marginTop: 'var(--spacing-md)' }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ ...statsValueStyle, color: 'var(--color-primary)' }}>
                {filteredEntries.length > 0 ? filteredEntries[0].weight : 0} lbs
              </div>
              <div style={statsLabelStyle}>Starting Weight</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ ...statsValueStyle, color: 'var(--color-success)' }}>
                {filteredEntries.length > 0 ? filteredEntries[filteredEntries.length - 1].weight : 0} lbs
              </div>
              <div style={statsLabelStyle}>Current Weight</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ ...statsValueStyle, color: 'var(--color-chart-secondary)' }}>
                {filteredEntries.length > 1
                  ? (filteredEntries[0].weight - filteredEntries[filteredEntries.length - 1].weight).toFixed(1)
                  : 0}{' '}
                lbs
              </div>
              <div style={statsLabelStyle}>Total Change</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ ...statsValueStyle, color: 'var(--color-warning)' }}>
                {filteredEntries.length > 1
                  ? (
                      (filteredEntries[0].weight - filteredEntries[filteredEntries.length - 1].weight) /
                      Math.max(1, filteredEntries.length - 1)
                    ).toFixed(1)
                  : 0}{' '}
                lbs
              </div>
              <div style={statsLabelStyle}>Average Change</div>
            </div>
          </div>
        </section>
      </main>
    </div>
  );
};

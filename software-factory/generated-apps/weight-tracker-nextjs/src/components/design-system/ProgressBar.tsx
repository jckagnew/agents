'use client';

import React from 'react';

export type ProgressBarVariant = 'standard' | 'success' | 'warning' | 'error';

interface ProgressBarProps {
  value: number;
  max?: number;
  variant?: ProgressBarVariant;
  showLabel?: boolean;
  label?: string;
  className?: string;
  ariaLabel?: string;
}

const variantColors: Record<ProgressBarVariant, { bg: string; fill: string }> = {
  standard: {
    bg: 'bg-gray-200',
    fill: 'bg-gradient-to-r from-blue-500 to-green-500',
  },
  success: {
    bg: 'bg-gray-200',
    fill: 'bg-green-500',
  },
  warning: {
    bg: 'bg-gray-200',
    fill: 'bg-yellow-500',
  },
  error: {
    bg: 'bg-gray-200',
    fill: 'bg-red-500',
  },
};

export function ProgressBar({
  value,
  max = 100,
  variant = 'standard',
  showLabel = true,
  label,
  className = '',
  ariaLabel,
}: ProgressBarProps) {
  const percentage = Math.min(Math.max((value / max) * 100, 0), 100);
  const colors = variantColors[variant];
  const displayLabel = label || `${Math.round(percentage)}%`;

  return (
    <div className={`w-full ${className}`}>
      <div className="flex items-center justify-between mb-1">
        <span className="text-sm font-medium text-gray-700">{displayLabel}</span>
        {showLabel && <span className="text-sm text-gray-600">{Math.round(percentage)}%</span>}
      </div>
      <div
        className={`h-2.5 rounded-full overflow-hidden ${colors.bg}`}
        role="progressbar"
        aria-valuenow={value}
        aria-valuemin={0}
        aria-valuemax={max}
        aria-label={ariaLabel || `Progress: ${percentage}%`}
        tabIndex={0}
      >
        <div
          className={`h-full transition-all duration-500 ease-out ${colors.fill}`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}

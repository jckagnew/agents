import React from 'react'

interface MetricCardProps {
  title: string
  value: string | number
  subtitle?: string
  trend?: 'up' | 'down' | 'neutral'
  variant?: 'default' | 'summary' | 'chart' | 'compact'
  className?: string
  children?: React.ReactNode
}

export function MetricCard({ 
  title, 
  value, 
  subtitle, 
  trend, 
  variant = 'default',
  className = '',
  children 
}: MetricCardProps) {
  const baseClasses = 'card-surface'
  const variantClasses = {
    default: '',
    summary: 'card-surface--summary',
    chart: 'card-surface--chart',
    compact: 'card-surface--compact'
  }
  
  const cardClasses = `${baseClasses} ${variantClasses[variant]} ${className}`.trim()

  return (
    <div className={cardClasses}>
      <h3 className="section-title">{title}</h3>
      <div style={{ textAlign: 'center' }}>
        <div 
          style={{ 
            fontSize: 'var(--font-size-h1)',
            fontWeight: 700,
            color: 'var(--color-primary)',
            marginBottom: 'var(--spacing-sm)'
          }}
        >
          {value}
        </div>
        {subtitle && (
          <div 
            style={{ 
              color: 'var(--color-text-secondary)',
              fontSize: 'var(--font-size-small)',
              marginBottom: 'var(--spacing-xs)'
            }}
          >
            {subtitle}
          </div>
        )}
        {trend && (
          <div 
            className={`pill-badge ${trend === 'up' ? 'trend-up' : trend === 'down' ? 'trend-down' : 'trend-neutral'}`}
            style={{ 
              display: 'inline-flex',
              alignItems: 'center',
              gap: 'var(--spacing-xs)',
              padding: 'var(--spacing-sm) var(--spacing-md)',
              borderRadius: 'var(--radius-full)',
              fontSize: 'var(--font-size-small)',
              fontWeight: 600,
              background: trend === 'up' 
                ? 'rgba(15, 157, 88, 0.12)' 
                : trend === 'down' 
                ? 'rgba(239, 68, 68, 0.12)' 
                : 'rgba(107, 114, 128, 0.12)',
              color: trend === 'up' 
                ? 'var(--color-success)' 
                : trend === 'down' 
                ? 'var(--color-error)' 
                : 'var(--color-text-secondary)'
            }}
          >
            {trend === 'up' && '↗'}
            {trend === 'down' && '↘'}
            {trend === 'neutral' && '→'}
          </div>
        )}
      </div>
      {children}
    </div>
  )
}

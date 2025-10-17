import React from 'react'

type Variant = 'primary' | 'secondary' | 'tertiary' | 'accent' | 'ghost'

interface PillButtonProps {
  children: React.ReactNode
  variant?: Variant
  accentKind?: 'success' | 'danger'
  onClick?: () => void
  type?: 'button' | 'submit' | 'reset'
  disabled?: boolean
  className?: string
  icon?: React.ReactNode
}

export function PillButton({
  children,
  variant = 'primary',
  accentKind,
  onClick,
  type = 'button',
  disabled = false,
  className = '',
  icon,
}: PillButtonProps) {
  const variantClass =
    variant === 'primary' ? 'button-primary' :
    variant === 'secondary' ? 'button-secondary' :
    variant === 'tertiary' ? 'button-tertiary' :
    variant === 'ghost' ? 'icon-button--ghost' :
    // accent
    accentKind === 'success' ? 'button-accent button-accent--success' :
    accentKind === 'danger' ? 'button-accent button-accent--danger' :
    'button-accent'

  const classes = [variantClass, className].filter(Boolean).join(' ').trim()

  return (
    <button type={type} onClick={onClick} disabled={disabled} className={classes}>
      {icon && <span className="button-icon">{icon}</span>}
      <span>{children}</span>
    </button>
  )
}
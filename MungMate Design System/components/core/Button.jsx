import React from 'react';

/**
 * MungMate primary button. Coral or coral→orange gradient, rounded 16px,
 * warm coral-tinted shadow, tactile shrink on press.
 */
export function Button({
  children,
  variant = 'primary',   // primary | gradient | secondary | ghost
  size = 'md',           // sm | md | lg
  full = false,
  icon = null,           // leading content (emoji or <i data-lucide>)
  disabled = false,
  onClick,
  type = 'button',
  style = {},
  ...rest
}) {
  const sizes = {
    sm: { padding: '8px 14px', fontSize: '13.5px', radius: 'var(--radius-md)', gap: '6px' },
    md: { padding: '12px 20px', fontSize: 'var(--text-base)', radius: 'var(--radius-lg)', gap: '8px' },
    lg: { padding: '16px 26px', fontSize: 'var(--text-lg)', radius: 'var(--radius-lg)', gap: '9px' },
  };
  const s = sizes[size] || sizes.md;

  const variants = {
    primary: {
      background: 'var(--coral-600)', color: 'var(--text-on-brand)',
      border: '1px solid transparent', boxShadow: 'var(--shadow-brand)',
    },
    gradient: {
      background: 'var(--brand-gradient)', color: 'var(--text-on-brand)',
      border: '1px solid transparent', boxShadow: 'var(--shadow-brand)',
    },
    secondary: {
      background: 'var(--white)', color: 'var(--text-strong)',
      border: '1px solid var(--border-strong)', boxShadow: 'var(--shadow-sm)',
    },
    ghost: {
      background: 'transparent', color: 'var(--brand)',
      border: '1px solid transparent', boxShadow: 'none',
    },
  };
  const v = variants[variant] || variants.primary;

  const [pressed, setPressed] = React.useState(false);
  const [hover, setHover] = React.useState(false);

  return (
    <button
      type={type}
      disabled={disabled}
      onClick={onClick}
      onMouseDown={() => setPressed(true)}
      onMouseUp={() => setPressed(false)}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => { setHover(false); setPressed(false); }}
      style={{
        display: full ? 'flex' : 'inline-flex',
        width: full ? '100%' : 'auto',
        alignItems: 'center', justifyContent: 'center', gap: s.gap,
        fontFamily: 'var(--font-sans)', fontWeight: 800, fontSize: s.fontSize,
        lineHeight: 1, padding: s.padding, borderRadius: s.radius,
        cursor: disabled ? 'not-allowed' : 'pointer',
        opacity: disabled ? 0.45 : 1,
        transform: pressed ? 'scale(0.97)' : (hover && !disabled ? 'translateY(-1px)' : 'none'),
        boxShadow: hover && !disabled && (variant === 'primary' || variant === 'gradient')
          ? 'var(--shadow-brand-hover)' : v.boxShadow,
        filter: hover && !disabled && variant === 'secondary' ? 'brightness(0.98)' : 'none',
        transition: 'transform var(--dur-fast) var(--ease-snap), box-shadow var(--dur-base) var(--ease-out)',
        ...v, ...style,
      }}
      {...rest}
    >
      {icon != null && <span style={{ display: 'inline-flex', fontSize: '1.1em' }}>{icon}</span>}
      {children}
    </button>
  );
}

import React from 'react';

/**
 * Selectable chip — filter/option tags. Pill, warm border, coral when selected.
 */
export function Chip({ children, selected = false, icon = null, onClick, style = {} }) {
  const [hover, setHover] = React.useState(false);
  return (
    <button
      type="button"
      onClick={onClick}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        display: 'inline-flex', alignItems: 'center', gap: '6px',
        fontFamily: 'var(--font-sans)', fontWeight: 700, fontSize: 'var(--text-sm)',
        lineHeight: 1, padding: '9px 15px', borderRadius: 'var(--radius-pill)',
        cursor: 'pointer',
        color: selected ? 'var(--brand)' : 'var(--text-body)',
        background: selected ? 'var(--coral-tint)' : 'var(--white)',
        border: selected ? '1.5px solid var(--coral-500)' : '1.5px solid var(--border-card)',
        boxShadow: hover && !selected ? 'var(--shadow-sm)' : 'none',
        transition: 'all var(--dur-fast) var(--ease-out)',
        ...style,
      }}
    >
      {icon != null && <span>{icon}</span>}
      {children}
    </button>
  );
}

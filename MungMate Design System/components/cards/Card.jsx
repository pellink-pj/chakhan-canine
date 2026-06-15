import React from 'react';

/**
 * Base surface card — white on cream, 20px radius, hairline warm border
 * plus soft coral-tinted shadow. Lifts slightly on hover when interactive.
 */
export function Card({ children, padding = 'var(--space-6)', interactive = false, onClick, style = {} }) {
  const [hover, setHover] = React.useState(false);
  return (
    <div
      onClick={onClick}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => setHover(false)}
      style={{
        background: 'var(--bg-elevated)',
        border: '1px solid var(--border-card)',
        borderRadius: 'var(--radius-xl)',
        boxShadow: interactive && hover ? 'var(--shadow-lg)' : 'var(--shadow-card)',
        padding,
        cursor: interactive ? 'pointer' : 'default',
        transform: interactive && hover ? 'translateY(-2px)' : 'none',
        transition: 'transform var(--dur-base) var(--ease-out), box-shadow var(--dur-base) var(--ease-out)',
        ...style,
      }}
    >
      {children}
    </div>
  );
}

import React from 'react';

/**
 * Big tap-target answer card for the readiness diagnostic (후킹 질문).
 * Full-width, generous hit area, coral selection state, gentle press shrink.
 */
export function ChoiceCard({ icon, label, sub, selected = false, onClick, style = {} }) {
  const [hover, setHover] = React.useState(false);
  const [pressed, setPressed] = React.useState(false);
  return (
    <button
      type="button"
      onClick={onClick}
      onMouseDown={() => setPressed(true)}
      onMouseUp={() => setPressed(false)}
      onMouseEnter={() => setHover(true)}
      onMouseLeave={() => { setHover(false); setPressed(false); }}
      style={{
        display: 'flex', alignItems: 'center', gap: '14px', width: '100%', textAlign: 'left',
        fontFamily: 'var(--font-sans)', cursor: 'pointer',
        padding: '18px 20px', minHeight: '64px', borderRadius: 'var(--radius-lg)',
        background: selected ? 'var(--coral-tint)' : 'var(--white)',
        border: selected ? '2px solid var(--coral-500)' : '2px solid var(--border-card)',
        boxShadow: selected ? 'var(--shadow-brand)' : (hover ? 'var(--shadow-card)' : 'var(--shadow-sm)'),
        transform: pressed ? 'scale(0.985)' : 'none',
        transition: 'transform var(--dur-fast) var(--ease-snap), box-shadow var(--dur-base) var(--ease-out), border-color var(--dur-fast) var(--ease-out)',
        ...style,
      }}
    >
      {icon != null && (
        <span style={{
          fontSize: '24px', width: '44px', height: '44px', flexShrink: 0,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          borderRadius: 'var(--radius-md)',
          background: selected ? 'var(--white)' : 'var(--mint-100)',
        }}>{icon}</span>
      )}
      <span style={{ display: 'flex', flexDirection: 'column', gap: '3px', minWidth: 0 }}>
        <span style={{
          fontWeight: 800, fontSize: 'var(--text-lg)',
          color: selected ? 'var(--brand-strong)' : 'var(--text-strong)',
        }}>{label}</span>
        {sub && <span style={{ fontWeight: 400, fontSize: 'var(--text-sm)', color: 'var(--text-muted)' }}>{sub}</span>}
      </span>
      <span style={{
        marginLeft: 'auto', flexShrink: 0,
        width: '22px', height: '22px', borderRadius: '50%',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        border: selected ? 'none' : '2px solid var(--border-strong)',
        background: selected ? 'var(--coral-600)' : 'transparent',
        color: '#fff', fontSize: '13px', fontWeight: 900,
      }}>{selected ? '✓' : ''}</span>
    </button>
  );
}

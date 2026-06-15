import React from 'react';

/**
 * 1–5 trait meter row (AKC-style). Label + 5 dots filled to `score`, with the
 * plain-Korean scale word. Filled dots use the brand gradient; high scores on
 * "negative" traits can be flagged caution via the `tone` prop.
 */
export function TraitMeter({ label, score = 3, max = 5, scaleWord, tone = 'brand', style = {} }) {
  const fill = {
    brand:   'var(--coral-500)',
    good:    'var(--good-line)',
    hope:    'var(--hope-line)',
    caution: 'var(--caution-line)',
  }[tone] || 'var(--coral-500)';

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '12px', ...style }}>
      <div style={{
        fontFamily: 'var(--font-sans)', fontWeight: 700, fontSize: 'var(--text-sm)',
        color: 'var(--text-body)', width: '92px', flexShrink: 0,
      }}>{label}</div>
      <div style={{ display: 'flex', gap: '5px', flexShrink: 0 }}>
        {Array.from({ length: max }).map((_, i) => (
          <span key={i} style={{
            width: '13px', height: '13px', borderRadius: '50%',
            background: i < score ? fill : 'var(--mint-200)',
            border: i < score ? 'none' : '1px solid var(--border-card)',
          }} />
        ))}
      </div>
      {scaleWord && <div style={{
        fontFamily: 'var(--font-sans)', fontWeight: 700, fontSize: 'var(--text-xs)',
        color: tone === 'brand' ? 'var(--text-muted)' : fill,
      }}>{scaleWord}</div>}
    </div>
  );
}

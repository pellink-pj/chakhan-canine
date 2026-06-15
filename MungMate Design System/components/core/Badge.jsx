import React from 'react';

/**
 * Small pill label. Tone-aware (good/hope/caution/brand/neutral/gold).
 * Used for trait tags, the 착한개 certification mark, popularity ranks.
 */
export function Badge({ children, tone = 'brand', icon = null, solid = false, style = {} }) {
  const tones = {
    brand:   { fg: 'var(--brand)',       bg: 'var(--coral-tint)',   solidBg: 'var(--coral-600)' },
    good:    { fg: 'var(--good-fg)',     bg: 'var(--good-tint)',    solidBg: 'var(--good-line)' },
    hope:    { fg: 'var(--hope-fg)',     bg: 'var(--hope-tint)',    solidBg: 'var(--hope-line)' },
    caution: { fg: 'var(--caution-fg)',  bg: 'var(--caution-tint)', solidBg: 'var(--caution-line)' },
    info:    { fg: 'var(--info-fg)',     bg: 'var(--info-tint)',    solidBg: 'var(--info-line)' },
    gold:    { fg: '#fff',               bg: 'var(--yellow-tint)',  solidBg: 'var(--rank-gold)' },
    neutral: { fg: 'var(--text-muted)',  bg: 'var(--mint-200)',     solidBg: 'var(--ink-600)' },
  };
  const t = tones[tone] || tones.brand;
  return (
    <span style={{
      display: 'inline-flex', alignItems: 'center', gap: '4px',
      fontFamily: 'var(--font-sans)', fontWeight: 800, fontSize: 'var(--text-xs)',
      lineHeight: 1, padding: '5px 10px', borderRadius: 'var(--radius-pill)',
      color: solid ? '#fff' : t.fg,
      background: solid ? t.solidBg : t.bg,
      ...style,
    }}>
      {icon != null && <span>{icon}</span>}
      {children}
    </span>
  );
}

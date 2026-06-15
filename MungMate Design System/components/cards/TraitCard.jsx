import React from 'react';

/**
 * The signature MungMate insight card. Renders one trait message in the
 * brand's hope-first voice: a headline + explanation, tinted and accented by
 * tone (good / hope / caution). Mirrors breed_messages.py output. The brand
 * uses no emoji — tone color + the left accent bar carry the meaning. An
 * optional `icon` (e.g. a Lucide node) may be passed but is not used by default.
 */
export function TraitCard({ icon, title, text, tone = 'hope', style = {} }) {
  const tones = {
    good:    { fg: 'var(--good-fg)',    line: 'var(--good-line)',    bg: 'var(--good-tint)' },
    hope:    { fg: 'var(--hope-fg)',    line: 'var(--hope-line)',    bg: 'var(--hope-tint)' },
    caution: { fg: 'var(--caution-fg)', line: 'var(--caution-line)', bg: 'var(--caution-tint)' },
  };
  const t = tones[tone] || tones.hope;
  const label = { good: '좋은 특성', hope: '훈련으로 극복 가능', caution: '신중히 고려' }[tone];

  return (
    <div style={{
      display: 'flex', gap: '13px',
      background: t.bg,
      border: '1px solid var(--border-card)',
      borderLeft: `4px solid ${t.line}`,
      borderRadius: 'var(--radius-xl)',
      padding: '15px 17px',
      ...style,
    }}>
      {icon != null && <div style={{ fontSize: '22px', lineHeight: 1.1, flexShrink: 0, color: t.fg }}>{icon}</div>}
      <div style={{ minWidth: 0 }}>
        <div style={{
          fontFamily: 'var(--font-sans)', fontWeight: 800, fontSize: '10.5px',
          textTransform: 'uppercase', letterSpacing: '0.05em', color: t.fg, marginBottom: '5px',
        }}>{label}</div>
        <div style={{
          fontFamily: 'var(--font-sans)', fontWeight: 800, fontSize: 'var(--text-lg)',
          color: 'var(--text-strong)', lineHeight: 'var(--lh-snug)', letterSpacing: 'var(--tracking-snug)',
        }}>{title}</div>
        {text && <div style={{
          fontFamily: 'var(--font-sans)', fontWeight: 400, fontSize: 'var(--text-sm)',
          color: 'var(--text-body)', lineHeight: 'var(--lh-body)', marginTop: '5px',
        }}>{text}</div>}
      </div>
    </div>
  );
}

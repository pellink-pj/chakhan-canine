/* MungMate app — shared chrome: Logo, TopBar, ProgressBar, PhoneFrame */

function Logo({ size = 26, light = false }) {
  const mark = Math.round(size * 1.55);
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: size * 0.42 }}>
      <div style={{
        width: mark, height: mark, borderRadius: mark * 0.3,
        background: light ? '#fff' : 'var(--brand-gradient)',
        color: light ? 'var(--brand)' : '#fff',
        display: 'flex', alignItems: 'center', justifyContent: 'center',
        fontWeight: 900, fontSize: mark * 0.48,
        boxShadow: light ? 'none' : 'var(--shadow-brand)', flexShrink: 0,
      }}>멍</div>
      <span style={{
        fontWeight: 900, fontSize: size, letterSpacing: '-0.02em',
        color: light ? '#fff' : 'var(--ink-900)',
      }}>멍메이트</span>
    </div>
  );
}

function TopBar({ onBack, title, right }) {
  return (
    <div style={{
      height: 56, flexShrink: 0, display: 'flex', alignItems: 'center', gap: 10,
      padding: '0 16px', background: 'var(--bg-app)',
      borderBottom: '1px solid var(--line-soft)', position: 'sticky', top: 0, zIndex: 5,
    }}>
      {onBack ? (
        <button onClick={onBack} aria-label="뒤로" style={{
          width: 36, height: 36, border: 'none', background: 'var(--white)',
          borderRadius: 'var(--radius-md)', cursor: 'pointer', fontSize: 18,
          color: 'var(--ink-700)', boxShadow: 'var(--shadow-sm)',
          display: 'flex', alignItems: 'center', justifyContent: 'center',
        }}>‹</button>
      ) : <Logo size={19} />}
      {title && <span style={{ fontWeight: 800, fontSize: 16, color: 'var(--ink-900)' }}>{title}</span>}
      <div style={{ marginLeft: 'auto' }}>{right}</div>
    </div>
  );
}

function ProgressBar({ step, total }) {
  return (
    <div style={{ display: 'flex', gap: 6, padding: '14px 20px 4px' }}>
      {Array.from({ length: total }).map((_, i) => (
        <div key={i} style={{
          flex: 1, height: 6, borderRadius: 999,
          background: i <= step ? 'var(--brand-gradient)' : 'var(--mint-200)',
          transition: 'background var(--dur-base) var(--ease-out)',
        }} />
      ))}
    </div>
  );
}

/* Mobile frame — centers the app in a soft device shell */
function PhoneFrame({ children }) {
  return (
    <div style={{
      width: 412, height: 844, background: 'var(--bg-app)',
      borderRadius: 38, overflow: 'hidden', position: 'relative',
      boxShadow: '0 30px 80px rgba(91,64,48,0.28), 0 0 0 10px #2B2018, 0 0 0 11px #00000022',
      display: 'flex', flexDirection: 'column',
    }}>
      {children}
    </div>
  );
}

/* Scroll region for a screen's body */
function ScreenBody({ children, style = {} }) {
  return (
    <div style={{ flex: 1, overflowY: 'auto', WebkitOverflowScrolling: 'touch', ...style }}>
      {children}
    </div>
  );
}

Object.assign(window, { Logo, TopBar, ProgressBar, PhoneFrame, ScreenBody });

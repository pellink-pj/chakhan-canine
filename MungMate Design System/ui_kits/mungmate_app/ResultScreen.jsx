/* MungMate app — Lifestyle match result. Ranked breed cards. */

function ResultScreen({ onBack, onOpen }) {
  const { Card, Badge } = window.MungMateDesignSystem_181714;
  const breeds = window.MM_DATA.breeds;

  return (
    <React.Fragment>
      <TopBar onBack={onBack} title="라이프스타일 매칭" />
      <ScreenBody>
        <div style={{ padding: '20px 24px 12px' }}>
          <Badge tone="good">진단 통과</Badge>
          <h2 style={{ fontSize: 22, fontWeight: 900, letterSpacing: '-0.02em', color: 'var(--ink-900)', margin: '12px 0 6px' }}>
            준비된 당신에게<br />어울리는 견종이에요
          </h2>
          <p style={{ fontSize: 14, lineHeight: 1.65, color: 'var(--text-muted)', margin: 0 }}>
            비용 · 산책 · 훈련 + 한국 시장 인기까지 통합 매칭한 결과예요.
          </p>
        </div>

        <div style={{ padding: '8px 18px 24px', display: 'flex', flexDirection: 'column', gap: 13 }}>
          {breeds.map((b) => (
            <Card key={b.id} interactive padding="0" onClick={() => onOpen(b.id)} style={{ overflow: 'hidden' }}>
              <div style={{ display: 'flex', gap: 14, padding: 16 }}>
                <div style={{
                  width: 64, height: 64, flexShrink: 0, borderRadius: 'var(--radius-lg)',
                  background: 'var(--brand-gradient)', border: 'none',
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  fontSize: 26, fontWeight: 800, color: '#fff',
                }}>{b.mono}</div>
                <div style={{ flex: 1, minWidth: 0 }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <span style={{ fontSize: 17, fontWeight: 900, color: 'var(--ink-900)' }}>{b.name}</span>
                    {b.founder && <Badge tone="brand" solid>창업자의 견종</Badge>}
                  </div>
                  <div style={{ fontSize: 12.5, color: 'var(--text-caption)', marginTop: 2 }}>{b.en} · {b.size}</div>
                  <div style={{ display: 'flex', gap: 6, marginTop: 9, flexWrap: 'wrap' }}>
                    <Badge tone="gold" solid>한국 인기 {b.rank}위</Badge>
                    <Badge tone="neutral">월 {b.costMonthly}</Badge>
                  </div>
                </div>
              </div>
              {/* Match bar */}
              <div style={{ padding: '0 16px 14px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 5 }}>
                  <span style={{ fontSize: 12, fontWeight: 700, color: 'var(--text-muted)' }}>매칭 점수</span>
                  <span style={{ fontSize: 15, fontWeight: 900, color: 'var(--brand)' }}>{b.match}%</span>
                </div>
                <div style={{ height: 8, borderRadius: 999, background: 'var(--mint-200)', overflow: 'hidden' }}>
                  <div style={{ width: b.match + '%', height: '100%', borderRadius: 999, background: 'var(--brand-gradient)' }} />
                </div>
              </div>
            </Card>
          ))}
        </div>
      </ScreenBody>
    </React.Fragment>
  );
}

window.ResultScreen = ResultScreen;

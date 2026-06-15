/* MungMate app — Intro / hero screen.
   "당신, 정말 준비됐나요?" → two big ChoiceCards. */

function IntroScreen({ onStart }) {
  const { Button, ChoiceCard, Badge } = window.MungMateDesignSystem_181714;
  const [answer, setAnswer] = React.useState(null);

  return (
    <React.Fragment>
      <TopBar right={<Badge tone="neutral">베타</Badge>} />
      <ScreenBody>
        {/* Hero */}
        <div style={{ padding: '34px 24px 20px', background: 'var(--brand-gradient-soft)' }}>
          <Badge tone="brand">한국형 책임 입양</Badge>
          <h1 style={{
            fontSize: 34, fontWeight: 900, lineHeight: 1.2, letterSpacing: '-0.03em',
            color: 'var(--ink-900)', margin: '16px 0 10px',
          }}>
            당신,<br />정말 <span style={{ color: 'var(--brand)' }}>준비됐나요?</span>
          </h1>
          <p style={{ fontSize: 15, lineHeight: 1.7, color: 'var(--text-body)', margin: 0 }}>
            귀여움만 보고 데려오기 전에. 293개 견종 데이터로,
            당신의 라이프스타일에 맞는 강아지를 찾아드려요.
          </p>
        </div>

        {/* Shock stat */}
        <div style={{ padding: '24px 24px 8px' }}>
          <div style={{
            background: 'var(--coral-tint)', border: '1px solid var(--coral-100)',
            borderLeft: '4px solid var(--coral-600)',
            borderRadius: 'var(--radius-xl)', padding: '16px 18px',
          }}>
            <div style={{ fontSize: 13, color: 'var(--caution-fg)', fontWeight: 700 }}>매년 한국에서</div>
            <div style={{ fontSize: 15, color: 'var(--ink-900)', fontWeight: 700 }}>
              <b style={{ fontSize: 28, fontWeight: 900, color: 'var(--brand)' }}>11만 마리</b>가 유기됩니다
            </div>
          </div>
        </div>

        {/* Question */}
        <div style={{ padding: '20px 24px 16px' }}>
          <p style={{ fontSize: 18, fontWeight: 800, color: 'var(--ink-900)', margin: '0 0 14px', letterSpacing: '-0.02em' }}>
            마음에 둔 강아지가 있으세요?
          </p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 11 }}>
            <ChoiceCard label="네, 있어요" sub="이 견종이 나랑 맞는지 확인할래요"
              selected={answer === 'yes'} onClick={() => setAnswer('yes')} />
            <ChoiceCard label="잘 모르겠어요" sub="라이프스타일에 맞는 견종을 추천받을래요"
              selected={answer === 'no'} onClick={() => setAnswer('no')} />
          </div>
        </div>
        <div style={{ height: 96 }} />
      </ScreenBody>

      {/* Sticky CTA */}
      <div style={{
        flexShrink: 0, padding: '14px 20px 22px', background: 'var(--bg-app)',
        borderTop: '1px solid var(--line-soft)',
      }}>
        <Button variant="gradient" size="lg" full
          disabled={!answer} onClick={onStart}>
          준비도 진단 시작하기
        </Button>
      </div>
    </React.Fragment>
  );
}

window.IntroScreen = IntroScreen;

/* MungMate app — Readiness diagnostic (후킹 질문).
   Provocative question → answer → data "truth" reveal → next. */

function DiagnosticScreen({ onBack, onDone }) {
  const { Button, ChoiceCard } = window.MungMateDesignSystem_181714;
  const questions = window.MM_DATA.diagnostic;
  const [step, setStep] = React.useState(0);
  const [answer, setAnswer] = React.useState(null);
  const [revealed, setRevealed] = React.useState(false);
  const q = questions[step];

  function next() {
    if (!revealed) { setRevealed(true); return; }
    if (step + 1 < questions.length) {
      setStep(step + 1); setAnswer(null); setRevealed(false);
    } else { onDone(); }
  }

  return (
    <React.Fragment>
      <TopBar onBack={onBack} title="입양 준비도 진단" />
      <ProgressBar step={step} total={questions.length} />
      <ScreenBody>
        <div style={{ padding: '18px 24px 8px' }}>
          <div style={{ fontSize: 12, fontWeight: 800, color: 'var(--brand)', letterSpacing: '0.04em', marginBottom: 10 }}>
            Q{step + 1} / {questions.length}
          </div>
          <h2 style={{ fontSize: 23, fontWeight: 900, lineHeight: 1.35, letterSpacing: '-0.02em', color: 'var(--ink-900)', margin: '0 0 6px' }}>
            {q.q}
          </h2>
          <p style={{ fontSize: 13.5, color: 'var(--text-muted)', margin: 0 }}>{q.hint}</p>
        </div>

        <div style={{ padding: '16px 24px', display: 'flex', flexDirection: 'column', gap: 11 }}>
          {q.options.map((o) => (
            <ChoiceCard key={o.value} icon={o.icon} label={o.label}
              selected={answer === o.value}
              onClick={() => { if (!revealed) setAnswer(o.value); }} />
          ))}
        </div>

        {/* Data truth reveal */}
        {revealed && (
          <div style={{ padding: '0 24px 8px', animation: 'mmRise 0.4s var(--ease-out) both' }}>
            <div style={{
              background: 'var(--hope-tint)',
              border: '1px solid var(--border-card)', borderLeft: '4px solid var(--hope-line)',
              borderRadius: 'var(--radius-xl)', padding: '15px 17px',
            }}>
              <div style={{ fontSize: 11, fontWeight: 800, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--hope-fg)', marginBottom: 5 }}>
                데이터가 말하는 진실
              </div>
              <p style={{ fontSize: 14.5, lineHeight: 1.65, color: 'var(--ink-900)', margin: 0, fontWeight: 500 }}>{q.truth}</p>
            </div>
          </div>
        )}
        <div style={{ height: 100 }} />
      </ScreenBody>

      <div style={{ flexShrink: 0, padding: '14px 20px 22px', background: 'var(--bg-app)', borderTop: '1px solid var(--line-soft)' }}>
        <Button variant={revealed ? 'gradient' : 'primary'} size="lg" full
          disabled={!answer}
          onClick={next}>
          {!revealed ? '진실 확인하기' : (step + 1 < questions.length ? '다음 질문' : '내 견종 매칭 보기')}
        </Button>
      </div>
    </React.Fragment>
  );
}

window.DiagnosticScreen = DiagnosticScreen;

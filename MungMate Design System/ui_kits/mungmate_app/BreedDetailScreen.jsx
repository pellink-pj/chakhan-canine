/* MungMate app — Breed detail. Traits, hope-first messages, founder testimony,
   착한개 certification CTA. The brand's voice in full — no emoji; tone color,
   accent bars and a monogram avatar carry the visual weight. */

function BreedDetailScreen({ breedId, onBack }) {
  const { Card, TraitCard, TraitMeter, Badge, Button } = window.MungMateDesignSystem_181714;
  const b = window.MM_DATA.breeds.find((x) => x.id === breedId) || window.MM_DATA.breeds[0];

  return (
    <React.Fragment>
      <TopBar onBack={onBack} title={b.name}
        right={<button aria-label="저장" style={{ height: 32, padding: '0 12px', border: '1px solid var(--border-strong)', background: 'var(--white)', borderRadius: 'var(--radius-pill)', fontSize: 12.5, fontWeight: 800, color: 'var(--text-body)', boxShadow: 'var(--shadow-sm)', cursor: 'pointer', fontFamily: 'var(--font-sans)' }}>저장</button>} />
      <ScreenBody>
        {/* Hero */}
        <div style={{ padding: '24px 24px 20px', background: 'var(--brand-gradient-soft)', textAlign: 'center' }}>
          <div style={{
            width: 88, height: 88, margin: '0 auto 14px', borderRadius: 26,
            background: 'var(--brand-gradient)', boxShadow: 'var(--shadow-brand)',
            display: 'flex', alignItems: 'center', justifyContent: 'center',
            fontSize: 40, fontWeight: 800, color: '#fff',
          }}>{b.mono}</div>
          <h1 style={{ fontSize: 26, fontWeight: 900, letterSpacing: '-0.02em', color: 'var(--ink-900)', margin: '0 0 2px' }}>{b.name}</h1>
          <div style={{ fontSize: 13.5, color: 'var(--text-caption)' }}>{b.en} · {b.nick}</div>
          <div style={{ display: 'flex', justifyContent: 'center', gap: 7, marginTop: 12, flexWrap: 'wrap' }}>
            {b.temperament.map((t) => <Badge key={t} tone="brand">{t}</Badge>)}
          </div>
        </div>

        {/* Quick facts */}
        <div style={{ display: 'flex', gap: 10, padding: '16px 20px 4px' }}>
          {[['한국 인기', b.rank + '위'], ['월 비용', b.costMonthly], ['기대 수명', b.life]].map(([k, v]) => (
            <div key={k} style={{ flex: 1, background: 'var(--white)', border: '1px solid var(--line-soft)', borderRadius: 'var(--radius-lg)', padding: '13px 8px', textAlign: 'center', boxShadow: 'var(--shadow-sm)' }}>
              <div style={{ fontSize: 11, color: 'var(--text-caption)', marginBottom: 5 }}>{k}</div>
              <div style={{ fontSize: 14, fontWeight: 900, color: 'var(--ink-900)' }}>{v}</div>
            </div>
          ))}
        </div>

        <div style={{ padding: '16px 20px 0' }}>
          <p style={{ fontSize: 14.5, lineHeight: 1.75, color: 'var(--text-body)', margin: 0 }}>{b.summary}</p>
        </div>

        {/* Traits */}
        <div style={{ padding: '20px 20px 0' }}>
          <SectionTitle title="성격 데이터" sub="AKC 기준 · 한국 보정" />
          <Card padding="16px 18px">
            <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
              {b.traits.map((t) => (
                <TraitMeter key={t.label} label={t.label} score={t.score} scaleWord={t.word} tone={t.tone} />
              ))}
            </div>
          </Card>
        </div>

        {/* Hope-first messages */}
        <div style={{ padding: '22px 20px 0' }}>
          <SectionTitle title="이 견종, 솔직하게" sub="단점도 훈련 가능성과 함께" />
          <div style={{ display: 'flex', flexDirection: 'column', gap: 11 }}>
            {b.messages.map((m, i) => (
              <TraitCard key={i} tone={m.tone} title={m.title} text={m.text} />
            ))}
          </div>
        </div>

        {/* Founder testimony */}
        {b.founder && (
          <div style={{ padding: '22px 20px 0' }}>
            <div style={{
              background: 'var(--ink-900)', borderRadius: 'var(--radius-2xl)', padding: '20px 20px 22px', color: '#fff',
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 12 }}>
                <div style={{ width: 38, height: 38, borderRadius: '50%', background: 'var(--brand-gradient)', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 17, fontWeight: 800, color: '#fff' }}>멍</div>
                <div>
                  <div style={{ fontSize: 13, fontWeight: 800 }}>멍메이트 창업자</div>
                  <div style={{ fontSize: 11, color: 'rgba(255,255,255,0.6)' }}>5년차 셸티 보호자</div>
                </div>
              </div>
              <p style={{ fontSize: 15, lineHeight: 1.75, margin: '0 0 12px', color: 'rgba(255,255,255,0.92)' }}>
                {window.MM_DATA.founderTestimony}
              </p>
              <div style={{ fontSize: 16, fontWeight: 900, color: 'var(--yellow-400)', lineHeight: 1.5 }}>
                "좋은 견종이 따로 있는 게 아니라,<br />좋은 보호자가 만듭니다."
              </div>
            </div>
          </div>
        )}

        {/* 착한개 certification CTA */}
        <div style={{ padding: '22px 20px 8px' }}>
          <div style={{
            background: 'var(--yellow-tint)', border: '1px solid var(--yellow-200)',
            borderLeft: '4px solid var(--rank-gold)',
            borderRadius: 'var(--radius-xl)', padding: '18px 18px',
          }}>
            <span style={{ fontSize: 15, fontWeight: 900, color: 'var(--ink-900)' }}>착한개 인증</span>
            <p style={{ fontSize: 13.5, lineHeight: 1.65, color: 'var(--text-body)', margin: '8px 0 14px' }}>
              AI 훈련을 마친 강아지에게 디지털 인증서를. 인증받은 강아지는 어디든 환영받습니다.
            </p>
            <Button variant="secondary" size="md" full>AI 훈련 시작하기</Button>
          </div>
        </div>
        <div style={{ height: 96 }} />
      </ScreenBody>

      <div style={{ flexShrink: 0, padding: '14px 20px 22px', background: 'var(--bg-app)', borderTop: '1px solid var(--line-soft)' }}>
        <Button variant="gradient" size="lg" full>이 견종으로 입양 준비하기</Button>
      </div>
    </React.Fragment>
  );
}

/* Section heading — a coral accent bar instead of an emoji icon. */
function SectionTitle({ title, sub }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 9, marginBottom: 11 }}>
      <span style={{ width: 4, height: 16, borderRadius: 2, background: 'var(--brand-gradient)', flexShrink: 0 }} />
      <span style={{ fontSize: 16, fontWeight: 900, color: 'var(--ink-900)', letterSpacing: '-0.02em' }}>{title}</span>
      {sub && <span style={{ fontSize: 11.5, color: 'var(--text-caption)', marginLeft: 'auto' }}>{sub}</span>}
    </div>
  );
}

window.BreedDetailScreen = BreedDetailScreen;

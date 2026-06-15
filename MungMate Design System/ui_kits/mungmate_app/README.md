# 멍메이트 App — UI kit

A high-fidelity, click-through recreation of the **멍메이트 (MungMate)** mobile web app — Korea's
responsible dog-adoption flow. Recreated from the `pellink-pj/chakhan-canine` Streamlit prototype
(`app.py`, `journey.py`, `breed_messages.py`) and the breed dataset (`result/*.json`).

## The flow (interactive in `index.html`)
1. **IntroScreen** — hero "당신, 정말 준비됐나요?" + the 11만 마리 shock stat + the two big
   `ChoiceCard` answers. Sticky gradient CTA.
2. **DiagnosticScreen** (입양 준비도 진단 / 후킹) — provocative, assumption-busting questions with a
   progress bar; answering reveals the **data "truth"** in a hope-toned card before advancing.
3. **ResultScreen** (라이프스타일 매칭) — ranked breed cards with match-score bars, Korea
   popularity rank, and monthly cost.
4. **BreedDetailScreen** — the full brand voice: `TraitMeter` data rows, hope-first `TraitCard`
   insights, the founder's Sheltie testimony, and the **착한개 인증** (Good-Dog certification) CTA.

## Composition
- Screens consume the published primitives via `window.MungMateDesignSystem_181714`
  (`Button`, `Badge`, `Chip`, `Card`, `TraitCard`, `TraitMeter`, `ChoiceCard`) — they are **not**
  re-implemented here.
- `shared.jsx` — local chrome only: `Logo`, `TopBar`, `ProgressBar`, `PhoneFrame`, `ScreenBody`.
- `data.js` — sample breed + diagnostic data (`window.MM_DATA`), lifted from the dataset.

## Files
`index.html` · `shared.jsx` · `IntroScreen.jsx` · `DiagnosticScreen.jsx` ·
`ResultScreen.jsx` · `BreedDetailScreen.jsx` · `data.js`

> Mobile-first (412×844 frame). The 착한개 certification network and AI-training surfaces are
> represented as entry points only — they were concept-stage in the source.

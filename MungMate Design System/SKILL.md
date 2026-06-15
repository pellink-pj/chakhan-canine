---
name: mungmate-design
description: Use this skill to generate well-branded interfaces and assets for 멍메이트 (MungMate) — Korea's responsible dog-adoption & AI-training ecosystem — for production or throwaway prototypes/mocks. Contains essential design guidelines, colors, type, fonts, assets, and UI kit components for prototyping.
user-invocable: true
---

Read the `README.md` file within this skill, and explore the other available files.

If creating visual artifacts (slides, mocks, throwaway prototypes, etc), copy assets out and create
static HTML files for the user to view. If working on production code, you can copy assets and read
the rules here to become an expert in designing with this brand.

If the user invokes this skill without any other guidance, ask them what they want to build or design,
ask some questions, and act as an expert designer who outputs HTML artifacts _or_ production code,
depending on the need.

## Quick orientation
- **Brand:** 멍메이트 (MungMate) / 착한 캐닌. Warm, honest, **hope-first** Korean dog-adoption service.
  The non-negotiable voice move: reframe every negative as *overcomeable with training* — never a bare
  warning. "원래 잘 짖지만, 훈련으로 컨트롤 가능해요." See README → CONTENT FUNDAMENTALS.
- **Look:** coral `#E8574A` + orange + sunny yellow on **cream** `#FFF8F2`; rounded everything
  (20–24px cards, pills); warm coral-tinted shadows; **NanumSquareRound** font. See README → VISUAL FOUNDATIONS.
- **Tokens:** link `styles.css` (it `@import`s `tokens/*.css`). Use the CSS custom properties, esp. the
  **tone trio** (`--good-*` / `--hope-*` / `--caution-*`).
- **Foundations:** `guidelines/*.card.html` — color, type, spacing, brand specimen cards.
- **Components:** `components/` (core / cards / forms) — `Button`, `Badge`, `Chip`, `Card`,
  `TraitCard` (the signature hope-first insight card), `TraitMeter`, `ChoiceCard`. Each has a
  `.prompt.md` with usage. In static HTML, load `_ds_bundle.js` and read
  `window.MungMateDesignSystem_181714`.
- **UI kit:** `ui_kits/mungmate_app/` — the full adoption flow (Intro → 준비도 진단 → 매칭 → 견종 상세).
- **Icons:** **no emoji** — meaning rides on tone color, accent bars, heavy type and the monogram
  mark; UI chrome uses Lucide line icons (CDN). See `assets/icons.md`. Never hand-roll ad-hoc SVG
  icons, and never use emoji.

## Source
Built from the GitHub repo `pellink-pj/chakhan-canine` — explore it for richer breed data and the
exact hope-message tone logic (`breed_messages.py`).

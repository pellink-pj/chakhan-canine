# 멍메이트 (MungMate) Design System

> **한국 반려동물 문화를 바꾸는, 책임감 있는 입양·훈련 생태계**
> A warm, honest, hope-first design language for Korea's responsible dog-adoption ecosystem.

---

## What this is

**멍메이트 (MungMate)** — also operating as **착한 캐닌 (Chakhan Canine)** — is a Korean-market
service that rethinks dog adoption around *responsibility* rather than *cuteness*. Instead of asking
"which breed suits you?", it first asks **"are you actually ready?"** It is built on a refined dataset
of **293 dog breeds** (AKC traits, reinterpreted for Korean apartment life) and an AI-training layer.

The product is a **4-stage ecosystem** — each stage reinforces the next:

1. **입양 준비도 진단 (Readiness Diagnostic)** — *the hook.* Provocative, data-backed questions
   ("You think a small dog is easy to raise?") that change how people *think* before they adopt.
2. **라이프스타일 매칭 (Lifestyle Matching)** — only people who pass the hook get real breed
   recommendations, blending cost · walks · training · looks · Korean-market popularity.
3. **AI 훈련 시스템 (AI Training)** — video-analysis coaching (Claude · Twelve Labs APIs),
   personalized to breed temperament, with progress tracking + certificates.
4. **착한개 인증 (Good-Dog Certification)** — trained dogs get a digital certificate and access
   to a network of dog-welcoming cafés, restaurants and parks. *"A certified dog is welcome anywhere."*

The founder's thesis, lived for 5 years with a **Shetland Sheepdog (Sheltie)** — a breed the data
calls a loud, high-strung poor fit for Korean apartments — is the heart of the brand voice:

> **"좋은 견종이 따로 있는 게 아닙니다. 좋은 보호자가 만드는 겁니다."**
> *"There's no such thing as a good breed. Good owners make good dogs."*

This reframes every "warning" as **hope + a solution** ("barks a lot — *but trainable*"), which is the
single most important thing to get right when designing for this brand.

### Products represented
- **멍메이트 web app** (primary) — the breed-matching + readiness flow. Currently a Streamlit
  prototype; a Next.js production build is planned. The UI kit `ui_kits/mungmate_app/` recreates it.
- **Pup Hero Lab (10분 영웅 키우기)** — a Tamagotchi-style mini-app that lets you "raise" a virtual
  dog of a chosen breed to validate the AI-training concept. Sample surface in `ui_kits/mungmate_app/`.
- **Pitch deck** — `mungmate-deck.md` (founder/investor narrative). Sample slides in `slides/`.

---

## Sources (provided inputs — store even if you can't open them now)

- **GitHub:** [`pellink-pj/chakhan-canine`](https://github.com/pellink-pj/chakhan-canine) — the
  Streamlit prototype (`app.py`, `journey.py`), the breed dataset (`result/*.json`, 293 breeds),
  the hope-message engine (`breed_messages.py`), the trait reference (`processed/traits_guide.json`),
  Korea-specific guidance (`docs/korea_context.md`), the pitch deck (`mungmate-deck.md`), and the
  Pup Hero Lab sub-app (`pup-hero-lab/`).
- Live demo referenced in the repo: `chakhan-canine.streamlit.app`.

> **Explore the repo further** to build richer, more accurate designs — the breed JSON files and the
> `breed_messages.py` tone-conversion logic are especially valuable for getting copy and data shapes right.

---

## CONTENT FUNDAMENTALS — how MungMate writes

The voice is the product. It is **honest but never harsh, and always hope-first.** Where a typical
breed site posts a cold warning, MungMate reframes it as a solvable challenge.

- **Hope-first reframing (the core move).** Negative traits are *never* dead-ends. The pattern is
  **acknowledge → reassure → give a path**: "원래 잘 짖지만, 훈련으로 컨트롤 가능해요" ("Barks a lot
  by nature — *but trainable, you can manage it*"). Compare the bad pattern it explicitly rejects:
  ~~"⚠️ 이 견종은 짖음이 많아요"~~ (just a warning).
- **The tone trio.** Every trait insight is one of three tones, and the whole color system encodes them:
  - **good (좋은 특성)** — fine as-is.
  - **hope (희망)** — demanding by nature, *overcomeable with training*.
  - **caution (신중히)** — genuinely think hard before adopting.
- **Pronouns & address.** Speaks directly to **"당신 / 여러분" (you)**, often with a pointed,
  almost confrontational question: *"이사 갈 집이 펫 금지면 다른 집 찾을 여유 있으세요?"*
  ("If your next place bans pets, can you afford to find another?"). It respects the reader enough
  to challenge them. Polite **-요/-습니다** endings throughout — firm, not rude.
- **Founder "I" voice.** Long-form/about copy switches to a personal **first person ("저는…")** — the
  Sheltie story is told as lived testimony, not marketing. Warm, vulnerable, specific
  ("이웃에게 사과하러 다녔어요" / "I went around apologizing to the neighbors").
- **Data as truth-teller.** Copy leans on concrete numbers to puncture assumptions:
  *"한국 유기견 11만 마리/년", "말티즈는 사실 슬개골 위험·짖음 ↑", "짖음 5/5(매우 높음)"*. Numbers
  arrive with a 1–5 scale and a plain-Korean label in parentheses.
- **Korean-first, English as accent.** All product copy is Korean. English appears only as the
  wordmark (MungMate), occasional technical nouns (AI, API), and arrows (→ ↑ ↓).
- **No emoji.** The brand uses **no emoji anywhere** — not in copy, headings, badges, or cards.
  Meaning is carried by the **tone color system** (good/hope/caution), **left accent bars**, **typographic
  weight**, and the **monogram** mark. Any iconographic need in UI chrome is met with Lucide line icons
  (see ICONOGRAPHY). This keeps the voice calm, grown-up and trustworthy rather than cute.
- **Casing & punctuation.** Korean has no case; English wordmark is `MungMate` (camel) or `멍메이트`.
  Headings are short, declarative, often a full sentence. Arrows (→) show flow/causality. Quote marks
  「」 and bold are used for the punch lines.
- **Vibe:** a knowledgeable, caring trainer-friend who won't sugarcoat the work but absolutely
  believes you and your dog can do it. Tough love, emphasis on *love*.

**Example specimens**
- Hero: **"당신, 정말 준비됐나요?"** ("Are you *really* ready?")
- Trait (hope): **원래 잘 짖지만, 훈련으로 컨트롤 가능해요**
- Trait (caution): **어린 자녀가 있으시면 신중히 고려해주세요**
- Promise: **"인증받은 강아지는 어디든 환영받습니다."**
- Thesis: **"좋은 견종이 따로 있는 게 아니라, 좋은 보호자가 만듭니다."**

---

## VISUAL FOUNDATIONS — how MungMate looks

**Overall feeling:** warm, rounded, sunny, trustworthy. Closer to a friendly Korean lifestyle app
(Kakao/Toss warmth) than a clinical pet database. Cream paper, coral energy, soft shadows, big rounded
corners. Nothing cold, nothing sharp.

- **Color.** A warm core with a cool accent, all on cream:
  - **Coral Pink `#F25D6C`** is the primary — buttons, links, big stats, the wordmark.
  - **Sunset Yellow `#F5BE3D`** is the energy/secondary — ranks, "hope", highlights, badges.
  - **Electric Blue `#0BB4F0`** is the accent — the "IT signal" / cool axis, used for tech & AI-training
    surfaces and `info` states (sparingly; it's the one cool note).
  - **Lavender Mist `#A57BD9`** is the bridge — ties coral to blue; soft decorative / fashion-design tone.
  - The **signature warm gradient** runs coral → orange → sunset (135°) on hero CTAs and the logo; a
    `--spectrum-gradient` (coral → lavender → blue) is reserved for occasional warm→cool flourishes.
  - Ground everything on **soft Light Mint `#ECF6F1`**, not white — it's easier on the eyes and far
    more distinctive than the obvious cream; white is reserved for elevated cards. (Coral pink on
    light mint is the signature fresh pairing.)
  - Neutrals (text) are **plum-tinted** (text is **Deep Plum `#2D1E33`**, not pure black), never cold gray.
  - The **tone trio** has its own fg/line/tint each: good = green, hope = sunset-yellow, caution = coral;
    a fourth **info** tone = electric blue for tech/AI.
- **Type.** One family: **NanumSquareRound** — a rounded Korean sans that carries both Hangul and
  Latin. Headlines run **heavy (800/900)** with tight tracking (-0.02 to -0.03em); body stays **400**
  with airy **1.7 line-height** (Korean needs the breathing room). Big shock-stats go 900 in coral.
- **Spacing.** 4px base rhythm. Cards breathe — generous 20–24px internal padding.
- **Corner radii — soft is the brand.** Cards `20–24px`, buttons `16px`, inputs `12px`, chips/badges
  full **pill**. Almost nothing is square. The logo mark itself is a rounded squircle.
- **Cards.** White surface on cream, `20px` radius, hairline warm border (`#F0E4D8`) **and** a soft
  **coral-tinted shadow** (`0 4px 16px rgba(91,64,48,.08)`) — warm, never a hard gray drop-shadow.
  Tone cards (good/hope/caution) add a **left accent + tinted background** in their tone color.
- **Backgrounds.** Mostly flat cream. The one signature flourish is the **coral→orange gradient**
  on primary CTAs, the logo, and hero banners. No photographic full-bleeds in the prototype, no
  noise/grain, no glassmorphism. Occasional very-soft radial cream wash behind heroes.
- **Buttons.** Primary = coral (or coral→orange gradient), white text, `16px` radius, `--shadow-brand`
  (coral-tinted). Secondary = white with warm border. Ghost = transparent, coral text.
- **Hover / press.** Hover: gentle **lift** (translateY -1px) + slightly stronger coral shadow, or a
  small darken. Press: **shrink** to ~0.97 scale (tactile, toy-like). Transitions are short (0.15–0.25s).
- **Motion.** Friendly, never flashy. `ease-out` for most; a gentle **spring/bounce**
  (`cubic-bezier(.34,1.56,.64,1)`) for playful confirmations (a dog "appearing", a stamp landing).
  Fades + small rises for entrances. No infinite loops on content. Respect reduced-motion.
- **Borders.** Hairline `1px` warm `#F0E4D8` on cream; `2px` for emphasis/selected states (coral).
- **Imagery vibe.** When photos appear they should read **warm, bright, candid** — real dogs and
  owners in everyday Korean settings (apartments, cafés, parks), never cold studio stock. Use
  `<image-slot>` placeholders in mocks; do not generate.
- **Iconography.** No emoji. UI chrome uses a clean outline icon set (Lucide); tone color + accent
  bars + the monogram carry semantic weight (see ICONOGRAPHY).
- **Transparency/blur.** Used sparingly — soft tints (`--coral-tint`, `--yellow-tint`) for card
  backgrounds, not frosted glass.
- **Fixed elements.** Mobile-first: sticky top app bar, sticky bottom primary CTA on flow screens,
  progress indicator for the multi-step readiness diagnostic.

---

## ICONOGRAPHY

MungMate uses **no emoji**. Semantics are carried by the system itself, with a single line-icon set
for genuine UI chrome:

1. **Tone color + accent bars + type** do the work emoji used to. A trait's meaning comes from its
   tone (good = green, hope = amber, caution = coral, info = electric blue), a 4px left accent bar on
   tone cards, a coral accent bar before section headings, and heavy type for emphasis. Korea
   popularity ranks read as a `gold` solid `Badge` ("한국 인기 29위"), not a medal emoji. Breed avatars
   use a **monogram** (the breed's initial in a coral-gradient squircle), not a dog emoji.
2. **UI chrome icons** use **[Lucide](https://lucide.dev)** (outline, ~2px stroke, rounded line-caps —
   matches the rounded brand) loaded from CDN for nav, inputs, chevrons, close, search, etc. See
   `assets/icons.md`. *Substitution note: the source Streamlit app ships no icon set of its own, so
   Lucide is our chosen, brand-consistent default — swap if you adopt a different production set.*

Unicode arrows (→ ↑ ↓) are still used inline in copy to show flow and trait direction. No PNG icon
sprites exist in the source. **Never hand-draw icons as ad-hoc SVG paths, and never use emoji** — use
Lucide for chrome and the tone/accent system for meaning.

---

## INDEX — what's in this system

**Foundations**
- `styles.css` — the single entry point consumers link (imports everything below).
- `tokens/fonts.css` — NanumSquareRound `@font-face` (via webfontworld CDN).
- `tokens/colors.css` — brand palette, tone trio, warm neutrals, semantic aliases.
- `tokens/typography.css` — font stack, weights, type scale, line-heights, tracking.
- `tokens/spacing.css` — spacing scale, radii, warm shadows, motion easings.
- `guidelines/*.card.html` — foundation specimen cards (Design System tab: Type / Colors / Spacing / Brand).

**Components** (`components/` — `window.MungMateDesignSystem_181714.<Name>`)
- `core/` — `Button`, `Badge`, `Chip`
- `cards/` — `Card`, `TraitCard` (the tone-trio insight card), `TraitMeter` (1–5 scale)
- `forms/` — `ChoiceCard` (big tap-target answer)

**UI kits**
- `ui_kits/mungmate_app/` — the 멍메이트 web app: readiness diagnostic → matching result → breed detail.

**Slides**
- `slides/` — pitch-deck sample slides styled from `mungmate-deck.md`.

**Assets**
- `assets/` — logo lockups, icon reference.

**Meta**
- `SKILL.md` — Agent-Skills-compatible entry so this system can be used in Claude Code.

---

## Caveats / substitutions
- **Font:** NanumSquareRound is **self-hosted** in `tokens/fonts/` (woff2 + woff, weights
  300/400/700/800 from the free `innks/NanumSquareRound` build) — the system is fully offline-capable,
  no CDN dependency. The 900 "heavy" token reuses the 800 ExtraBold cut (heaviest available); if you
  have a licensed 900/Heavy cut, drop it in and add a `@font-face` for it.
- **Icons:** Lucide is a brand-fit substitution; the source app had no dedicated icon set.
- **Imagery:** no production photography was provided — mocks use placeholders.

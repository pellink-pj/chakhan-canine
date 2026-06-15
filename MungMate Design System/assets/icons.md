# MungMate · Icon reference

MungMate uses **no emoji**. See README → ICONOGRAPHY. Meaning is carried by the design system;
genuine UI chrome uses one line-icon set.

## Track 1 — The system carries meaning (no emoji)
Instead of emoji, use:

| Need | MungMate solution |
|---|---|
| Trait sentiment (barking, energy, etc.) | `TraitCard` **tone** color + left accent bar (good/hope/caution) |
| Popularity rank | `gold` solid `Badge` — e.g. "한국 인기 29위" (no medal emoji) |
| Section heading | a coral accent bar before the title (see `SectionTitle` in the UI kit) |
| Breed avatar | **monogram** — the breed's initial in a coral-gradient squircle |
| Emphasis / shock stat | heavy type + a coral left-accent box |
| Tech / AI | `info` tone (electric blue) |

Inline unicode arrows **→ ↑ ↓** are fine in copy to show flow and trait direction.

## Track 2 — UI chrome icons (Lucide)
Outline set, ~2px stroke, rounded caps — matches the rounded brand. Load from CDN:

```html
<script src="https://unpkg.com/lucide@latest"></script>
<!-- then -->
<i data-lucide="search"></i>
<script>lucide.createIcons();</script>
```

Common chrome glyphs: `search`, `chevron-left`, `chevron-right`, `x`, `menu`,
`arrow-right`, `check`, `heart`, `home`, `user`, `settings`, `bell`, `map-pin`,
`badge-check` (착한개 certification), `dog`, `bone`, `paw-print`.

> **Substitution note:** the source Streamlit app ships no icon set. Lucide is our
> brand-consistent default. Swap if a production set is adopted. **Never hand-roll ad-hoc SVG icons,
> and never use emoji.**

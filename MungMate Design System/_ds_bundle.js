/* @ds-bundle: {"format":3,"namespace":"MungMateDesignSystem_181714","components":[{"name":"Card","sourcePath":"components/cards/Card.jsx"},{"name":"TraitCard","sourcePath":"components/cards/TraitCard.jsx"},{"name":"TraitMeter","sourcePath":"components/cards/TraitMeter.jsx"},{"name":"Badge","sourcePath":"components/core/Badge.jsx"},{"name":"Button","sourcePath":"components/core/Button.jsx"},{"name":"Chip","sourcePath":"components/core/Chip.jsx"},{"name":"ChoiceCard","sourcePath":"components/forms/ChoiceCard.jsx"}],"sourceHashes":{"components/cards/Card.jsx":"1511ea195d22","components/cards/TraitCard.jsx":"7946ab32946f","components/cards/TraitMeter.jsx":"241d6baa4482","components/core/Badge.jsx":"7b2f4b8c59fd","components/core/Button.jsx":"d6186901d0b2","components/core/Chip.jsx":"29ce6a79cc24","components/forms/ChoiceCard.jsx":"50126f42adbd","ui_kits/mungmate_app/BreedDetailScreen.jsx":"6c96b25819fb","ui_kits/mungmate_app/DiagnosticScreen.jsx":"f1d07a71eda6","ui_kits/mungmate_app/IntroScreen.jsx":"f1ebb383aac8","ui_kits/mungmate_app/ResultScreen.jsx":"8fbd9f4a81a9","ui_kits/mungmate_app/data.js":"36cb5246d09e","ui_kits/mungmate_app/shared.jsx":"e83f207fc1e2"},"inlinedExternals":[],"unexposedExports":[]} */

(() => {

const __ds_ns = (window.MungMateDesignSystem_181714 = window.MungMateDesignSystem_181714 || {});

const __ds_scope = {};

(__ds_ns.__errors = __ds_ns.__errors || []);

// components/cards/Card.jsx
try { (() => {
/**
 * Base surface card — white on cream, 20px radius, hairline warm border
 * plus soft coral-tinted shadow. Lifts slightly on hover when interactive.
 */
function Card({
  children,
  padding = 'var(--space-6)',
  interactive = false,
  onClick,
  style = {}
}) {
  const [hover, setHover] = React.useState(false);
  return /*#__PURE__*/React.createElement("div", {
    onClick: onClick,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      background: 'var(--bg-elevated)',
      border: '1px solid var(--border-card)',
      borderRadius: 'var(--radius-xl)',
      boxShadow: interactive && hover ? 'var(--shadow-lg)' : 'var(--shadow-card)',
      padding,
      cursor: interactive ? 'pointer' : 'default',
      transform: interactive && hover ? 'translateY(-2px)' : 'none',
      transition: 'transform var(--dur-base) var(--ease-out), box-shadow var(--dur-base) var(--ease-out)',
      ...style
    }
  }, children);
}
Object.assign(__ds_scope, { Card });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/cards/Card.jsx", error: String((e && e.message) || e) }); }

// components/cards/TraitCard.jsx
try { (() => {
/**
 * The signature MungMate insight card. Renders one trait message in the
 * brand's hope-first voice: a headline + explanation, tinted and accented by
 * tone (good / hope / caution). Mirrors breed_messages.py output. The brand
 * uses no emoji — tone color + the left accent bar carry the meaning. An
 * optional `icon` (e.g. a Lucide node) may be passed but is not used by default.
 */
function TraitCard({
  icon,
  title,
  text,
  tone = 'hope',
  style = {}
}) {
  const tones = {
    good: {
      fg: 'var(--good-fg)',
      line: 'var(--good-line)',
      bg: 'var(--good-tint)'
    },
    hope: {
      fg: 'var(--hope-fg)',
      line: 'var(--hope-line)',
      bg: 'var(--hope-tint)'
    },
    caution: {
      fg: 'var(--caution-fg)',
      line: 'var(--caution-line)',
      bg: 'var(--caution-tint)'
    }
  };
  const t = tones[tone] || tones.hope;
  const label = {
    good: '좋은 특성',
    hope: '훈련으로 극복 가능',
    caution: '신중히 고려'
  }[tone];
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: '13px',
      background: t.bg,
      border: '1px solid var(--border-card)',
      borderLeft: `4px solid ${t.line}`,
      borderRadius: 'var(--radius-xl)',
      padding: '15px 17px',
      ...style
    }
  }, icon != null && /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: '22px',
      lineHeight: 1.1,
      flexShrink: 0,
      color: t.fg
    }
  }, icon), /*#__PURE__*/React.createElement("div", {
    style: {
      minWidth: 0
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontWeight: 800,
      fontSize: '10.5px',
      textTransform: 'uppercase',
      letterSpacing: '0.05em',
      color: t.fg,
      marginBottom: '5px'
    }
  }, label), /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontWeight: 800,
      fontSize: 'var(--text-lg)',
      color: 'var(--text-strong)',
      lineHeight: 'var(--lh-snug)',
      letterSpacing: 'var(--tracking-snug)'
    }
  }, title), text && /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontWeight: 400,
      fontSize: 'var(--text-sm)',
      color: 'var(--text-body)',
      lineHeight: 'var(--lh-body)',
      marginTop: '5px'
    }
  }, text)));
}
Object.assign(__ds_scope, { TraitCard });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/cards/TraitCard.jsx", error: String((e && e.message) || e) }); }

// components/cards/TraitMeter.jsx
try { (() => {
/**
 * 1–5 trait meter row (AKC-style). Label + 5 dots filled to `score`, with the
 * plain-Korean scale word. Filled dots use the brand gradient; high scores on
 * "negative" traits can be flagged caution via the `tone` prop.
 */
function TraitMeter({
  label,
  score = 3,
  max = 5,
  scaleWord,
  tone = 'brand',
  style = {}
}) {
  const fill = {
    brand: 'var(--coral-500)',
    good: 'var(--good-line)',
    hope: 'var(--hope-line)',
    caution: 'var(--caution-line)'
  }[tone] || 'var(--coral-500)';
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: '12px',
      ...style
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontWeight: 700,
      fontSize: 'var(--text-sm)',
      color: 'var(--text-body)',
      width: '92px',
      flexShrink: 0
    }
  }, label), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: '5px',
      flexShrink: 0
    }
  }, Array.from({
    length: max
  }).map((_, i) => /*#__PURE__*/React.createElement("span", {
    key: i,
    style: {
      width: '13px',
      height: '13px',
      borderRadius: '50%',
      background: i < score ? fill : 'var(--mint-200)',
      border: i < score ? 'none' : '1px solid var(--border-card)'
    }
  }))), scaleWord && /*#__PURE__*/React.createElement("div", {
    style: {
      fontFamily: 'var(--font-sans)',
      fontWeight: 700,
      fontSize: 'var(--text-xs)',
      color: tone === 'brand' ? 'var(--text-muted)' : fill
    }
  }, scaleWord));
}
Object.assign(__ds_scope, { TraitMeter });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/cards/TraitMeter.jsx", error: String((e && e.message) || e) }); }

// components/core/Badge.jsx
try { (() => {
/**
 * Small pill label. Tone-aware (good/hope/caution/brand/neutral/gold).
 * Used for trait tags, the 착한개 certification mark, popularity ranks.
 */
function Badge({
  children,
  tone = 'brand',
  icon = null,
  solid = false,
  style = {}
}) {
  const tones = {
    brand: {
      fg: 'var(--brand)',
      bg: 'var(--coral-tint)',
      solidBg: 'var(--coral-600)'
    },
    good: {
      fg: 'var(--good-fg)',
      bg: 'var(--good-tint)',
      solidBg: 'var(--good-line)'
    },
    hope: {
      fg: 'var(--hope-fg)',
      bg: 'var(--hope-tint)',
      solidBg: 'var(--hope-line)'
    },
    caution: {
      fg: 'var(--caution-fg)',
      bg: 'var(--caution-tint)',
      solidBg: 'var(--caution-line)'
    },
    info: {
      fg: 'var(--info-fg)',
      bg: 'var(--info-tint)',
      solidBg: 'var(--info-line)'
    },
    gold: {
      fg: '#fff',
      bg: 'var(--yellow-tint)',
      solidBg: 'var(--rank-gold)'
    },
    neutral: {
      fg: 'var(--text-muted)',
      bg: 'var(--mint-200)',
      solidBg: 'var(--ink-600)'
    }
  };
  const t = tones[tone] || tones.brand;
  return /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: '4px',
      fontFamily: 'var(--font-sans)',
      fontWeight: 800,
      fontSize: 'var(--text-xs)',
      lineHeight: 1,
      padding: '5px 10px',
      borderRadius: 'var(--radius-pill)',
      color: solid ? '#fff' : t.fg,
      background: solid ? t.solidBg : t.bg,
      ...style
    }
  }, icon != null && /*#__PURE__*/React.createElement("span", null, icon), children);
}
Object.assign(__ds_scope, { Badge });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Badge.jsx", error: String((e && e.message) || e) }); }

// components/core/Button.jsx
try { (() => {
function _extends() { return _extends = Object.assign ? Object.assign.bind() : function (n) { for (var e = 1; e < arguments.length; e++) { var t = arguments[e]; for (var r in t) ({}).hasOwnProperty.call(t, r) && (n[r] = t[r]); } return n; }, _extends.apply(null, arguments); }
/**
 * MungMate primary button. Coral or coral→orange gradient, rounded 16px,
 * warm coral-tinted shadow, tactile shrink on press.
 */
function Button({
  children,
  variant = 'primary',
  // primary | gradient | secondary | ghost
  size = 'md',
  // sm | md | lg
  full = false,
  icon = null,
  // leading content (emoji or <i data-lucide>)
  disabled = false,
  onClick,
  type = 'button',
  style = {},
  ...rest
}) {
  const sizes = {
    sm: {
      padding: '8px 14px',
      fontSize: '13.5px',
      radius: 'var(--radius-md)',
      gap: '6px'
    },
    md: {
      padding: '12px 20px',
      fontSize: 'var(--text-base)',
      radius: 'var(--radius-lg)',
      gap: '8px'
    },
    lg: {
      padding: '16px 26px',
      fontSize: 'var(--text-lg)',
      radius: 'var(--radius-lg)',
      gap: '9px'
    }
  };
  const s = sizes[size] || sizes.md;
  const variants = {
    primary: {
      background: 'var(--coral-600)',
      color: 'var(--text-on-brand)',
      border: '1px solid transparent',
      boxShadow: 'var(--shadow-brand)'
    },
    gradient: {
      background: 'var(--brand-gradient)',
      color: 'var(--text-on-brand)',
      border: '1px solid transparent',
      boxShadow: 'var(--shadow-brand)'
    },
    secondary: {
      background: 'var(--white)',
      color: 'var(--text-strong)',
      border: '1px solid var(--border-strong)',
      boxShadow: 'var(--shadow-sm)'
    },
    ghost: {
      background: 'transparent',
      color: 'var(--brand)',
      border: '1px solid transparent',
      boxShadow: 'none'
    }
  };
  const v = variants[variant] || variants.primary;
  const [pressed, setPressed] = React.useState(false);
  const [hover, setHover] = React.useState(false);
  return /*#__PURE__*/React.createElement("button", _extends({
    type: type,
    disabled: disabled,
    onClick: onClick,
    onMouseDown: () => setPressed(true),
    onMouseUp: () => setPressed(false),
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => {
      setHover(false);
      setPressed(false);
    },
    style: {
      display: full ? 'flex' : 'inline-flex',
      width: full ? '100%' : 'auto',
      alignItems: 'center',
      justifyContent: 'center',
      gap: s.gap,
      fontFamily: 'var(--font-sans)',
      fontWeight: 800,
      fontSize: s.fontSize,
      lineHeight: 1,
      padding: s.padding,
      borderRadius: s.radius,
      cursor: disabled ? 'not-allowed' : 'pointer',
      opacity: disabled ? 0.45 : 1,
      transform: pressed ? 'scale(0.97)' : hover && !disabled ? 'translateY(-1px)' : 'none',
      boxShadow: hover && !disabled && (variant === 'primary' || variant === 'gradient') ? 'var(--shadow-brand-hover)' : v.boxShadow,
      filter: hover && !disabled && variant === 'secondary' ? 'brightness(0.98)' : 'none',
      transition: 'transform var(--dur-fast) var(--ease-snap), box-shadow var(--dur-base) var(--ease-out)',
      ...v,
      ...style
    }
  }, rest), icon != null && /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'inline-flex',
      fontSize: '1.1em'
    }
  }, icon), children);
}
Object.assign(__ds_scope, { Button });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Button.jsx", error: String((e && e.message) || e) }); }

// components/core/Chip.jsx
try { (() => {
/**
 * Selectable chip — filter/option tags. Pill, warm border, coral when selected.
 */
function Chip({
  children,
  selected = false,
  icon = null,
  onClick,
  style = {}
}) {
  const [hover, setHover] = React.useState(false);
  return /*#__PURE__*/React.createElement("button", {
    type: "button",
    onClick: onClick,
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => setHover(false),
    style: {
      display: 'inline-flex',
      alignItems: 'center',
      gap: '6px',
      fontFamily: 'var(--font-sans)',
      fontWeight: 700,
      fontSize: 'var(--text-sm)',
      lineHeight: 1,
      padding: '9px 15px',
      borderRadius: 'var(--radius-pill)',
      cursor: 'pointer',
      color: selected ? 'var(--brand)' : 'var(--text-body)',
      background: selected ? 'var(--coral-tint)' : 'var(--white)',
      border: selected ? '1.5px solid var(--coral-500)' : '1.5px solid var(--border-card)',
      boxShadow: hover && !selected ? 'var(--shadow-sm)' : 'none',
      transition: 'all var(--dur-fast) var(--ease-out)',
      ...style
    }
  }, icon != null && /*#__PURE__*/React.createElement("span", null, icon), children);
}
Object.assign(__ds_scope, { Chip });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/core/Chip.jsx", error: String((e && e.message) || e) }); }

// components/forms/ChoiceCard.jsx
try { (() => {
/**
 * Big tap-target answer card for the readiness diagnostic (후킹 질문).
 * Full-width, generous hit area, coral selection state, gentle press shrink.
 */
function ChoiceCard({
  icon,
  label,
  sub,
  selected = false,
  onClick,
  style = {}
}) {
  const [hover, setHover] = React.useState(false);
  const [pressed, setPressed] = React.useState(false);
  return /*#__PURE__*/React.createElement("button", {
    type: "button",
    onClick: onClick,
    onMouseDown: () => setPressed(true),
    onMouseUp: () => setPressed(false),
    onMouseEnter: () => setHover(true),
    onMouseLeave: () => {
      setHover(false);
      setPressed(false);
    },
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: '14px',
      width: '100%',
      textAlign: 'left',
      fontFamily: 'var(--font-sans)',
      cursor: 'pointer',
      padding: '18px 20px',
      minHeight: '64px',
      borderRadius: 'var(--radius-lg)',
      background: selected ? 'var(--coral-tint)' : 'var(--white)',
      border: selected ? '2px solid var(--coral-500)' : '2px solid var(--border-card)',
      boxShadow: selected ? 'var(--shadow-brand)' : hover ? 'var(--shadow-card)' : 'var(--shadow-sm)',
      transform: pressed ? 'scale(0.985)' : 'none',
      transition: 'transform var(--dur-fast) var(--ease-snap), box-shadow var(--dur-base) var(--ease-out), border-color var(--dur-fast) var(--ease-out)',
      ...style
    }
  }, icon != null && /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: '24px',
      width: '44px',
      height: '44px',
      flexShrink: 0,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      borderRadius: 'var(--radius-md)',
      background: selected ? 'var(--white)' : 'var(--mint-100)'
    }
  }, icon), /*#__PURE__*/React.createElement("span", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: '3px',
      minWidth: 0
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontWeight: 800,
      fontSize: 'var(--text-lg)',
      color: selected ? 'var(--brand-strong)' : 'var(--text-strong)'
    }
  }, label), sub && /*#__PURE__*/React.createElement("span", {
    style: {
      fontWeight: 400,
      fontSize: 'var(--text-sm)',
      color: 'var(--text-muted)'
    }
  }, sub)), /*#__PURE__*/React.createElement("span", {
    style: {
      marginLeft: 'auto',
      flexShrink: 0,
      width: '22px',
      height: '22px',
      borderRadius: '50%',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      border: selected ? 'none' : '2px solid var(--border-strong)',
      background: selected ? 'var(--coral-600)' : 'transparent',
      color: '#fff',
      fontSize: '13px',
      fontWeight: 900
    }
  }, selected ? '✓' : ''));
}
Object.assign(__ds_scope, { ChoiceCard });
})(); } catch (e) { __ds_ns.__errors.push({ path: "components/forms/ChoiceCard.jsx", error: String((e && e.message) || e) }); }

// ui_kits/mungmate_app/BreedDetailScreen.jsx
try { (() => {
/* MungMate app — Breed detail. Traits, hope-first messages, founder testimony,
   착한개 certification CTA. The brand's voice in full — no emoji; tone color,
   accent bars and a monogram avatar carry the visual weight. */

function BreedDetailScreen({
  breedId,
  onBack
}) {
  const {
    Card,
    TraitCard,
    TraitMeter,
    Badge,
    Button
  } = window.MungMateDesignSystem_181714;
  const b = window.MM_DATA.breeds.find(x => x.id === breedId) || window.MM_DATA.breeds[0];
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(TopBar, {
    onBack: onBack,
    title: b.name,
    right: /*#__PURE__*/React.createElement("button", {
      "aria-label": "\uC800\uC7A5",
      style: {
        height: 32,
        padding: '0 12px',
        border: '1px solid var(--border-strong)',
        background: 'var(--white)',
        borderRadius: 'var(--radius-pill)',
        fontSize: 12.5,
        fontWeight: 800,
        color: 'var(--text-body)',
        boxShadow: 'var(--shadow-sm)',
        cursor: 'pointer',
        fontFamily: 'var(--font-sans)'
      }
    }, "\uC800\uC7A5")
  }), /*#__PURE__*/React.createElement(ScreenBody, null, /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '24px 24px 20px',
      background: 'var(--brand-gradient-soft)',
      textAlign: 'center'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 88,
      height: 88,
      margin: '0 auto 14px',
      borderRadius: 26,
      background: 'var(--brand-gradient)',
      boxShadow: 'var(--shadow-brand)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontSize: 40,
      fontWeight: 800,
      color: '#fff'
    }
  }, b.mono), /*#__PURE__*/React.createElement("h1", {
    style: {
      fontSize: 26,
      fontWeight: 900,
      letterSpacing: '-0.02em',
      color: 'var(--ink-900)',
      margin: '0 0 2px'
    }
  }, b.name), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 13.5,
      color: 'var(--text-caption)'
    }
  }, b.en, " \xB7 ", b.nick), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'center',
      gap: 7,
      marginTop: 12,
      flexWrap: 'wrap'
    }
  }, b.temperament.map(t => /*#__PURE__*/React.createElement(Badge, {
    key: t,
    tone: "brand"
  }, t)))), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 10,
      padding: '16px 20px 4px'
    }
  }, [['한국 인기', b.rank + '위'], ['월 비용', b.costMonthly], ['기대 수명', b.life]].map(([k, v]) => /*#__PURE__*/React.createElement("div", {
    key: k,
    style: {
      flex: 1,
      background: 'var(--white)',
      border: '1px solid var(--line-soft)',
      borderRadius: 'var(--radius-lg)',
      padding: '13px 8px',
      textAlign: 'center',
      boxShadow: 'var(--shadow-sm)'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 11,
      color: 'var(--text-caption)',
      marginBottom: 5
    }
  }, k), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 14,
      fontWeight: 900,
      color: 'var(--ink-900)'
    }
  }, v)))), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '16px 20px 0'
    }
  }, /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 14.5,
      lineHeight: 1.75,
      color: 'var(--text-body)',
      margin: 0
    }
  }, b.summary)), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '20px 20px 0'
    }
  }, /*#__PURE__*/React.createElement(SectionTitle, {
    title: "\uC131\uACA9 \uB370\uC774\uD130",
    sub: "AKC \uAE30\uC900 \xB7 \uD55C\uAD6D \uBCF4\uC815"
  }), /*#__PURE__*/React.createElement(Card, {
    padding: "16px 18px"
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 12
    }
  }, b.traits.map(t => /*#__PURE__*/React.createElement(TraitMeter, {
    key: t.label,
    label: t.label,
    score: t.score,
    scaleWord: t.word,
    tone: t.tone
  }))))), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '22px 20px 0'
    }
  }, /*#__PURE__*/React.createElement(SectionTitle, {
    title: "\uC774 \uACAC\uC885, \uC194\uC9C1\uD558\uAC8C",
    sub: "\uB2E8\uC810\uB3C4 \uD6C8\uB828 \uAC00\uB2A5\uC131\uACFC \uD568\uAED8"
  }), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 11
    }
  }, b.messages.map((m, i) => /*#__PURE__*/React.createElement(TraitCard, {
    key: i,
    tone: m.tone,
    title: m.title,
    text: m.text
  })))), b.founder && /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '22px 20px 0'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      background: 'var(--ink-900)',
      borderRadius: 'var(--radius-2xl)',
      padding: '20px 20px 22px',
      color: '#fff'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 10,
      marginBottom: 12
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 38,
      height: 38,
      borderRadius: '50%',
      background: 'var(--brand-gradient)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontSize: 17,
      fontWeight: 800,
      color: '#fff'
    }
  }, "\uBA4D"), /*#__PURE__*/React.createElement("div", null, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 13,
      fontWeight: 800
    }
  }, "\uBA4D\uBA54\uC774\uD2B8 \uCC3D\uC5C5\uC790"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 11,
      color: 'rgba(255,255,255,0.6)'
    }
  }, "5\uB144\uCC28 \uC178\uD2F0 \uBCF4\uD638\uC790"))), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 15,
      lineHeight: 1.75,
      margin: '0 0 12px',
      color: 'rgba(255,255,255,0.92)'
    }
  }, window.MM_DATA.founderTestimony), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 16,
      fontWeight: 900,
      color: 'var(--yellow-400)',
      lineHeight: 1.5
    }
  }, "\"\uC88B\uC740 \uACAC\uC885\uC774 \uB530\uB85C \uC788\uB294 \uAC8C \uC544\uB2C8\uB77C,", /*#__PURE__*/React.createElement("br", null), "\uC88B\uC740 \uBCF4\uD638\uC790\uAC00 \uB9CC\uB4ED\uB2C8\uB2E4.\""))), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '22px 20px 8px'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      background: 'var(--yellow-tint)',
      border: '1px solid var(--yellow-200)',
      borderLeft: '4px solid var(--rank-gold)',
      borderRadius: 'var(--radius-xl)',
      padding: '18px 18px'
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 15,
      fontWeight: 900,
      color: 'var(--ink-900)'
    }
  }, "\uCC29\uD55C\uAC1C \uC778\uC99D"), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 13.5,
      lineHeight: 1.65,
      color: 'var(--text-body)',
      margin: '8px 0 14px'
    }
  }, "AI \uD6C8\uB828\uC744 \uB9C8\uCE5C \uAC15\uC544\uC9C0\uC5D0\uAC8C \uB514\uC9C0\uD138 \uC778\uC99D\uC11C\uB97C. \uC778\uC99D\uBC1B\uC740 \uAC15\uC544\uC9C0\uB294 \uC5B4\uB514\uB4E0 \uD658\uC601\uBC1B\uC2B5\uB2C8\uB2E4."), /*#__PURE__*/React.createElement(Button, {
    variant: "secondary",
    size: "md",
    full: true
  }, "AI \uD6C8\uB828 \uC2DC\uC791\uD558\uAE30"))), /*#__PURE__*/React.createElement("div", {
    style: {
      height: 96
    }
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      flexShrink: 0,
      padding: '14px 20px 22px',
      background: 'var(--bg-app)',
      borderTop: '1px solid var(--line-soft)'
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "gradient",
    size: "lg",
    full: true
  }, "\uC774 \uACAC\uC885\uC73C\uB85C \uC785\uC591 \uC900\uBE44\uD558\uAE30")));
}

/* Section heading — a coral accent bar instead of an emoji icon. */
function SectionTitle({
  title,
  sub
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 9,
      marginBottom: 11
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      width: 4,
      height: 16,
      borderRadius: 2,
      background: 'var(--brand-gradient)',
      flexShrink: 0
    }
  }), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 16,
      fontWeight: 900,
      color: 'var(--ink-900)',
      letterSpacing: '-0.02em'
    }
  }, title), sub && /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 11.5,
      color: 'var(--text-caption)',
      marginLeft: 'auto'
    }
  }, sub));
}
window.BreedDetailScreen = BreedDetailScreen;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/mungmate_app/BreedDetailScreen.jsx", error: String((e && e.message) || e) }); }

// ui_kits/mungmate_app/DiagnosticScreen.jsx
try { (() => {
/* MungMate app — Readiness diagnostic (후킹 질문).
   Provocative question → answer → data "truth" reveal → next. */

function DiagnosticScreen({
  onBack,
  onDone
}) {
  const {
    Button,
    ChoiceCard
  } = window.MungMateDesignSystem_181714;
  const questions = window.MM_DATA.diagnostic;
  const [step, setStep] = React.useState(0);
  const [answer, setAnswer] = React.useState(null);
  const [revealed, setRevealed] = React.useState(false);
  const q = questions[step];
  function next() {
    if (!revealed) {
      setRevealed(true);
      return;
    }
    if (step + 1 < questions.length) {
      setStep(step + 1);
      setAnswer(null);
      setRevealed(false);
    } else {
      onDone();
    }
  }
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(TopBar, {
    onBack: onBack,
    title: "\uC785\uC591 \uC900\uBE44\uB3C4 \uC9C4\uB2E8"
  }), /*#__PURE__*/React.createElement(ProgressBar, {
    step: step,
    total: questions.length
  }), /*#__PURE__*/React.createElement(ScreenBody, null, /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '18px 24px 8px'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 12,
      fontWeight: 800,
      color: 'var(--brand)',
      letterSpacing: '0.04em',
      marginBottom: 10
    }
  }, "Q", step + 1, " / ", questions.length), /*#__PURE__*/React.createElement("h2", {
    style: {
      fontSize: 23,
      fontWeight: 900,
      lineHeight: 1.35,
      letterSpacing: '-0.02em',
      color: 'var(--ink-900)',
      margin: '0 0 6px'
    }
  }, q.q), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 13.5,
      color: 'var(--text-muted)',
      margin: 0
    }
  }, q.hint)), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '16px 24px',
      display: 'flex',
      flexDirection: 'column',
      gap: 11
    }
  }, q.options.map(o => /*#__PURE__*/React.createElement(ChoiceCard, {
    key: o.value,
    icon: o.icon,
    label: o.label,
    selected: answer === o.value,
    onClick: () => {
      if (!revealed) setAnswer(o.value);
    }
  }))), revealed && /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '0 24px 8px',
      animation: 'mmRise 0.4s var(--ease-out) both'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      background: 'var(--hope-tint)',
      border: '1px solid var(--border-card)',
      borderLeft: '4px solid var(--hope-line)',
      borderRadius: 'var(--radius-xl)',
      padding: '15px 17px'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 11,
      fontWeight: 800,
      textTransform: 'uppercase',
      letterSpacing: '0.05em',
      color: 'var(--hope-fg)',
      marginBottom: 5
    }
  }, "\uB370\uC774\uD130\uAC00 \uB9D0\uD558\uB294 \uC9C4\uC2E4"), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 14.5,
      lineHeight: 1.65,
      color: 'var(--ink-900)',
      margin: 0,
      fontWeight: 500
    }
  }, q.truth))), /*#__PURE__*/React.createElement("div", {
    style: {
      height: 100
    }
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      flexShrink: 0,
      padding: '14px 20px 22px',
      background: 'var(--bg-app)',
      borderTop: '1px solid var(--line-soft)'
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: revealed ? 'gradient' : 'primary',
    size: "lg",
    full: true,
    disabled: !answer,
    onClick: next
  }, !revealed ? '진실 확인하기' : step + 1 < questions.length ? '다음 질문' : '내 견종 매칭 보기')));
}
window.DiagnosticScreen = DiagnosticScreen;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/mungmate_app/DiagnosticScreen.jsx", error: String((e && e.message) || e) }); }

// ui_kits/mungmate_app/IntroScreen.jsx
try { (() => {
/* MungMate app — Intro / hero screen.
   "당신, 정말 준비됐나요?" → two big ChoiceCards. */

function IntroScreen({
  onStart
}) {
  const {
    Button,
    ChoiceCard,
    Badge
  } = window.MungMateDesignSystem_181714;
  const [answer, setAnswer] = React.useState(null);
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(TopBar, {
    right: /*#__PURE__*/React.createElement(Badge, {
      tone: "neutral"
    }, "\uBCA0\uD0C0")
  }), /*#__PURE__*/React.createElement(ScreenBody, null, /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '34px 24px 20px',
      background: 'var(--brand-gradient-soft)'
    }
  }, /*#__PURE__*/React.createElement(Badge, {
    tone: "brand"
  }, "\uD55C\uAD6D\uD615 \uCC45\uC784 \uC785\uC591"), /*#__PURE__*/React.createElement("h1", {
    style: {
      fontSize: 34,
      fontWeight: 900,
      lineHeight: 1.2,
      letterSpacing: '-0.03em',
      color: 'var(--ink-900)',
      margin: '16px 0 10px'
    }
  }, "\uB2F9\uC2E0,", /*#__PURE__*/React.createElement("br", null), "\uC815\uB9D0 ", /*#__PURE__*/React.createElement("span", {
    style: {
      color: 'var(--brand)'
    }
  }, "\uC900\uBE44\uB410\uB098\uC694?")), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 15,
      lineHeight: 1.7,
      color: 'var(--text-body)',
      margin: 0
    }
  }, "\uADC0\uC5EC\uC6C0\uB9CC \uBCF4\uACE0 \uB370\uB824\uC624\uAE30 \uC804\uC5D0. 293\uAC1C \uACAC\uC885 \uB370\uC774\uD130\uB85C, \uB2F9\uC2E0\uC758 \uB77C\uC774\uD504\uC2A4\uD0C0\uC77C\uC5D0 \uB9DE\uB294 \uAC15\uC544\uC9C0\uB97C \uCC3E\uC544\uB4DC\uB824\uC694.")), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '24px 24px 8px'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      background: 'var(--coral-tint)',
      border: '1px solid var(--coral-100)',
      borderLeft: '4px solid var(--coral-600)',
      borderRadius: 'var(--radius-xl)',
      padding: '16px 18px'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 13,
      color: 'var(--caution-fg)',
      fontWeight: 700
    }
  }, "\uB9E4\uB144 \uD55C\uAD6D\uC5D0\uC11C"), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 15,
      color: 'var(--ink-900)',
      fontWeight: 700
    }
  }, /*#__PURE__*/React.createElement("b", {
    style: {
      fontSize: 28,
      fontWeight: 900,
      color: 'var(--brand)'
    }
  }, "11\uB9CC \uB9C8\uB9AC"), "\uAC00 \uC720\uAE30\uB429\uB2C8\uB2E4"))), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '20px 24px 16px'
    }
  }, /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 18,
      fontWeight: 800,
      color: 'var(--ink-900)',
      margin: '0 0 14px',
      letterSpacing: '-0.02em'
    }
  }, "\uB9C8\uC74C\uC5D0 \uB454 \uAC15\uC544\uC9C0\uAC00 \uC788\uC73C\uC138\uC694?"), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      flexDirection: 'column',
      gap: 11
    }
  }, /*#__PURE__*/React.createElement(ChoiceCard, {
    label: "\uB124, \uC788\uC5B4\uC694",
    sub: "\uC774 \uACAC\uC885\uC774 \uB098\uB791 \uB9DE\uB294\uC9C0 \uD655\uC778\uD560\uB798\uC694",
    selected: answer === 'yes',
    onClick: () => setAnswer('yes')
  }), /*#__PURE__*/React.createElement(ChoiceCard, {
    label: "\uC798 \uBAA8\uB974\uACA0\uC5B4\uC694",
    sub: "\uB77C\uC774\uD504\uC2A4\uD0C0\uC77C\uC5D0 \uB9DE\uB294 \uACAC\uC885\uC744 \uCD94\uCC9C\uBC1B\uC744\uB798\uC694",
    selected: answer === 'no',
    onClick: () => setAnswer('no')
  }))), /*#__PURE__*/React.createElement("div", {
    style: {
      height: 96
    }
  })), /*#__PURE__*/React.createElement("div", {
    style: {
      flexShrink: 0,
      padding: '14px 20px 22px',
      background: 'var(--bg-app)',
      borderTop: '1px solid var(--line-soft)'
    }
  }, /*#__PURE__*/React.createElement(Button, {
    variant: "gradient",
    size: "lg",
    full: true,
    disabled: !answer,
    onClick: onStart
  }, "\uC900\uBE44\uB3C4 \uC9C4\uB2E8 \uC2DC\uC791\uD558\uAE30")));
}
window.IntroScreen = IntroScreen;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/mungmate_app/IntroScreen.jsx", error: String((e && e.message) || e) }); }

// ui_kits/mungmate_app/ResultScreen.jsx
try { (() => {
/* MungMate app — Lifestyle match result. Ranked breed cards. */

function ResultScreen({
  onBack,
  onOpen
}) {
  const {
    Card,
    Badge
  } = window.MungMateDesignSystem_181714;
  const breeds = window.MM_DATA.breeds;
  return /*#__PURE__*/React.createElement(React.Fragment, null, /*#__PURE__*/React.createElement(TopBar, {
    onBack: onBack,
    title: "\uB77C\uC774\uD504\uC2A4\uD0C0\uC77C \uB9E4\uCE6D"
  }), /*#__PURE__*/React.createElement(ScreenBody, null, /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '20px 24px 12px'
    }
  }, /*#__PURE__*/React.createElement(Badge, {
    tone: "good"
  }, "\uC9C4\uB2E8 \uD1B5\uACFC"), /*#__PURE__*/React.createElement("h2", {
    style: {
      fontSize: 22,
      fontWeight: 900,
      letterSpacing: '-0.02em',
      color: 'var(--ink-900)',
      margin: '12px 0 6px'
    }
  }, "\uC900\uBE44\uB41C \uB2F9\uC2E0\uC5D0\uAC8C", /*#__PURE__*/React.createElement("br", null), "\uC5B4\uC6B8\uB9AC\uB294 \uACAC\uC885\uC774\uC5D0\uC694"), /*#__PURE__*/React.createElement("p", {
    style: {
      fontSize: 14,
      lineHeight: 1.65,
      color: 'var(--text-muted)',
      margin: 0
    }
  }, "\uBE44\uC6A9 \xB7 \uC0B0\uCC45 \xB7 \uD6C8\uB828 + \uD55C\uAD6D \uC2DC\uC7A5 \uC778\uAE30\uAE4C\uC9C0 \uD1B5\uD569 \uB9E4\uCE6D\uD55C \uACB0\uACFC\uC608\uC694.")), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '8px 18px 24px',
      display: 'flex',
      flexDirection: 'column',
      gap: 13
    }
  }, breeds.map(b => /*#__PURE__*/React.createElement(Card, {
    key: b.id,
    interactive: true,
    padding: "0",
    onClick: () => onOpen(b.id),
    style: {
      overflow: 'hidden'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 14,
      padding: 16
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: 64,
      height: 64,
      flexShrink: 0,
      borderRadius: 'var(--radius-lg)',
      background: 'var(--brand-gradient)',
      border: 'none',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontSize: 26,
      fontWeight: 800,
      color: '#fff'
    }
  }, b.mono), /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      minWidth: 0
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: 8
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 17,
      fontWeight: 900,
      color: 'var(--ink-900)'
    }
  }, b.name), b.founder && /*#__PURE__*/React.createElement(Badge, {
    tone: "brand",
    solid: true
  }, "\uCC3D\uC5C5\uC790\uC758 \uACAC\uC885")), /*#__PURE__*/React.createElement("div", {
    style: {
      fontSize: 12.5,
      color: 'var(--text-caption)',
      marginTop: 2
    }
  }, b.en, " \xB7 ", b.size), /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 6,
      marginTop: 9,
      flexWrap: 'wrap'
    }
  }, /*#__PURE__*/React.createElement(Badge, {
    tone: "gold",
    solid: true
  }, "\uD55C\uAD6D \uC778\uAE30 ", b.rank, "\uC704"), /*#__PURE__*/React.createElement(Badge, {
    tone: "neutral"
  }, "\uC6D4 ", b.costMonthly)))), /*#__PURE__*/React.createElement("div", {
    style: {
      padding: '0 16px 14px'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'baseline',
      marginBottom: 5
    }
  }, /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 12,
      fontWeight: 700,
      color: 'var(--text-muted)'
    }
  }, "\uB9E4\uCE6D \uC810\uC218"), /*#__PURE__*/React.createElement("span", {
    style: {
      fontSize: 15,
      fontWeight: 900,
      color: 'var(--brand)'
    }
  }, b.match, "%")), /*#__PURE__*/React.createElement("div", {
    style: {
      height: 8,
      borderRadius: 999,
      background: 'var(--mint-200)',
      overflow: 'hidden'
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: b.match + '%',
      height: '100%',
      borderRadius: 999,
      background: 'var(--brand-gradient)'
    }
  }))))))));
}
window.ResultScreen = ResultScreen;
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/mungmate_app/ResultScreen.jsx", error: String((e && e.message) || e) }); }

// ui_kits/mungmate_app/data.js
try { (() => {
/* MungMate app — sample data (from the chakhan-canine breed dataset + journey.py).
   Korean-market reinterpreted AKC traits. Scores are 1–5.
   No emoji: avatars use a monogram, insight cards rely on tone color. */

window.MM_DATA = {
  // ── Readiness diagnostic (후킹 질문) — provocative, assumption-busting ──
  diagnostic: [{
    q: '작은 강아지가 키우기 더 쉬울 거라 생각하세요?',
    hint: '말티즈·푸들 같은 인기 소형견을 떠올리며',
    options: [{
      label: '네, 작을수록 쉽죠',
      value: 'yes'
    }, {
      label: '꼭 그렇진 않을 것 같아요',
      value: 'no'
    }],
    truth: '사실, 소형견일수록 짖음·분리불안이 잦고 슬개골 탈구 위험이 높아요. 크기와 난이도는 별개예요.'
  }, {
    q: '이사 갈 집이 펫 금지면, 다른 집을 찾을 여유가 있으세요?',
    hint: '한국 임대 시장의 현실을 생각하며',
    options: [{
      label: '네, 강아지가 우선이에요',
      value: 'yes'
    }, {
      label: '솔직히 자신 없어요',
      value: 'no'
    }],
    truth: '주거 불안정은 한국 유기의 큰 원인이에요. 입양은 10년 이상의 약속이에요.'
  }, {
    q: '귀여운 강아지가 손을 물면, 어떻게 하시겠어요?',
    hint: '모든 강아지는 물 수 있어요',
    options: [{
      label: '훈련으로 고쳐나가요',
      value: 'yes'
    }, {
      label: '많이 당황스러울 것 같아요',
      value: 'no'
    }],
    truth: '문제 행동은 견종 탓이 아니라 훈련의 문제예요. 준비된 보호자에겐 해결 가능한 과제예요.'
  }],
  // ── Breed recommendations (matching result) ──
  breeds: [{
    id: 'sheltie',
    name: '셔틀랜드 쉽독',
    en: 'Shetland Sheepdog',
    nick: '셸티',
    mono: '셔',
    match: 92,
    rank: 29,
    size: '소형~중형',
    life: '12–14년',
    temperament: ['영리함', '활발함', '다정함'],
    summary: '스코틀랜드 셰틀랜드 제도 출신의 영리한 목양견. 가족에게 깊이 헌신하고 학습 의지가 매우 강해요.',
    costMonthly: '15–25만원',
    traits: [{
      label: '짖음',
      score: 5,
      word: '매우 높음',
      tone: 'hope'
    }, {
      label: '훈련 가능성',
      score: 5,
      word: '매우 쉬움',
      tone: 'good'
    }, {
      label: '활동량',
      score: 4,
      word: '높음',
      tone: 'hope'
    }, {
      label: '가족 친화',
      score: 5,
      word: '매우 다정',
      tone: 'good'
    }, {
      label: '털 빠짐',
      score: 3,
      word: '보통',
      tone: 'brand'
    }, {
      label: '낯선 사람',
      score: 2,
      word: '경계함',
      tone: 'brand'
    }],
    messages: [{
      tone: 'hope',
      title: '원래 잘 짖지만, 훈련으로 컨트롤 가능해요',
      text: '타고난 경계심으로 짖음이 많은 편이에요. 하지만 학습 의지가 강해서, 꾸준한 훈련으로 짖음을 컨트롤할 수 있어요. 공동주택에서도 충분히 함께 살 수 있어요.'
    }, {
      tone: 'hope',
      title: '활동량이 많은 견종이에요',
      text: '하루 1시간 이상의 산책·놀이가 필요해요. 충분히 운동시켜주면 실내에선 차분히 지내요.'
    }, {
      tone: 'good',
      title: '아이와 가족에게 다정한 견종이에요',
      text: '가족과의 친밀도가 높고, 어린 자녀와도 잘 어울려요. 안전한 가족견 후보예요.'
    }],
    founder: true
  }, {
    id: 'border-collie',
    name: '보더 콜리',
    en: 'Border Collie',
    nick: 'BC',
    mono: '보',
    match: 84,
    rank: 26,
    size: '중형',
    life: '12–15년',
    temperament: ['에너지', '다정함', '천재견'],
    summary: '세계에서 가장 영리한 견종. 일(Job)이 필요한 워킹독이라 충분한 자극이 핵심이에요.',
    costMonthly: '18–30만원',
    traits: [{
      label: '짖음',
      score: 3,
      word: '보통',
      tone: 'brand'
    }, {
      label: '훈련 가능성',
      score: 5,
      word: '매우 쉬움',
      tone: 'good'
    }, {
      label: '활동량',
      score: 5,
      word: '매우 높음',
      tone: 'hope'
    }, {
      label: '가족 친화',
      score: 4,
      word: '다정',
      tone: 'good'
    }],
    messages: [{
      tone: 'hope',
      title: '에너지가 매우 높은 워킹독이에요',
      text: '운동과 두뇌 자극이 부족하면 문제 행동이 생겨요. 산책 + 노즈워크 + 트릭 훈련을 함께 해주세요.'
    }, {
      tone: 'good',
      title: '다른 강아지와 잘 어울려요',
      text: '사회성이 좋아 강아지 놀이터에서도 무리 없이 어울려요.'
    }],
    founder: false
  }, {
    id: 'maltese',
    name: '말티즈',
    en: 'Maltese',
    nick: '말티즈',
    mono: '말',
    match: 71,
    rank: 1,
    size: '초소형',
    life: '12–15년',
    temperament: ['애교', '활발함', '예민함'],
    summary: '한국에서 가장 인기 있는 견종. 사랑스럽지만 데이터는 짖음·슬개골 위험을 경고해요.',
    costMonthly: '12–20만원',
    traits: [{
      label: '짖음',
      score: 4,
      word: '높음',
      tone: 'hope'
    }, {
      label: '훈련 가능성',
      score: 3,
      word: '보통',
      tone: 'brand'
    }, {
      label: '활동량',
      score: 3,
      word: '보통',
      tone: 'brand'
    }, {
      label: '가족 친화',
      score: 5,
      word: '매우 다정',
      tone: 'good'
    }],
    messages: [{
      tone: 'hope',
      title: '생각보다 잘 짖는 편이에요',
      text: '인기와 달리 경계 짖음이 잦아요. 어릴 때부터 사회화·분리불안 훈련을 해주면 충분히 관리돼요.'
    }, {
      tone: 'caution',
      title: '슬개골 탈구를 주의해주세요',
      text: '소형견 특성상 무릎 관절이 약해요. 미끄럼 방지 매트와 체중 관리가 중요해요.'
    }],
    founder: false
  }],
  // ── Founder testimony (from breed_messages.py) ──
  founderTestimony: '멍메이트 창업자의 셸티도 짖음이 매우 높은 견종이에요. 5년 훈련으로 지금은 짖지 않고, 물지 않고, 아이가 와서 눈을 찔러도 가만히 있어요. 좋은 견종이 따로 있는 게 아니라, 좋은 보호자가 만듭니다.'
};
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/mungmate_app/data.js", error: String((e && e.message) || e) }); }

// ui_kits/mungmate_app/shared.jsx
try { (() => {
/* MungMate app — shared chrome: Logo, TopBar, ProgressBar, PhoneFrame */

function Logo({
  size = 26,
  light = false
}) {
  const mark = Math.round(size * 1.55);
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      alignItems: 'center',
      gap: size * 0.42
    }
  }, /*#__PURE__*/React.createElement("div", {
    style: {
      width: mark,
      height: mark,
      borderRadius: mark * 0.3,
      background: light ? '#fff' : 'var(--brand-gradient)',
      color: light ? 'var(--brand)' : '#fff',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontWeight: 900,
      fontSize: mark * 0.48,
      boxShadow: light ? 'none' : 'var(--shadow-brand)',
      flexShrink: 0
    }
  }, "\uBA4D"), /*#__PURE__*/React.createElement("span", {
    style: {
      fontWeight: 900,
      fontSize: size,
      letterSpacing: '-0.02em',
      color: light ? '#fff' : 'var(--ink-900)'
    }
  }, "\uBA4D\uBA54\uC774\uD2B8"));
}
function TopBar({
  onBack,
  title,
  right
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      height: 56,
      flexShrink: 0,
      display: 'flex',
      alignItems: 'center',
      gap: 10,
      padding: '0 16px',
      background: 'var(--bg-app)',
      borderBottom: '1px solid var(--line-soft)',
      position: 'sticky',
      top: 0,
      zIndex: 5
    }
  }, onBack ? /*#__PURE__*/React.createElement("button", {
    onClick: onBack,
    "aria-label": "\uB4A4\uB85C",
    style: {
      width: 36,
      height: 36,
      border: 'none',
      background: 'var(--white)',
      borderRadius: 'var(--radius-md)',
      cursor: 'pointer',
      fontSize: 18,
      color: 'var(--ink-700)',
      boxShadow: 'var(--shadow-sm)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center'
    }
  }, "\u2039") : /*#__PURE__*/React.createElement(Logo, {
    size: 19
  }), title && /*#__PURE__*/React.createElement("span", {
    style: {
      fontWeight: 800,
      fontSize: 16,
      color: 'var(--ink-900)'
    }
  }, title), /*#__PURE__*/React.createElement("div", {
    style: {
      marginLeft: 'auto'
    }
  }, right));
}
function ProgressBar({
  step,
  total
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      display: 'flex',
      gap: 6,
      padding: '14px 20px 4px'
    }
  }, Array.from({
    length: total
  }).map((_, i) => /*#__PURE__*/React.createElement("div", {
    key: i,
    style: {
      flex: 1,
      height: 6,
      borderRadius: 999,
      background: i <= step ? 'var(--brand-gradient)' : 'var(--mint-200)',
      transition: 'background var(--dur-base) var(--ease-out)'
    }
  })));
}

/* Mobile frame — centers the app in a soft device shell */
function PhoneFrame({
  children
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      width: 412,
      height: 844,
      background: 'var(--bg-app)',
      borderRadius: 38,
      overflow: 'hidden',
      position: 'relative',
      boxShadow: '0 30px 80px rgba(91,64,48,0.28), 0 0 0 10px #2B2018, 0 0 0 11px #00000022',
      display: 'flex',
      flexDirection: 'column'
    }
  }, children);
}

/* Scroll region for a screen's body */
function ScreenBody({
  children,
  style = {}
}) {
  return /*#__PURE__*/React.createElement("div", {
    style: {
      flex: 1,
      overflowY: 'auto',
      WebkitOverflowScrolling: 'touch',
      ...style
    }
  }, children);
}
Object.assign(window, {
  Logo,
  TopBar,
  ProgressBar,
  PhoneFrame,
  ScreenBody
});
})(); } catch (e) { __ds_ns.__errors.push({ path: "ui_kits/mungmate_app/shared.jsx", error: String((e && e.message) || e) }); }

__ds_ns.Card = __ds_scope.Card;

__ds_ns.TraitCard = __ds_scope.TraitCard;

__ds_ns.TraitMeter = __ds_scope.TraitMeter;

__ds_ns.Badge = __ds_scope.Badge;

__ds_ns.Button = __ds_scope.Button;

__ds_ns.Chip = __ds_scope.Chip;

__ds_ns.ChoiceCard = __ds_scope.ChoiceCard;

})();

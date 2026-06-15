Primary call-to-action for MungMate flows — use for the one main action on a screen (진단 시작, 매칭 보기, 다음).

```jsx
<Button variant="gradient" size="lg" full onClick={start}>
  준비도 진단 시작하기
</Button>
```

Variants: `primary` (solid coral), `gradient` (coral→sunset, for the hero CTA), `secondary` (white + warm border), `ghost` (coral text only). Sizes `sm|md|lg`. Press shrinks to 0.97; hover lifts. Pass `full` for sticky bottom CTAs. An optional `icon` (Lucide node) is supported but unused by default.

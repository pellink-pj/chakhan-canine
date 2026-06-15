Large selectable answer for the readiness diagnostic and lifestyle questions. 64px+ hit target, coral selection state with a check.

```jsx
<ChoiceCard label="네, 있어요" sub="마음에 둔 견종이 있어요"
  selected={ans === 'yes'} onClick={() => setAns('yes')} />
<ChoiceCard label="잘 모르겠어요" sub="추천받고 싶어요"
  selected={ans === 'no'} onClick={() => setAns('no')} />
```

Stack in a column with gap. Always give a clear `selected` state — this drives the whole flow. An optional `icon` (Lucide node) is supported but unused by default.

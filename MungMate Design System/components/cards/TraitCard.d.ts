import * as React from 'react';

/**
 * Signature hope-first insight card — emoji + headline + explanation, tinted
 * and accented by tone. Mirrors the output shape of breed_messages.py.
 * @startingPoint section="Cards" subtitle="Hope-first trait insight" viewport="700x180"
 */
export interface TraitCardProps {
  /** Optional leading icon (e.g. a Lucide node). Omitted by default — the brand uses no emoji. */
  icon?: React.ReactNode;
  /** Headline in brand voice — e.g. "원래 잘 짖지만, 훈련으로 컨트롤 가능해요". */
  title: string;
  /** Supporting explanation. */
  text?: string;
  /**
   * good = fine as-is · hope = overcomeable with training · caution = think hard.
   * @default "hope"
   */
  tone?: 'good' | 'hope' | 'caution';
  style?: React.CSSProperties;
}

export function TraitCard(props: TraitCardProps): JSX.Element;

import * as React from 'react';

/**
 * 1–5 trait meter — label + dot scale + plain-Korean scale word.
 * @startingPoint section="Cards" subtitle="1–5 trait score row" viewport="700x120"
 */
export interface TraitMeterProps {
  /** Trait name, e.g. "짖음" / "활동량". */
  label: string;
  /** Filled count. @default 3 */
  score?: number;
  /** @default 5 */
  max?: number;
  /** Plain-Korean label for the score, e.g. "매우 높음". */
  scaleWord?: string;
  /** Dot color. @default "brand" */
  tone?: 'brand' | 'good' | 'hope' | 'caution';
  style?: React.CSSProperties;
}

export function TraitMeter(props: TraitMeterProps): JSX.Element;

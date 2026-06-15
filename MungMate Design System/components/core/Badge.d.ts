import * as React from 'react';

/**
 * Small pill label — trait tags, 착한개 certification mark, popularity ranks.
 * @startingPoint section="Core" subtitle="Tone-aware pill badge" viewport="700x120"
 */
export interface BadgeProps {
  children: React.ReactNode;
  /** @default "brand" */
  tone?: 'brand' | 'good' | 'hope' | 'caution' | 'info' | 'gold' | 'neutral';
  /** Optional leading icon (Lucide node). Omitted by default. */
  icon?: React.ReactNode;
  /** Filled instead of tinted. @default false */
  solid?: boolean;
  style?: React.CSSProperties;
}

export function Badge(props: BadgeProps): JSX.Element;

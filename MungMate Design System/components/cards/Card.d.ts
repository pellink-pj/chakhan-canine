import * as React from 'react';

/**
 * Base surface card — white on cream, soft warm shadow, 20px radius.
 * @startingPoint section="Cards" subtitle="Base elevated surface" viewport="700x200"
 */
export interface CardProps {
  children: React.ReactNode;
  /** CSS padding. @default "var(--space-6)" */
  padding?: string;
  /** Hover-lift + pointer. @default false */
  interactive?: boolean;
  onClick?: (e: React.MouseEvent<HTMLDivElement>) => void;
  style?: React.CSSProperties;
}

export function Card(props: CardProps): JSX.Element;

import * as React from 'react';

/**
 * Big tap-target answer card for the readiness diagnostic (후킹 질문).
 * @startingPoint section="Forms" subtitle="Large selectable answer" viewport="700x200"
 */
export interface ChoiceCardProps {
  /** Optional leading icon (Lucide node). */
  icon?: React.ReactNode;
  /** Answer text. */
  label: string;
  /** Optional secondary line. */
  sub?: string;
  selected?: boolean;
  onClick?: (e: React.MouseEvent<HTMLButtonElement>) => void;
  style?: React.CSSProperties;
}

export function ChoiceCard(props: ChoiceCardProps): JSX.Element;

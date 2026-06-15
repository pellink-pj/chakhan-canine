import * as React from 'react';

/**
 * MungMate primary button — coral / gradient / secondary / ghost.
 * @startingPoint section="Core" subtitle="Coral CTA with tactile press" viewport="700x150"
 */
export interface ButtonProps {
  children: React.ReactNode;
  /** Visual style. @default "primary" */
  variant?: 'primary' | 'gradient' | 'secondary' | 'ghost';
  /** @default "md" */
  size?: 'sm' | 'md' | 'lg';
  /** Stretch to container width. @default false */
  full?: boolean;
  /** Leading icon — a Lucide node. */
  icon?: React.ReactNode;
  disabled?: boolean;
  onClick?: (e: React.MouseEvent<HTMLButtonElement>) => void;
  type?: 'button' | 'submit' | 'reset';
  style?: React.CSSProperties;
}

export function Button(props: ButtonProps): JSX.Element;

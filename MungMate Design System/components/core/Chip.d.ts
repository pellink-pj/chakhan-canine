import * as React from 'react';

/** Selectable filter/option chip. Coral-tinted when selected. */
export interface ChipProps {
  children: React.ReactNode;
  selected?: boolean;
  icon?: React.ReactNode;
  onClick?: (e: React.MouseEvent<HTMLButtonElement>) => void;
  style?: React.CSSProperties;
}

export function Chip(props: ChipProps): JSX.Element;

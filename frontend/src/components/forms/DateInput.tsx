'use client';

import { useState, useEffect } from 'react';
import { isoToDisplay, displayToISO } from '@/lib/utils';

interface Props {
  value:       string;
  onChange:    (iso: string) => void;
  required?:   boolean;
  placeholder?: string;
  className?:  string;
}

export function DateInput({ value, onChange, required, placeholder = 'dd/mm/aaaa', className }: Props) {
  const [disp, setDisp] = useState(() => isoToDisplay(value));

  useEffect(() => {
    setDisp(isoToDisplay(value));
  }, [value]);

  const handle = (e: React.ChangeEvent<HTMLInputElement>) => {
    const raw = e.target.value.replace(/\D/g, '').slice(0, 8);
    let masked = raw;
    if (raw.length > 2) masked = `${raw.slice(0, 2)}/${raw.slice(2)}`;
    if (raw.length > 4) masked = `${raw.slice(0, 2)}/${raw.slice(2, 4)}/${raw.slice(4)}`;
    setDisp(masked);
    if (raw.length === 8) {
      const iso = displayToISO(masked);
      if (iso) onChange(iso);
    } else if (raw.length === 0) {
      onChange('');
    }
  };

  return (
    <input
      type="text"
      value={disp === '—' ? '' : disp}
      onChange={handle}
      placeholder={placeholder}
      required={required}
      inputMode="numeric"
      className={className}
    />
  );
}

'use client';

import { useState } from 'react';

export function useMoney(initial = 0) {
  const [cents, setCents] = useState(() => Math.round((Number(initial) || 0) * 100));

  const display = (() => {
    const s   = String(cents).padStart(3, '0');
    const int = parseInt(s.slice(0, -2), 10);
    const dec = s.slice(-2);
    return `${int.toLocaleString('pt-BR')},${dec}`;
  })();

  const onChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const digits = e.target.value.replace(/\D/g, '');
    setCents(parseInt(digits || '0', 10));
  };

  const reset = () => setCents(0);
  const value = cents / 100;
  const isEmpty = cents === 0;

  return { display, onChange, reset, value, isEmpty };
}

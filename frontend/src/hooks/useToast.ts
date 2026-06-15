'use client';

import { useState, useCallback } from 'react';

export type ToastType = 'ok' | 'err';

export interface ToastState {
  msg:  string;
  type: ToastType;
}

export function useToast() {
  const [toast, setToast] = useState<ToastState | null>(null);

  const show = useCallback((msg: string, type: ToastType = 'ok') => {
    setToast({ msg, type });
  }, []);

  const hide = useCallback(() => setToast(null), []);

  return { toast, show, hide };
}

'use client';

import { useEffect } from 'react';
import { cn } from '@/lib/utils';

interface Props {
  msg:     string;
  type:    'ok' | 'err';
  onClose: () => void;
}

export function Toast({ msg, type, onClose }: Props) {
  useEffect(() => {
    const t = setTimeout(onClose, 3500);
    return () => clearTimeout(t);
  }, [onClose]);

  return (
    <div
      className={cn(
        'fixed bottom-6 right-6 z-50 flex items-center gap-2 rounded-xl px-5 py-3',
        'text-sm font-bold text-white shadow-2xl max-w-sm',
        'animate-[slideUp_0.2s_ease]',
        type === 'ok' ? 'bg-brand-blue' : 'bg-brand-red'
      )}
    >
      <span>{type === 'ok' ? '✓' : '✕'}</span>
      <span className="flex-1">{msg}</span>
      <button
        onClick={onClose}
        className="ml-1 text-lg leading-none opacity-70 hover:opacity-100 transition-opacity"
      >
        ×
      </button>
    </div>
  );
}

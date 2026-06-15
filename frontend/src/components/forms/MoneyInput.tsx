'use client';

import { useMoney } from '@/hooks/useMoney';

interface Props {
  value:    ReturnType<typeof useMoney>;
  className?: string;
}

export function MoneyInput({ value: money, className }: Props) {
  return (
    <div className={`flex items-center border rounded-lg overflow-hidden focus-within:ring-2 focus-within:ring-brand-blue/30 ${className ?? ''}`}>
      <span className="px-3 py-2.5 text-sm font-semibold text-slate-500 bg-slate-50 dark:bg-slate-800 border-r border-slate-200 dark:border-slate-700 select-none">
        R$
      </span>
      <input
        value={money.display}
        onChange={money.onChange}
        inputMode="numeric"
        placeholder="0,00"
        className="flex-1 px-3 py-2.5 border-none rounded-none text-sm bg-white dark:bg-slate-900 outline-none text-slate-800 dark:text-slate-100 font-mono"
      />
    </div>
  );
}

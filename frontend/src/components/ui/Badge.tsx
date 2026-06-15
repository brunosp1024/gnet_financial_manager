import { cn } from '@/lib/utils';

const variantMap: Record<string, string> = {
  pix:              'bg-sky-100 text-sky-700 dark:bg-sky-900/40 dark:text-sky-300',
  cash:             'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300',
  card:             'bg-violet-100 text-violet-700 dark:bg-violet-900/40 dark:text-violet-300',
  clt:              'bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300',
  service_provider: 'bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300',
  admin:            'bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-300',
  gerente:          'bg-orange-100 text-orange-700 dark:bg-orange-900/40 dark:text-orange-300',
  financeiro:       'bg-teal-100 text-teal-700 dark:bg-teal-900/40 dark:text-teal-300',
  active:           'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/40 dark:text-emerald-300',
  inactive:         'bg-slate-100 text-slate-500 dark:bg-slate-800 dark:text-slate-400',
};

interface Props {
  variant?: string;
  children: React.ReactNode;
  className?: string;
}

export function Badge({ variant = '', children, className }: Props) {
  const key = variant.toLowerCase();
  return (
    <span
      className={cn(
        'inline-flex items-center px-2 py-0.5 rounded-full text-xs font-semibold',
        variantMap[key] ?? 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300',
        className
      )}
    >
      {children}
    </span>
  );
}

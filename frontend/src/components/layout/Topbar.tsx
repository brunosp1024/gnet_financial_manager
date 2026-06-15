'use client';

import { usePathname } from 'next/navigation';
import { useRef, useState, useEffect } from 'react';
import { useAuth } from '@/hooks/useAuth';
import { initials } from '@/lib/utils';

const PAGE_TITLES: Record<string, string> = {
  '/dashboard': 'Dashboard',
  '/cashflow':  'Fluxo de Caixa',
  '/customers': 'Clientes',
  '/employees': 'Funcionários',
  '/users':     'Usuários',
};

const NOTIFS = [
  { msg: '3 mensalidades vencem hoje', time: 'Agora',    dot: true },
  { msg: 'Relatório mensal disponível', time: '1h atrás', dot: true },
  { msg: 'Novo cliente cadastrado',    time: '2h atrás', dot: false },
];

interface Props {
  theme:    'light' | 'dark';
  onToggle: () => void;
}

export function Topbar({ theme, onToggle }: Props) {
  const pathname = usePathname();
  const { user } = useAuth();
  const [notif,    setNotif]    = useState(false);
  const notifRef   = useRef<HTMLDivElement>(null);

  const title = PAGE_TITLES[pathname] ?? 'Dashboard';

  useEffect(() => {
    const h = (e: MouseEvent) => {
      if (notifRef.current && !notifRef.current.contains(e.target as Node)) setNotif(false);
    };
    document.addEventListener('mousedown', h);
    return () => document.removeEventListener('mousedown', h);
  }, []);

  const fullName = `${user?.first_name ?? ''} ${user?.last_name ?? ''}`.trim();
  const group    = user?.group ?? '';

  return (
    <header className="sticky top-0 z-30 flex items-center justify-between px-6 h-[64px] bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-100 dark:border-slate-800 shadow-sm">
      {/* Left */}
      <div>
        <div className="font-display font-bold text-base text-slate-800 dark:text-slate-100">{title}</div>
        <div className="text-xs text-slate-400 dark:text-slate-500 font-body">GlobalNet&#39;I › {title}</div>
      </div>

      {/* Right */}
      <div className="flex items-center gap-2">
        {/* Theme */}
        <button
          onClick={onToggle}
          className="icon-btn"
          title="Alternar tema"
        >
          {theme === 'dark' ? '☀️' : '🌙'}
        </button>

        {/* Notifications */}
        <div className="relative" ref={notifRef}>
          <button className="icon-btn relative" onClick={() => setNotif((n) => !n)} title="Notificações">
            🔔
            <span className="absolute top-1 right-1 w-2 h-2 rounded-full bg-brand-red border-2 border-white dark:border-slate-900" />
          </button>

          {notif && (
            <div className="absolute right-0 top-full mt-2 w-72 bg-white dark:bg-slate-900 rounded-2xl shadow-2xl border border-slate-100 dark:border-slate-800 z-50 overflow-hidden">
              <div className="px-4 py-3 border-b border-slate-100 dark:border-slate-800 font-display font-bold text-sm text-slate-700 dark:text-slate-200">
                🔔 Notificações
              </div>
              {NOTIFS.map((n, i) => (
                <div
                  key={i}
                  className="flex items-start gap-3 px-4 py-3 hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors"
                >
                  {n.dot && (
                    <span className="mt-1.5 w-2 h-2 rounded-full bg-brand-blue flex-shrink-0" />
                  )}
                  {!n.dot && <span className="w-2" />}
                  <div className="flex-1">
                    <div className="text-sm text-slate-700 dark:text-slate-200 font-medium">{n.msg}</div>
                    <div className="text-xs text-slate-400 dark:text-slate-500 mt-0.5">{n.time}</div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* User pill */}
        <div className="flex items-center gap-2.5 pl-2 border-l border-slate-100 dark:border-slate-800 ml-1">
          <div className="w-9 h-9 rounded-full bg-gradient-to-br from-brand-blue to-brand-blue-l flex items-center justify-center text-white font-bold text-sm flex-shrink-0">
            {initials(fullName)}
          </div>
          <div className="hidden sm:block">
            <div className="text-sm font-semibold text-slate-700 dark:text-slate-200 leading-tight">
              {user?.first_name ?? 'Usuário'}
            </div>
            <div className="text-xs text-slate-400 dark:text-slate-500">{group}</div>
          </div>
        </div>
      </div>
    </header>
  );
}

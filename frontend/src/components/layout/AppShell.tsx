'use client';

import { useState, useEffect } from 'react';
import { Sidebar } from './Sidebar';
import { Topbar }  from './Topbar';
import { Footer }  from './Footer';
import { Toast }   from '@/components/ui/Toast';
import { useToast } from '@/hooks/useToast';
import { ToastContext } from '@/hooks/useToastContext';

export function AppShell({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');
  const { toast, show, hide } = useToast();

  useEffect(() => {
    const saved = (localStorage.getItem('gn_theme') as 'light' | 'dark') || 'light';
    setTheme(saved);
    document.documentElement.classList.toggle('dark', saved === 'dark');
  }, []);

  const toggleTheme = () => {
    setTheme((t) => {
      const next = t === 'dark' ? 'light' : 'dark';
      localStorage.setItem('gn_theme', next);
      document.documentElement.classList.toggle('dark', next === 'dark');
      return next;
    });
  };

  return (
    <ToastContext.Provider value={show}>
      <div className="flex h-screen overflow-hidden bg-slate-200 dark:bg-slate-950 font-body">
        <Sidebar />
        <div className="flex flex-col flex-1 overflow-hidden">
          <Topbar theme={theme} onToggle={toggleTheme} />
          <main className="flex-1 overflow-y-auto p-6">
            {children}
          </main>
          <Footer />
        </div>
        {toast && <Toast msg={toast.msg} type={toast.type} onClose={hide} />}
      </div>
    </ToastContext.Provider>
  );
}

'use client';

import { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { User } from '@/types';
import { authService } from '@/services/auth.service';
import Cookies from 'js-cookie';

interface AuthContextValue {
  user:         User | null;
  isLoading:    boolean;
  login:        (username: string, password: string) => Promise<void>;
  logout:       () => Promise<void>;
  hasGroup:     (group: string) => boolean;
  isAdmin:      boolean;
  isGerente:    boolean;
  isFinanceiro: boolean;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser]           = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Restore session on mount
  useEffect(() => {
    const restore = async () => {
      if (!Cookies.get('gn_access')) { setIsLoading(false); return; }
      try {
        const me = await authService.me();
        setUser(me);
      } catch {
        Cookies.remove('gn_access');
        Cookies.remove('gn_refresh');
      } finally {
        setIsLoading(false);
      }
    };
    restore();
  }, []);

  const login = async (username: string, password: string) => {
    const { user } = await authService.login({ username, password });
    setUser(user);
  };

  const logout = async () => {
    await authService.logout();
    setUser(null);
  };

  const hasGroup    = (g: string) => user?.group === g;
  const isAdmin     = hasGroup('ADMIN');
  const isGerente   = hasGroup('GERENTE');
  const isFinanceiro= hasGroup('FINANCEIRO');

  return (
    <AuthContext.Provider value={{ user, isLoading, login, logout, hasGroup, isAdmin, isGerente, isFinanceiro }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used within AuthProvider');
  return ctx;
}

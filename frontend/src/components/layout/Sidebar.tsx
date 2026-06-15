'use client';

import { usePathname, useRouter } from 'next/navigation';
import { useState } from 'react';
import { cn } from '@/lib/utils';
import { useAuth } from '@/hooks/useAuth';
import { LOGO_BASE64 } from '@/lib/logo';
import '@/styles/sidebar.css';

interface NavItem {
  id:    string;
  href:  string;
  icon:  string;
  label: string;
  sec:   string;
}

export function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);
  const pathname = usePathname();
  const router   = useRouter();
  const { user, logout, isAdmin, isGerente } = useAuth();

  const canSeeUsers = isAdmin || isGerente;

  const navItems: NavItem[] = [
    { id: 'dashboard', href: '/dashboard',  icon: '📊', label: 'Dashboard',      sec: 'GERAL' },
    { id: 'cashflow',  href: '/cashflow',   icon: '💰', label: 'Fluxo de Caixa', sec: 'FINANCEIRO' },
    { id: 'customers', href: '/customers',  icon: '👥', label: 'Clientes',        sec: 'CADASTROS' },
    { id: 'employees', href: '/employees',  icon: '🏢', label: 'Funcionários',    sec: 'CADASTROS' },
    ...(canSeeUsers
      ? [{ id: 'users', href: '/users', icon: '🔐', label: 'Usuários', sec: 'ADMINISTRAÇÃO' }]
      : []),
  ];

  const sections = [...new Set(navItems.map((i) => i.sec))];

  const handleLogout = async () => {
    await logout();
    router.replace('/login');
  };

  return (
    <aside className={cn('sidebar', collapsed ? 'sidebar-collapsed' : 'sidebar-expanded')}>
      {/* Logo */}
      <div className="sidebar-logo">
        <img
          src={LOGO_BASE64}
          alt="GlobalNet'I"
          className={cn(
            'sidebar-logo-img',
            collapsed ? 'sidebar-logo-img-collapsed' : 'sidebar-logo-img-expanded'
          )}
        />
        <div
          className={cn(
            'sidebar-logo-text',
            collapsed ? 'sidebar-logo-text-collapsed' : 'sidebar-logo-text-expanded'
          )}
        >
          <div className="sidebar-logo-title">
            GLOBAL<span className="text-brand-red-l">NET&#39;I</span>
          </div>
          <div className="sidebar-logo-sub">Provedor de Internet</div>
        </div>
        <button
          onClick={() => setCollapsed((c) => !c)}
          className={'sidebar-toggle'}
        >
          {collapsed ? '›' : '‹'}
        </button>
      </div>

      {/* Nav */}
      <nav className="sidebar-nav">
        {sections.map((sec) => (
          <div key={sec}>
            {!collapsed && (
              <div className="sidebar-section-label">{sec}</div>
            )}
            {navItems
              .filter((i) => i.sec === sec)
              .map((item) => {
                const active = pathname.startsWith(item.href);
                return (
                  <button
                    key={item.id}
                    onClick={() => router.push(item.href)}
                    title={collapsed ? item.label : undefined}
                    className={cn(
                      'sidebar-nav-btn',
                      active && 'active',
                      collapsed && 'collapsed'
                    )}
                  >
                    <span className="sidebar-nav-icon">{item.icon}</span>
                    {!collapsed && <span className="sidebar-nav-label">{item.label}</span>}
                  </button>
                );
              })}
          </div>
        ))}
      </nav>

      {/* Footer */}
      <div className="sidebar-footer">
        <button
          onClick={handleLogout}
          className={cn(
            'sidebar-footer-btn',
            collapsed && 'collapsed'
          )}
          title={collapsed ? 'Sair' : undefined}
        >
          <span className="sidebar-footer-icon">🚪</span>
          {!collapsed && <span className="sidebar-footer-label">Sair</span>}
        </button>
      </div>
    </aside>
  );
}

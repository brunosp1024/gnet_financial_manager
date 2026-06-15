'use client';

import { useState, FormEvent } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import { LOGO_BASE64 } from '@/lib/logo';
import '@/styles/login.css';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error,    setError]    = useState('');
  const [loading,  setLoading]  = useState(false);
  const { login } = useAuth();
  const router    = useRouter();

  const submit = async (e: FormEvent) => {
    e.preventDefault();  // Avoid page reload
    setError('');
    setLoading(true);
    try {
      await login(username, password);
      router.replace('/dashboard');
    } catch {
      setError('Usuário ou senha inválidos. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      {/* Painel esquerdo (desktop) */}
      <div className="login-left-panel">
        <div className="decor-circle-top" />
        <div className="decor-circle-bottom" />
        <div className="decor-circle-mid" />
        <div className="login-brand-content">
          <img src="/images/logo.png" alt="GlobalNet'I" className="login-brand-logo" />
          <div className="login-brand-name">
            GLOBAL<span className="login-brand-name-red">NET&#39;I</span>
          </div>
          <div className="login-brand-subtitle">Provedor de Internet</div>
          <div className="login-brand-box">
            <p>
              <strong className="login-brand-box-strong">Conectando o mundo a você!</strong><br/>
              Gerencie seu provedor com eficiência e segurança total.
            </p>
          </div>
        </div>
      </div>

      {/* Painel direito (formulário) */}
      <div className="login-right-panel">
        <div className="login-form-wrapper">
          {/* Mobile logo */}
          <div className="login-mobile-logo">
            <img src={LOGO_BASE64} alt="" className="login-mobile-logo-img" />
            <div className="login-mobile-logo-name">
              GLOBAL<span className="login-mobile-logo-name-red">NET&#39;I</span>
            </div>
          </div>
          {/* Login card */}
          <div className="login-card">
            <h1 className="login-title">Entrar no sistema</h1>
            <p className="login-subtitle">Entre com suas credenciais de acesso</p>
            {error && (
              <div className="login-error">
                <span>⚠</span> {error}
              </div>
            )}
            <form onSubmit={submit} className="login-form">
              <div className="login-form-group">
                <label htmlFor="username" className="login-label">Usuário</label>
                <input
                  id="username"
                  type="text"
                  placeholder="admin"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  required
                  autoFocus
                  className="login-input"
                />
              </div>
              <div className="login-form-group">
                <label htmlFor="password" className="login-label">Senha</label>
                <input
                  id="password"
                  type="password"
                  placeholder="••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  className="login-input"
                />
              </div>
              <button type="submit" disabled={loading} className="login-submit-btn">
                {loading ? 'Entrando…' : 'Entrar'}
              </button>
            </form>
          </div>
        </div>
      </div>
    </div>
  );
}

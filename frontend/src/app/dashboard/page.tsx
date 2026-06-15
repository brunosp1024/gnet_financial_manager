'use client';

import { useState, useEffect, useCallback } from 'react';
import { financeService } from '@/services/finance.service';
import { DashboardSummary } from '@/types';
import { fmtMoney, CAT_LABEL, BRAND_COLORS } from '@/lib/utils';
import { DateInput } from '@/components/forms/DateInput';

export default function DashboardPage() {
  const [summary,  setSummary]  = useState<DashboardSummary | null>(null);
  const [loading,  setLoading]  = useState(true);
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo,   setDateTo]   = useState('');

  const load = useCallback(async (df = dateFrom, dt = dateTo) => {
    setLoading(true);
    try {
      const data = await financeService.getDashboard({
        date_from: df || undefined,
        date_to:   dt || undefined,
      });
      setSummary(data);
    } catch { /* noop */ }
    finally { setLoading(false); }
  }, [dateFrom, dateTo]);

  useEffect(() => { load(); }, []); // eslint-disable-line

  const cats = summary?.by_category
    ? summary.by_category.map((c) => ({
        name:  CAT_LABEL[c.category] ?? c.category,
        value: c.total,
        count: c.count,
      }))
    : [];

  const total = summary ? summary.income_total + summary.expense_total : 0;

  const kpis = summary
    ? [
        { icon: '📥', label: 'Total Entradas', value: fmtMoney(summary.income_total),  color: 'text-brand-blue',  bg: 'bg-blue-50 dark:bg-blue-950/30',   border: 'border-blue-100 dark:border-blue-900' },
        { icon: '📤', label: 'Total Saídas',   value: fmtMoney(summary.expense_total), color: 'text-brand-red',   bg: 'bg-red-50 dark:bg-red-950/30',     border: 'border-red-100 dark:border-red-900' },
        { icon: '⚖️', label: 'Saldo',          value: fmtMoney(summary.balance),       color: summary.balance >= 0 ? 'text-brand-blue' : 'text-brand-red', bg: 'bg-slate-50 dark:bg-slate-800/50', border: 'border-slate-100 dark:border-slate-700' },
        { icon: '📋', label: 'Transações',     value: summary.transaction_count,       color: 'text-slate-700 dark:text-slate-200', bg: 'bg-slate-50 dark:bg-slate-800/50', border: 'border-slate-100 dark:border-slate-700' },
      ]
    : [];

  return (
    <div>
      {/* Header */}
      <div className="page-header">
        <div>
          <h1 className="page-title">📊 Dashboard</h1>
          <p className="page-sub">Visão geral do fluxo financeiro</p>
        </div>
      </div>

      {/* Filters */}
      <div className="filter-bar">
        <div className="field-group">
          <label>Data Inicial</label>
          <DateInput value={dateFrom} onChange={setDateFrom} />
        </div>
        <div className="field-group">
          <label>Data Final</label>
          <DateInput value={dateTo} onChange={setDateTo} />
        </div>
        <button className="btn btn-primary btn-sm self-end" onClick={() => load()}>Filtrar</button>
        <button
          className="btn btn-secondary btn-sm self-end"
          onClick={() => { setDateFrom(''); setDateTo(''); load('', ''); }}
        >
          Limpar
        </button>
      </div>

      {loading ? (
        <div className="flex justify-center py-20">
          <div className="w-8 h-8 rounded-full border-4 border-slate-200 border-t-brand-blue animate-spin" />
        </div>
      ) : summary && (
        <>
          {/* KPIs */}
          <div className="stats-grid">
            {kpis.map((k, i) => (
              <div key={i} className={`stat-card border ${k.bg} ${k.border}`}>
                <div className="text-2xl">{k.icon}</div>
                <div className="text-xs font-semibold text-slate-400 dark:text-slate-500 uppercase tracking-wide">{k.label}</div>
                <div className={`font-display font-bold text-xl ${k.color}`}>{k.value}</div>
              </div>
            ))}
          </div>

          {/* Category table */}
          {cats.length > 0 && (
            <div className="card">
              <div className="px-6 py-4 border-b border-slate-100 dark:border-slate-800">
                <h2 className="section-title mb-0">Breakdown por Categoria</h2>
              </div>
              <div className="table-wrap">
                <table>
                  <thead>
                    <tr>
                      <th>Categoria</th>
                      <th>Lançamentos</th>
                      <th>Total</th>
                      <th style={{ minWidth: 180 }}>Participação</th>
                    </tr>
                  </thead>
                  <tbody>
                    {cats.sort((a, b) => b.value - a.value).map((c, i) => {
                      const pct = total ? Math.min(100, (c.value / total) * 100) : 0;
                      return (
                        <tr key={i}>
                          <td>
                            <div className="flex items-center gap-2 font-semibold">
                              <span
                                className="w-2.5 h-2.5 rounded-full flex-shrink-0"
                                style={{ background: BRAND_COLORS[i % BRAND_COLORS.length] }}
                              />
                              {c.name}
                            </div>
                          </td>
                          <td className="text-slate-400 dark:text-slate-500">{c.count}</td>
                          <td className="font-bold font-display">{fmtMoney(c.value)}</td>
                          <td>
                            <div className="flex items-center gap-2">
                              <div className="prog-bar flex-1">
                                <div
                                  className="prog-fill"
                                  style={{
                                    width: `${pct}%`,
                                    background: BRAND_COLORS[i % BRAND_COLORS.length],
                                  }}
                                />
                              </div>
                              <span className="text-xs text-slate-400 dark:text-slate-500 w-10 text-right font-semibold">
                                {pct.toFixed(1)}%
                              </span>
                            </div>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}

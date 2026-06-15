'use client';

import { Badge } from '@/components/ui/Badge';
import { Modal } from '@/components/ui/Modal';
import { useToastContext } from '@/hooks/useToastContext';
import { CAT_LABEL, fmtMoney, isoToDisplay, PAY_LABEL } from '@/lib/utils';
import { DailyReport } from '@/types';

type Props = {
  report: DailyReport;
  onClose: () => void;
};

export function ReportModal({ report, onClose }: Props) {
  const toast = useToastContext();
  const inc = report.transactions.filter((t) => t.type === 'INCOME');
  const exp = report.transactions.filter((t) => t.type === 'EXPENSE');
  const now = new Date();
  const hora = now.toLocaleTimeString('pt-BR', { hour: '2-digit', minute: '2-digit' });

  const txtPlain = `
    RELATÓRIO DIÁRIO — GlobalNet'I
    Data: ${isoToDisplay(report.date)}  |  Emitido às ${hora}
    ENTRADAS (${inc.length})
    ${inc.length ? inc.map((t) => `  • ${t.description}\n    ${CAT_LABEL[t.category]} | ${PAY_LABEL[t.payment_method] ?? ''} | ${fmtMoney(t.value)}`).join('\n') : '  Nenhuma entrada.'}
    SAÍDAS (${exp.length})
    ${exp.length ? exp.map((t) => `  • ${t.description}\n    ${CAT_LABEL[t.category]} | ${fmtMoney(t.value)}`).join('\n') : '  Nenhuma saída.'}
    ─────────────────────────────────
      Total Entradas:  ${fmtMoney(report.total_income)}
      Total Saídas:    ${fmtMoney(report.total_expense)}
      Saldo do Dia:    ${fmtMoney(report.balance)}
    ─────────────────────────────────
    GlobalNet'I — Provedor de Internet
  `.trim();

  const kpis = [
    { label: '📥 Entradas', val: fmtMoney(report.total_income), pos: true },
    { label: '📤 Saídas', val: fmtMoney(report.total_expense), pos: false },
    { label: report.balance >= 0 ? '✅ Saldo' : '⚠️ Saldo', val: fmtMoney(report.balance), pos: report.balance >= 0 },
  ];

  return (
    <Modal
      title="📄 Relatório do Dia"
      onClose={onClose}
      wide
      footer={
        <>
          <button
            className="btn btn-secondary btn-sm"
            onClick={() => { navigator.clipboard.writeText(txtPlain); toast('Relatório copiado!', 'ok'); }}
          >
            📋 Copiar texto
          </button>
          <button className="btn btn-primary btn-sm" onClick={onClose}>Fechar</button>
        </>
      }
    >
      <div className="grid grid-cols-3 gap-3 mb-5">
        {kpis.map((k, i) => (
          <div
            key={i}
            className={`rounded-xl p-4 border ${k.pos ? 'bg-blue-50 border-blue-100 dark:bg-blue-950/20 dark:border-blue-900' : 'bg-red-50 border-red-100 dark:bg-red-950/20 dark:border-red-900'}`}
          >
            <div className={`text-xs font-semibold mb-1 ${k.pos ? 'text-brand-blue' : 'text-brand-red'}`}>{k.label}</div>
            <div className={`font-display font-bold text-lg ${k.pos ? 'text-brand-blue' : 'text-brand-red'}`}>{k.val}</div>
          </div>
        ))}
      </div>

      {[
        { items: inc, title: 'Entradas', icon: '📥', pos: true },
        { items: exp, title: 'Saídas', icon: '📤', pos: false },
      ].map(({ items, title, icon, pos }) => (
        <div key={title} className="mb-4">
          <div className={`flex items-center justify-between px-4 py-2.5 rounded-xl mb-2 ${pos ? 'bg-blue-50 dark:bg-blue-950/20' : 'bg-red-50 dark:bg-red-950/20'}`}>
            <span className={`text-sm font-bold ${pos ? 'text-brand-blue' : 'text-brand-red'}`}>
              {icon} {title} <span className="font-normal opacity-60">({items.length})</span>
            </span>
            <span className={`font-display font-bold text-sm ${pos ? 'text-brand-blue' : 'text-brand-red'}`}>
              {fmtMoney(pos ? report.total_income : report.total_expense)}
            </span>
          </div>
          {items.length === 0
            ? <div className="text-sm text-slate-400 dark:text-slate-600 px-2 py-2">Nenhum lançamento.</div>
            : items.map((t) => (
                <div key={t.id} className="flex items-center justify-between py-2 px-3 rounded-lg hover:bg-slate-50 dark:hover:bg-slate-800/30 transition-colors">
                  <div>
                    <div className="text-sm font-medium text-slate-700 dark:text-slate-200">{t.description}</div>
                    <div className="flex items-center gap-2 mt-0.5">
                      <span className="text-xs text-slate-400">{CAT_LABEL[t.category]}</span>
                      {t.payment_method && (
                        <>
                          <span className="text-slate-300 dark:text-slate-700">·</span>
                          <Badge variant={t.payment_method.toLowerCase()}>{PAY_LABEL[t.payment_method]}</Badge>
                        </>
                      )}
                    </div>
                  </div>
                  <span className={`font-display font-bold text-sm ${pos ? 'text-brand-blue' : 'text-brand-red'}`}>
                    {fmtMoney(t.value)}
                  </span>
                </div>
              ))}
        </div>
      ))}

      <div className="mt-4 rounded-xl bg-slate-800 dark:bg-slate-950 p-4 space-y-2">
        <div className="flex justify-between text-sm">
          <span className="text-slate-400">Total Entradas</span>
          <span className="text-emerald-400 font-bold font-display">{fmtMoney(report.total_income)}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-slate-400">Total Saídas</span>
          <span className="text-red-400 font-bold font-display">{fmtMoney(report.total_expense)}</span>
        </div>
        <div className="border-t border-slate-700 pt-2 flex justify-between">
          <span className="text-white font-bold text-sm">💼 Saldo do Dia</span>
          <span className={`font-display font-bold text-base ${report.balance >= 0 ? 'text-emerald-400' : 'text-red-400'}`}>
            {fmtMoney(report.balance)}
          </span>
        </div>
      </div>
    </Modal>
  );
}

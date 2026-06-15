import { fmtMoney, PAY_LABEL, CAT_LABEL } from '@/lib/utils';
import { Badge } from '@/components/ui/Badge';
import { Transaction } from '@/types';
import React from 'react';

interface ListTransactionsSectionProps {
  items: Transaction[];
  totalItems: number;
  title: string;
  icon: string;
  isIncome: boolean;
  color: string;
  setConfirm: (val: { id: string }) => void;
}

export const ListTransactionsSection: React.FC<ListTransactionsSectionProps> = ({
  items,
  totalItems,
  title,
  icon,
  isIncome,
  color,
  setConfirm,
}) => (
  <div className="mb-5">
    <div className="flex items-center justify-between mb-3">
      <div className="flex items-center gap-2">
        <span>{icon}</span>
        <span className="section-title mb-0">{title}</span>
        <span className="bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 rounded-full px-2.5 py-0.5 text-xs font-bold">{totalItems}</span>
      </div>
      <span className={`font-display font-bold text-sm ${color}`}>
        {fmtMoney(items.reduce((s, t) => s + Number(t.value), 0))}
      </span>
    </div>
    {items.length === 0 ? (
      <div className="empty-state py-10">
        <div className="empty-state-icon">📭</div>
        <div>Nenhum lançamento nessa categoria</div>
      </div>
    ) : (
      <div className="card">
        <div className="table-wrap">
          <table>
            <thead>
              <tr>
                {isIncome && (
                  <th>Cliente</th>
                )}
                <th>Categoria</th>
                {isIncome && (
                  <th>Forma de pagamento</th>
                )}
                <th>Valor</th>
                <th>Descrição</th>
                <th>Ações</th>
                <th />
              </tr>
            </thead>
            <tbody>
              {items.map((t) => (
                <tr key={t.id}>
                  {isIncome && (
                    <td className="font-medium">{t.customer_name}</td>
                  )}
                  <td className="font-medium">{CAT_LABEL[t.category]}</td>
                  {isIncome && (
                    <td><Badge variant={t.payment_method?.toLowerCase()}>{PAY_LABEL[t.payment_method]}</Badge></td>
                  )}
                  <td className={`font-display font-bold ${color}`}>{fmtMoney(t.value)}</td>
                  <td className="font-medium">{t.description}</td>
                  <td>
                    <button
                      className="btn btn-ghost btn-sm text-brand-red hover:bg-red-50 dark:hover:bg-red-950/20"
                      onClick={() => setConfirm({ id: t.id })}
                    >
                      ✕
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    )}
  </div>
);
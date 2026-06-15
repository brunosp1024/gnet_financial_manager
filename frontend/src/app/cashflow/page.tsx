'use client';

import { useState, useEffect, useCallback } from 'react';
import { financeService } from '@/services/finance.service';
import { customersService } from '@/services/customers.service';
import { Transaction, TransactionType, TransactionCategory, PaymentMethod, DailyReport, Customer } from '@/types';
import { CAT_LABEL } from '@/lib/utils';
import { useMoney } from '@/hooks/useMoney';
import { useToastContext } from '@/hooks/useToastContext';
import { MoneyInput } from '@/components/forms/MoneyInput';
import { Pagination } from '@/components/ui/Pagination';
import { SelectWithSearch } from '@/components/ui/SelectWithSearch';
import { ListTransactionsSection } from './components/ListTransactionsSection';
import { Confirm } from '@/components/ui/Modal';
import { ReportModal } from './components/ReportModal';

const INC_CATS: TransactionCategory[] = ['MONTHLY_FEE', 'STORE_SERVICE'];
const EXP_CATS: TransactionCategory[] = ['LOGISTIC', 'PAYROLL'];

// ── Main Page ─────────────────────────────────────────────────────────────────
export default function CashFlowPage() {
  const toast = useToastContext();
  const [tab,     setTab]     = useState<TransactionType>('INCOME');
  const [list,    setList]    = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(false);
  const [report,  setReport]  = useState<DailyReport | null>(null);
  const [confirm, setConfirm] = useState<{ id: string } | null>(null);
  const [page,    setPage]    = useState(1);
  const [meta,    setMeta]    = useState({ count: 0, currentPage: 1, totalPages: 1 });
  const [customers, setCustomers] = useState<Customer[]>([]);

  const [desc, setDesc] = useState('');
  const [cat,  setCat]  = useState<TransactionCategory>('MONTHLY_FEE');
  const [pay,  setPay]  = useState<PaymentMethod>('PIX');
  const [customerId, setCustomerId] = useState('');
  const money = useMoney(0);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await financeService.getTransactions({ type: tab, page });
      setList(res.results);
      setMeta({
        count: res.count,
        currentPage: res.current_page,
        totalPages: res.total_pages,
      });
    } catch { /* noop */ }
    finally { setLoading(false); }
  }, [tab, page]);

  useEffect(() => {
    setCat(tab === 'INCOME' ? 'MONTHLY_FEE' : 'LOGISTIC');
    money.reset();
    setDesc('');
    setPage(1);
  }, [tab]); // eslint-disable-line

  useEffect(() => {
    load();
  }, [load]);

  useEffect(() => {
    const loadCustomers = async () => {
      try {
        const res = await customersService.list({ page_size: 1000, ordering: 'name' });
        setCustomers(res.results.filter((customer) => customer.is_active));
      } catch { /* noop */ }
    };

    loadCustomers();
  }, []);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (money.isEmpty) { toast('Informe um valor maior que zero', 'err'); return; }
    try {
      await financeService.createTransaction({
        type: tab, category: cat, payment_method: pay,
        description: desc, value: money.value,
        customer_id: customerId || null,
      });
      toast('Lançamento adicionado com sucesso!', 'ok');
      setDesc('');
      setCustomerId('');
      money.reset();
      if (page === 1) {
        load();
      } else {
        setPage(1);
      }
    } catch { toast('Erro ao salvar lançamento', 'err'); }
  };

  const handleDelete = async (id: string) => {
    try {
      await financeService.deleteTransaction(id);
      toast('Lançamento removido', 'ok');
      setConfirm(null); load();
    } catch { toast('Erro ao remover', 'err'); }
  };

  const openReport = async () => {
    try {
      const r = await financeService.getDailyReport();
      setReport(r);
    } catch { toast('Erro ao carregar relatório', 'err'); }
  };

  const cats = tab === 'INCOME' ? INC_CATS : EXP_CATS;
  const isIncome = tab === 'INCOME';
  const color = isIncome ? 'text-brand-blue' : 'text-brand-red';
  const incomes  = list.filter((t) => t.category === 'MONTHLY_FEE' || t.category === 'STORE_SERVICE');
  const expenses = list.filter((t) => t.type === 'EXPENSE');

  return (
    <div>
      <div className="page-header">
        <div>
          <h1 className="page-title">Fluxo de Caixa 💰</h1>
          <p className="page-sub">Controle de entradas e saídas financeiras</p>
        </div>
        <button className="btn btn-secondary bg-[#b9ceee]" onClick={openReport}>📄 Relatório do Dia</button>
      </div>

      {/* Tabs */}
      <div className="tab-list">
        <div className={`tab-item ${tab === 'INCOME' ? 'active' : ''}`} onClick={() => setTab('INCOME')}>📥 Entradas</div>
        <div className={`tab-item ${tab === 'EXPENSE' ? 'active' : ''}`} onClick={() => setTab('EXPENSE')}>📤 Saídas</div>
      </div>

      {/* Add form */}
      <div className="card p-5 mb-5">
        <div className="text-sm font-bold text-slate-600 dark:text-slate-300 mb-4">
          {isIncome ? '➕ Nova Entrada' : '➕ Nova Saída'}
        </div>
        <form onSubmit={submit}>
          <div className="flex flex-wrap gap-3 items-end">
            {isIncome && (
              <div className="field-group" style={{ flex: 2, minWidth: 180 }}>
                <SelectWithSearch
                  label="Cliente"
                  items={customers.map((c) => ({ id: c.id, name: c.name }))}
                  value={customerId}
                  onChange={setCustomerId}
                />
              </div>
            )}
            <div className="field-group" style={{ minWidth: 140 }}>
              <label>Valor</label>
              <MoneyInput value={money} />
            </div>
            <SelectWithSearch
              label="Categoria"
              items={cats.map((c) => ({ id: c, name: CAT_LABEL[c] }))}
              value={cat}
              onChange={(v) => setCat(v as TransactionCategory)}
            />
            {isIncome && (
              <SelectWithSearch
                label="Pagamento"
                items={[
                  { id: 'PIX', name: 'PIX' },
                  { id: 'CASH', name: 'Dinheiro' },
                  { id: 'CARD', name: 'Cartão' },
                ]}
                value={pay}
                onChange={(v) => setPay(v as PaymentMethod)}
              />
            )}
            <div className="field-group" style={{ flex: 2, minWidth: 200 }}>
              <label>Descrição</label>
              <input placeholder="Ex: Mensalidade João Silva" value={desc} onChange={(e) => setDesc(e.target.value)} required />
            </div>
            <div className="self-end">
              <button className="btn btn-primary" type="submit" disabled={money.isEmpty}>+ Adicionar</button>
            </div>
          </div>
        </form>
      </div>

      {loading ? (
        <div className="flex justify-center py-16"><div className="w-8 h-8 rounded-full border-4 border-slate-200 border-t-brand-blue animate-spin" /></div>
      ) : isIncome ? (
        <>
          <ListTransactionsSection
            items={incomes}
            totalItems={meta.count}
            title="Listagem de entradas"
            icon="📡"
            isIncome={isIncome}
            color={color}
            setConfirm={setConfirm}
          />
        </>
      ) : (
        <ListTransactionsSection
          items={expenses}
          totalItems={list.length}
          title="Despesas"
          icon="💸"
          isIncome={isIncome}
          color={color}
          setConfirm={setConfirm}
        />
      )}

      {!loading && list.length > 0 ? (
        <div className="card mt-5">
          <Pagination
            count={meta.count}
            currentPage={meta.currentPage}
            totalPages={meta.totalPages}
            onPageChange={setPage}
          />
        </div>
      ) : null}

      {report ? <ReportModal report={report} onClose={() => setReport(null)} /> : null}
      {confirm ? (
        <Confirm
          msg="Deseja remover este lançamento?"
          onOk={() => confirm && handleDelete(confirm.id)}
          onNo={() => setConfirm(null)}
        />
      ) : null}
    </div>
  );
}

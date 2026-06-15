import api from '@/lib/api';
import {
  DashboardSummary,
  DailyReport,
  Transaction,
  TransactionFilters,
  TransactionPayload,
  PaginatedResponse,
} from '@/types';

type TransactionApi = {
  id: string;
  type?: Transaction['type'];
  type_display?: string;
  category?: Transaction['category'];
  category_display?: string;
  payment_method: Transaction['payment_method'];
  description: string;
  value: string;
  customer_id?: string | null;
  customer_name: string | null;
  created_at: string;
  updated_at?: string;
  created_by?: string | null;
  updated_by?: string | null;
};

const TYPE_BY_LABEL: Record<string, Transaction['type']> = {
  Entrada: 'INCOME',
  Saida: 'EXPENSE',
  Saída: 'EXPENSE',
};

const CATEGORY_BY_LABEL: Record<string, Transaction['category']> = {
  Mensalidade: 'MONTHLY_FEE',
  'Loja / Serviços': 'STORE_SERVICE',
  Logística: 'LOGISTIC',
  'Folha de Pagamento': 'PAYROLL',
};

function normalizeTransaction(tx: TransactionApi): Transaction {
  return {
    id: tx.id,
    type: tx.type ?? TYPE_BY_LABEL[tx.type_display ?? ''] ?? 'INCOME',
    category: tx.category ?? CATEGORY_BY_LABEL[tx.category_display ?? ''] ?? 'MONTHLY_FEE',
    payment_method: tx.payment_method,
    description: tx.description,
    value: tx.value,
    customer_id: tx.customer_id ?? null,
    customer_name: tx.customer_name ?? null,
    created_at: tx.created_at,
    created_by: tx.created_by ?? null,
    updated_at: tx.updated_at ?? tx.created_at,
    updated_by: tx.updated_by ?? null,
  };
}

export const financeService = {
  async getDashboard(params?: { date_from?: string; date_to?: string }): Promise<DashboardSummary> {
    const { data } = await api.get<DashboardSummary>('/finance/dashboard/', { params });
    return data;
  },

  async getDailyReport(): Promise<DailyReport> {
    const { data } = await api.get<Omit<DailyReport, 'transactions'> & { transactions: TransactionApi[] }>(
      '/finance/transactions/daily_report/'
    );
    return {
      ...data,
      transactions: data.transactions.map(normalizeTransaction),
    };
  },

  async getTransactions(filters?: TransactionFilters): Promise<PaginatedResponse<Transaction>> {
    const { data } = await api.get<PaginatedResponse<TransactionApi>>('/finance/transactions/', {
      params: filters,
    });
    return {
      ...data,
      results: data.results.map(normalizeTransaction),
    };
  },

  async createTransaction(payload: TransactionPayload): Promise<unknown> {
    const { data } = await api.post('/finance/transactions/', payload);
    return data;
  },

  async deleteTransaction(id: string): Promise<void> {
    await api.delete(`/finance/transactions/${id}/`);
  },
};

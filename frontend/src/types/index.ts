// ── Auth ──────────────────────────────────────────────────────────────────────

export interface User {
  id: string;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  is_active: boolean;
  created_at: string;
  group: string | null;
  updated_at?: string;
  created_by?: string | null;
  updated_by?: string | null;
}

export interface TokenPair {
  access: string;
  refresh: string;
}

export interface LoginCredentials {
  username: string;
  password: string;
}

// ── Customer ──────────────────────────────────────────────────────────────────

export interface Customer {
  id: string;
  name: string;
  address: string;
  phone: string | null;
  cpf: string;
  start_date: string | null;
  birthday: string | null;
  is_active: boolean;
  is_overdue: boolean;
  observations: string;
  created_at: string;
  created_by: string | null;
  updated_at: string;
  updated_by: string | null;
  [key: string]: unknown;
}

export type CustomerPayload = Partial<{
  name: string;
  address: string;
  phone: string | null;
  cpf: string;
  start_date: string | null;
  birthday: string | null;
  observations: string;
  is_active: boolean;
}>;

// ── Employee ──────────────────────────────────────────────────────────────────

export type EmployeeModality = 'CLT' | 'SERVICE_PROVIDER';

export interface Employee {
  id: string;
  name: string;
  address?: string;
  phone: string | null;
  cpf?: string;
  position: string;
  modality: EmployeeModality;
  start_date: string | null;
  birthday?: string | null;
  is_active: boolean;
  observations?: string;
  created_at?: string;
  created_by?: string | null;
  updated_at?: string;
  updated_by?: string | null;
  [key: string]: unknown;
}

export type EmployeePayload = Partial<{
  name: string;
  address: string;
  phone: string | null;
  cpf: string;
  position: string;
  modality: EmployeeModality;
  start_date: string | null;
  birthday: string | null;
  observations: string;
  is_active: boolean;
}>;

// ── Transaction ───────────────────────────────────────────────────────────────

export type TransactionType     = 'INCOME' | 'EXPENSE';
export type TransactionCategory = 'MONTHLY_FEE' | 'STORE_SERVICE' | 'LOGISTIC' | 'PAYROLL';
export type PaymentMethod       = 'CASH' | 'PIX' | 'CARD';

export interface Transaction {
  id: string;
  type: TransactionType;
  category: TransactionCategory;
  payment_method: PaymentMethod | '';
  description: string;
  value: string;
  customer_id: string | null;
  customer_name: string | null;
  created_at: string;
  created_by: string | null;
  updated_at: string;
  updated_by: string | null;
}

export type TransactionPayload = {
  type: TransactionType;
  category: TransactionCategory;
  payment_method?: PaymentMethod | '';
  description: string;
  value: number;
  customer_id?: string | null;
};

// ── Notifications ────────────────────────────────────────────────────────────

export type NotificationType = 'OVERDUE' | 'NEW_CUSTOMER' | 'BIRTHDAY' | 'ANOTHER';

export interface Notification {
  id: string;
  type: NotificationType;
  message: string;
  is_read: boolean;
  created_at: string;
}

export type NotificationPayload = {
  type: NotificationType;
  message: string;
  is_read?: boolean;
};

// ── Invoices ─────────────────────────────────────────────────────────────────

export type InvoiceStatus = 'PENDING' | 'PAID' | 'OVERDUE';

export interface Invoice {
  id: string;
  customer_name: string;
  value: string;
  due_date: string;
  status: InvoiceStatus;
  status_display: string;
  paid_at: string | null;
}

export type InvoicePayload = {
  customer_id: string;
  value: number | string;
  due_date: string;
};

export type InvoiceUpdatePayload = Partial<{
  value: number | string;
  due_date: string;
  status: InvoiceStatus;
  paid_at: string | null;
}>;

// ── Dashboard ─────────────────────────────────────────────────────────────────

export interface CategoryStat {
  category: TransactionCategory;
  type: TransactionType;
  total: number;
  count: number;
}

export interface DashboardSummary {
  income_total:      number;
  expense_total:     number;
  balance:           number;
  transaction_count: number;
  by_category:       CategoryStat[];
}

// ── Daily Report ──────────────────────────────────────────────────────────────

export interface DailyReport {
  date:          string;
  transactions:  Transaction[];
  total_income:  number;
  total_expense: number;
  balance:       number;
}

// ── Pagination ────────────────────────────────────────────────────────────────

export interface PaginatedResponse<T> {
  count:    number;
  next:     string | null;
  previous: string | null;
  total_pages: number;
  current_page: number;
  results:  T[];
}

// ── API filters ───────────────────────────────────────────────────────────────

export interface TransactionFilters {
  type?:      TransactionType;
  category?:  TransactionCategory;
  date_from?: string;
  date_to?:   string;
  search?:    string;
  ordering?:  string;
  page?:      number;
  page_size?: number;
}

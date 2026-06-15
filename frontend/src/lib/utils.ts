import clsx from 'clsx';

export function cn(...values: Array<string | false | null | undefined>) {
  return clsx(values);
}

export function fmtMoney(value: number | string | null | undefined) {
  const amount = Number(value ?? 0);
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(Number.isFinite(amount) ? amount : 0);
}

export function isoToDisplay(value?: string | null) {
  if (!value) return '—';
  const match = value.match(/^(\d{4})-(\d{2})-(\d{2})/);
  if (!match) return value;
  return `${match[3]}/${match[2]}/${match[1]}`;
}

export function displayToISO(value?: string | null) {
  if (!value) return '';
  const match = value.match(/^(\d{2})\/(\d{2})\/(\d{4})$/);
  if (!match) return '';
  return `${match[3]}-${match[2]}-${match[1]}`;
}

export function todayISO() {
  return new Date().toISOString().slice(0, 10);
}

export function cpfMask(value: string) {
  if (!value) return '-';
  const digits = value.replace(/\D/g, '').slice(0, 11);
  return digits
    .replace(/^(\d{3})(\d)/, '$1.$2')
    .replace(/^(\d{3})\.(\d{3})(\d)/, '$1.$2.$3')
    .replace(/\.(\d{3})(\d)/, '.$1-$2');
}

export function phoneMask(value: string) {
  if (!value) return '';
  const digits = value.replace(/\D/g, '').slice(0, 11);
    if (digits.length === 11) {
      console.log('quantas vezes');
      // Show: (XX) X XXXX-XXXX
      return digits
        .replace(/^(\d{2})(\d)/, '($1) $2')
        .replace(/^\((\d{2})\) (\d)(\d{4})(\d{4})$/, '($1) $2 $3-$4');
    }
    // Show: (XX) XXXX-XXXX
    return digits
      .replace(/^(\d{2})(\d)/, '($1) $2')
      .replace(/(\d{4,5})(\d{4})$/, '$1-$2');
}

export function unmaskCPF(value: string) {
  return value.replace(/\D/g, '');
}

export function unmaskPhone(value: string) {
  return value.replace(/\D/g, '');
}

export function validateCPF(value: string) {
  const cpf = value.replace(/\D/g, '');
  if (cpf.length !== 11 || /^(\d)\1+$/.test(cpf)) return false;

  const calc = (base: string, factor: number) => {
    const total = base.split('').reduce((sum, digit) => sum + Number(digit) * factor--, 0);
    const remainder = (total * 10) % 11;
    return remainder === 10 ? 0 : remainder;
  };

  const digit1 = calc(cpf.slice(0, 9), 10);
  const digit2 = calc(cpf.slice(0, 10), 11);
  return digit1 === Number(cpf[9]) && digit2 === Number(cpf[10]);
}

export function initials(value?: string | null) {
  if (!value) return 'GN';
  return value
    .trim()
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase() ?? '')
    .join('') || 'GN';
}

export const CAT_LABEL: Record<string, string> = {
  MONTHLY_FEE: 'Mensalidade',
  STORE_SERVICE: 'Loja / Serviços',
  LOGISTIC: 'Logística',
  PAYROLL: 'Folha de Pagamento',
};

export const PAY_LABEL: Record<string, string> = {
  CASH: 'Dinheiro',
  PIX: 'PIX',
  CARD: 'Cartão',
};

export const MODALITY_LABEL: Record<string, string> = {
  CLT: 'CLT',
  SERVICE_PROVIDER: 'Prestador de Serviços',
};

export const BRAND_COLORS = ['#1565c0', '#d32f2f', '#1d4ed8', '#0f766e', '#ea580c'];

'use client';

import { CrudPage, CrudConfig, FieldDef } from '@/components/ui/CrudPage';
import { customersService } from '@/services/customers.service';
import { Customer } from '@/types';
import { isoToDisplay, todayISO } from '@/lib/utils';
import { cpfMask, phoneMask } from '@/lib/utils';
import { Badge } from '@/components/ui/Badge';


const customerFields: FieldDef[] = [
    { key: 'name',         label: 'Nome completo',        required: true,  ph: 'Nome do cliente' },
    { key: 'cpf',          label: 'CPF',                  type: 'cpf',     ph: '000.000.000-00' },
    { key: 'phone',        label: 'Telefone',             type: 'phone',  ph: '(99) 9 9999-9999' },
    { key: 'address',      label: 'Endereço',             ph: 'Rua, nº, bairro' },
    { key: 'start_date',   label: 'Início do Contrato',   type: 'date' },
    { key: 'observations', label: 'Observações',          ph: 'Informações adicionais' },
  ];

const customerDetailFields: FieldDef[] = [
  ...customerFields,
  { key: 'created_by', label: 'Criado por', type: 'text' },
  { key: 'created_at', label: 'Criado em', type: 'date' },
];

const config: CrudConfig<Customer> = {
  singular: 'Cliente',
  plural:   'Clientes',
  icon:     '👥',
  subtitle: 'Gestão de assinantes do provedor',
  defaultForm: {
    name: '', address: '', phone: '', cpf: '',
    start_date: todayISO(), observations: '',
  },
  toForm: (it) => ({
    name:         it.name         ?? '',
    address:      it.address      ?? '',
    phone:        it.phone ? phoneMask(it.phone) : '',
    cpf:          it.cpf ? cpfMask(it.cpf) : '',
    start_date:   it.start_date   ?? '',
    observations: it.observations ?? '',
  }),
  fields: customerFields,
  detailFields: customerDetailFields,
  cols: [
    { key: 'name',       label: 'Nome' },
    { key: 'cpf',        label: 'CPF',    render: (v, _row) => cpfMask(v as string) || '-' },
    { key: 'phone',      label: 'Fone',   render: (v, _row) => phoneMask(v as string) || '-' },
    { key: 'start_date', label: 'Início', render: (v) => isoToDisplay(v as string) },
    { key: 'is_active',  label: 'Status', render: (v) => <Badge variant={v ? 'active' : 'inactive'}>{v ? 'Ativo' : 'Inativo'}</Badge> },
    { key: 'created_at', label: 'Cadastro', render: (v) => isoToDisplay((v as string)?.slice(0, 10)) },
  ],
  detail: (id) => customersService.detail(id),
  list:   (p) => customersService.list(p as { search?: string }),
  create: (d) => customersService.create(d),
  update: (id, d) => customersService.update(id, d),
  remove: (id) => customersService.remove(id),
};

export default function CustomersPage() {
  return <CrudPage config={config} />;
}

'use client';

import { CrudPage, CrudConfig, FieldDef } from '@/components/ui/CrudPage';
import { employeesService } from '@/services/employees.service';
import { Employee } from '@/types';
import { isoToDisplay, todayISO, MODALITY_LABEL, phoneMask, cpfMask } from '@/lib/utils';
import { Badge } from '@/components/ui/Badge';

const employeeFields: FieldDef[] = [
    { key: 'name',         label: 'Nome completo',     required: true },
    { key: 'cpf',          label: 'CPF',               type: 'cpf', required: true },
    { key: 'phone',        label: 'Telefone',          type: 'phone',  ph: '(99) 9 9999-9999' },
    { key: 'position',     label: 'Cargo / Função',    ph: 'Ex: Técnico de Redes' },
    { key: 'address',      label: 'Endereço',          ph: 'Rua, nº, bairro, cidade' },
    { key: 'birthday',     label: 'Data de Nascimento', type: 'date' },
    { key: 'start_date',   label: 'Data de Admissão',  type: 'date' },
    {
      key: 'modality', label: 'Modalidade Contratual', type: 'select',
      opts: [
        { v: 'CLT',              l: 'CLT — Carteira Assinada' },
        { v: 'SERVICE_PROVIDER', l: 'Prestador de Serviços' },
      ],
    },
  ];

const employeeDetailFields: FieldDef[] = [
  ...employeeFields,
  { key: 'observations', label: 'Observações', type: 'text' },
  { key: 'created_by', label: 'Criado por', type: 'text' },
  { key: 'created_at', label: 'Criado em', type: 'date' },
];

const config: CrudConfig<Employee> = {
  singular: 'Funcionário',
  plural:   'Funcionários',
  icon:     '🏢',
  subtitle: 'Gestão de colaboradores e prestadores',
  defaultForm: {
    name: '', cpf: '', phone: '', address: '',
    position: '', modality: 'CLT',
    start_date: todayISO(), birthday: '', observations: '',
  },
  toForm: (it) => ({
    name:         it.name         ?? '',
    cpf:          it.cpf ? cpfMask(it.cpf) : '',
    phone:        it.phone ? phoneMask(it.phone) : '',
    address:      it.address      ?? '',
    position:     it.position     ?? '',
    modality:     it.modality     ?? 'CLT',
    start_date:   it.start_date   ?? '',
    birthday:     it.birthday     ?? '',
    observations: it.observations ?? '',
  }),
  fields: employeeFields,
  detailFields: employeeDetailFields,
  cols: [
    { key: 'name',       label: 'Nome' },
    { key: 'position',   label: 'Cargo',    render: (v) => (v as string) || '—' },
    { key: 'phone',        label: 'Telefone',    render: (v, _row) => phoneMask(v as string) },
    { key: 'modality',   label: 'Modalidade', render: (v) => <Badge variant={(v as string)?.toLowerCase()}>{MODALITY_LABEL[v as string] ?? v}</Badge> },
    { key: 'start_date', label: 'Admissão', render: (v) => isoToDisplay(v as string) },
  ],
  detail: (id) => employeesService.detail(id),
  list:   (p) => employeesService.list(p as { search?: string }),
  create: (d) => employeesService.create(d),
  update: (id, d) => employeesService.update(id, d),
  remove: (id) => employeesService.remove(id),
};

export default function EmployeesPage() {
  return <CrudPage config={config} />;
}

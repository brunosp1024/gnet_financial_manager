'use client';

import { CrudPage, CrudConfig } from '@/components/ui/CrudPage';
import { usersService } from '@/services/users.service';
import { User } from '@/types';
import { isoToDisplay } from '@/lib/utils';
import { Badge } from '@/components/ui/Badge';

const config: CrudConfig<User> = {
  singular: 'Usuário',
  plural:   'Usuários',
  icon:     '🔐',
  subtitle: 'Controle de acesso ao sistema',
  defaultForm: {
    username: '', first_name: '', last_name: '', email: '', group: 'FINANCEIRO', password: '',
  },
  toForm: (it) => ({
    username:   it.username   ?? '',
    first_name: it.first_name ?? '',
    last_name:  it.last_name  ?? '',
    email:      it.email      ?? '',
    group:      it.group      ?? 'FINANCEIRO',
    password:   '',
  }),
  fields: [
    { key: 'first_name', label: 'Nome',     required: true },
    { key: 'last_name',  label: 'Sobrenome', required: true },
    { key: 'username',   label: 'Usuário',   required: true, ph: 'login' },
    { key: 'email',      label: 'E-mail',    type: 'email', required: true },
    {
      key: 'group', label: 'Perfil', type: 'select', required: true,
      opts: [
        { v: 'ADMIN', l: 'Administrador' },
        { v: 'GERENTE', l: 'Gerente' },
        { v: 'FINANCEIRO', l: 'Financeiro' },
      ],
    },
    { key: 'password',   label: 'Senha',     type: 'password', ph: 'Mínimo 6 caracteres' },
  ],
  cols: [
    { key: 'first_name', label: 'Nome',    render: (_v, row) => `${row.first_name} ${row.last_name}` },
    { key: 'username',   label: 'Usuário' },
    { key: 'email',      label: 'E-mail' },
    { key: 'group',      label: 'Perfil',  render: (v) => (v as string) ? <Badge variant={(v as string).toLowerCase()} className="mr-1">{v}</Badge> : '—' },
    { key: 'is_active',  label: 'Status',  render: (v) => <Badge variant={v ? 'active' : 'inactive'}>{v ? 'Ativo' : 'Inativo'}</Badge> },
    { key: 'created_at', label: 'Cadastro', render: (v) => isoToDisplay((v as string)?.slice(0, 10)) },
  ],
  detail: (id) => usersService.detail(id),
  list:   (p) => usersService.list(p as { search?: string }),
  create: (d) => usersService.create(d as Parameters<typeof usersService.create>[0]),
  update: (id, d) => usersService.update(id, d),
  remove: (id) => usersService.remove(id),
};

export default function UsersPage() {
  return <CrudPage config={config} />;
}

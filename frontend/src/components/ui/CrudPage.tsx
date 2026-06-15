'use client';

import { useState, useEffect, useCallback, ReactNode } from 'react';
import { Modal, Confirm } from '@/components/ui/Modal';
import { Pagination } from '@/components/ui/Pagination';
import { DateInput } from '@/components/forms/DateInput';
import { cpfMask, phoneMask, validateCPF, unmaskCPF, unmaskPhone, isoToDisplay } from '@/lib/utils';
import { useToastContext } from '@/hooks/useToastContext';
import { PaginatedResponse } from '@/types';

export interface FieldDef {
  key:      string;
  label:    string;
  type?:    'text' | 'email' | 'password' | 'date' | 'cpf' | 'select' | 'phone';
  required?:boolean;
  ph?:      string;
  opts?:    { v: string; l: string }[];
}

export interface ColDef {
  key: string;
  label: string;
  render?: (val: unknown, row: Record<string, unknown>) => ReactNode;
}

export interface CrudConfig<T extends Record<string, unknown>> {
  singular:   string;
  plural:     string;
  icon:       string;
  subtitle:   string;
  fields:     FieldDef[];
  detailFields: FieldDef[];
  cols:       ColDef[];
  defaultForm:Record<string, string>;
  toForm:     (item: T) => Record<string, string>;
  detail?:    (id: string) => Promise<T>;
  list:       (params?: Record<string, unknown>) => Promise<PaginatedResponse<T>>;
  create:     (data: Record<string, unknown>) => Promise<unknown>;
  update:     (id: string, data: Record<string, unknown>) => Promise<unknown>;
  remove:     (id: string) => Promise<void>;
}

interface Props<T extends Record<string, unknown>> {
  config: CrudConfig<T>;
}

export function CrudPage<T extends Record<string, unknown>>({ config: cfg }: Props<T>) {
  const toast = useToastContext();
  const [items,   setItems]   = useState<T[]>([]);
  const [loading, setLoading] = useState(true);
  const [open,    setOpen]    = useState(false);
  const [edit,    setEdit]    = useState<T | null>(null);
  const [form,    setForm]    = useState<Record<string, string>>({});
  const [errs,    setErrs]    = useState<Record<string, string>>({});
  const [saving,  setSaving]  = useState(false);
  const [confirm, setConfirm] = useState<{ id: string } | null>(null);
  const [search,  setSearch]  = useState('');
  const [page,    setPage]    = useState(1);
  const [meta,    setMeta]    = useState({ count: 0, currentPage: 1, totalPages: 1 });
  const [view,    setView]    = useState<T | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const res = await cfg.list({ search: search || undefined, page });
      setItems(res.results);
      setMeta({
        count: res.count,
        currentPage: res.current_page,
        totalPages: res.total_pages,
      });
    } catch { /* noop */ }
    finally { setLoading(false); }
  }, [search, page, cfg]);

  useEffect(() => { load(); }, [load]);

  const openNew = () => {
    setEdit(null);
    setForm({ ...cfg.defaultForm });
    setErrs({});
    setOpen(true);
  };

  const openEdit = async (item: T) => {
    try {
      const fullItem = cfg.detail ? await cfg.detail(String(item.id)) : item;
      setEdit(fullItem);
      setForm(cfg.toForm(fullItem));
      setErrs({});
      setOpen(true);
    } catch {
      toast(`Erro ao carregar ${cfg.singular.toLowerCase()}`, 'err');
    }
  };

  const openView = async (item: T) => {
    try {
      const fullItem = cfg.detail ? await cfg.detail(String(item.id)) : item;
      setView(fullItem);
    } catch {
      toast(`Erro ao carregar ${cfg.singular.toLowerCase()}`, 'err');
    }
  };

  const setF = (k: string, v: string) => {
    setForm((f) => ({ ...f, [k]: v }));
    setErrs((e) => ({ ...e, [k]: '' }));
  };

  const validate = () => {
    const e: Record<string, string> = {};
    cfg.fields.forEach((f) => {
      const v = (form[f.key] ?? '').trim();
      if (f.required && !v) e[f.key] = 'Campo obrigatório';
      if (f.type === 'cpf' && v && !validateCPF(v)) e[f.key] = 'CPF inválido';
    });
    return e;
  };

  const save = async () => {
    const e = validate();
    if (Object.keys(e).length) { setErrs(e); return; }
    setSaving(true);
    try {
      // Remove cpf and phone mask before sending to API
      const payload = Object.fromEntries(
        Object.entries(form)
          .filter(([, v]) => v !== '')
          .map(([k, v]) => {
            if (k === 'cpf') return [k, unmaskCPF(v)];
            if (k === 'phone') return [k, unmaskPhone(v)];
            return [k, v];
          })
      );
      if (edit) {
        await cfg.update(edit.id as string, payload);
        toast(`${cfg.singular} atualizado!`, 'ok');
      } else {
        await cfg.create(payload);
        toast(`${cfg.singular} cadastrado!`, 'ok');
      }
      setOpen(false);
      if (page === 1) {
        load();
      } else {
        setPage(1);
      }
    } catch (ex: unknown) {
      const msg = (ex as { response?: { data?: Record<string, string[]> } })?.response?.data;
      if (msg) {
        const first = Object.values(msg)[0]?.[0];
        toast(first ?? 'Erro ao salvar', 'err');
      } else {
        toast('Erro ao salvar', 'err');
      }
    } finally {
      setSaving(false);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await cfg.remove(id);
      toast('Removido com sucesso', 'ok');
      setConfirm(null);
      load();
    } catch { toast('Erro ao remover', 'err'); }
  };

  return (
    <div>
      {/* Header */}
      <div className="page-header">
        <div>
          <h1 className="page-title">{cfg.icon} {cfg.plural}</h1>
          <p className="page-sub">{cfg.subtitle}</p>
        </div>
        <button className="btn btn-primary" onClick={openNew}>+ Novo {cfg.singular}</button>
      </div>

      {/* Search */}
      <div className="filter-bar">
        <div className="field-group">
          <label>Busca</label>
          <input
            placeholder={`Buscar ${cfg.plural.toLowerCase()}…`}
            value={search}
            onChange={(e) => {
              setSearch(e.target.value);
              setPage(1);
            }}
          />
        </div>
        <button
          className="btn btn-primary btn-sm self-end"
          onClick={() => {
            if (page === 1) {
              load();
            } else {
              setPage(1);
            }
          }}
        >
          Buscar
        </button>
      </div>

      {/* Table */}
      <div className="card">
        {loading ? (
          <div className="flex justify-center py-16">
            <div className="w-8 h-8 rounded-full border-4 border-slate-200 border-t-brand-blue animate-spin" />
          </div>
        ) : items.length === 0 ? (
          <div className="empty-state">
            <div className="empty-state-icon">{cfg.icon}</div>
            <div>Nenhum {cfg.singular.toLowerCase()} cadastrado ainda</div>
          </div>
        ) : (
          <>
            <div className="table-wrap">
              <table>
                <thead>
                  <tr>
                    {cfg.cols.map((c) => <th key={c.key}>{c.label}</th>)}
                    <th>Ações</th>
                  </tr>
                </thead>
                <tbody>
                  {items.map((it) => (
                    <tr key={it.id as string}>
                      {cfg.cols.map((c) => (
                        <td key={c.key}>
                          {c.render
                            ? c.render(it[c.key], it as Record<string, unknown>)
                            : (it[c.key] as string) || '—'}
                        </td>
                      ))}
                      <td>
                        <div className="flex gap-2">
                          <button className="btn btn-info btn-sm" onClick={() => openView(it)}>👁️</button>
                          <button className="btn btn-secondary btn-sm" onClick={() => openEdit(it)}>✏️</button>
                          <button
                            className="btn btn-danger btn-sm"
                            onClick={() => setConfirm({ id: it.id as string })}
                          >✕</button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <Pagination
              count={meta.count}
              currentPage={meta.currentPage}
              totalPages={meta.totalPages}
              onPageChange={setPage}
            />
          </>
        )}
      </div>

      {/* Modal */}
      {open && (
        <Modal
          title={edit ? `Editar ${cfg.singular}` : `Novo ${cfg.singular}`}
          onClose={() => setOpen(false)}
          footer={
            <>
              <button className="btn btn-secondary" onClick={() => setOpen(false)}>Cancelar</button>
              <button className="btn btn-primary" onClick={save} disabled={saving}>
                {saving ? 'Salvando…' : 'Salvar'}
              </button>
            </>
          }
        >
          <div className="flex flex-col gap-4">
            {cfg.fields.map((f) => (
              <div key={f.key}>
                <label>
                  {f.label}
                  {f.required && <span className="text-brand-red ml-0.5">*</span>}
                </label>
                {f.type === 'select' ? (
                  <select value={form[f.key] ?? ''} onChange={(e) => setF(f.key, e.target.value)} className={errs[f.key] ? 'err' : ''}>
                    {f.opts?.map((o) => <option key={o.v} value={o.v}>{o.l}</option>)}
                  </select>
                ) : f.type === 'date' ? (
                  <DateInput value={form[f.key] ?? ''} onChange={(v) => setF(f.key, v)} required={f.required} className={errs[f.key] ? 'err' : ''} />
                ) : f.type === 'cpf' ? (
                  <input
                    value={form[f.key] ?? ''}
                    onChange={(e) => setF(f.key, cpfMask(e.target.value))}
                    maxLength={14}
                    placeholder="000.000.000-00"
                    className={errs[f.key] ? 'err' : ''}
                  />
                ) : f.type === 'phone' ? (
                  <input
                    value={form[f.key] ?? ''}
                    onChange={(e) => setF(f.key, phoneMask(e.target.value))}
                    placeholder={f.ph ?? ''}
                    maxLength={16}
                    className={errs[f.key] ? 'err' : ''}
                  />
                ) :(
                  <input
                    type={f.type ?? 'text'}
                    value={form[f.key] ?? ''}
                    onChange={(e) => setF(f.key, e.target.value)}
                    placeholder={f.ph ?? ''}
                    required={f.required}
                    className={errs[f.key] ? 'err' : ''}
                  />
                )}
                {errs[f.key] && <p className="form-error">⚠ {errs[f.key]}</p>}
              </div>
            ))}
          </div>
        </Modal>
      )}

      {/* Detail Modal */}
      {view && (
        <Modal
          title={`Visualizar ${cfg.singular}`}
          onClose={() => setView(null)}
          footer={<button className="btn btn-secondary" onClick={() => setView(null)}>Fechar</button>}
        >
          <div className="flex flex-col gap-4">
            {cfg.detailFields.map((f) => {
              console.log(f.type);
              
              let value = view[f.key];
              if (f.type === 'date') {
                console.log('Valor original:', value);
                console.log('Valor formatado:', phoneMask(value as string));
                
              }
              if (f.type === 'cpf' && value) value = cpfMask(value as string);
              if (f.type === 'phone' && value) value = phoneMask(value as string);
              if (f.type === 'date' && value) value = isoToDisplay(value as string);
              if (f.type === 'select' && f.opts && value) {
                const opt = f.opts.find(o => o.v === value);
                value = opt ? opt.l : value;
              }
              return (
                <div key={f.key}>
                  <label>{f.label}</label>
                  <div className="detail-value">
                    {value as string || '—'}
                  </div>
                </div>
              );
            })}
          </div>
        </Modal>
      )}

      {/* Confirm Delete Modal */}
      {confirm && (
        <Confirm
          msg={`Deseja remover este ${cfg.singular.toLowerCase()} permanentemente?`}
          onOk={() => handleDelete(confirm.id)}
          onNo={() => setConfirm(null)}
        />
      )}
    </div>
  );
}

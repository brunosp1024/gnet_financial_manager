'use client';

import { ReactNode } from 'react';

interface Props {
  title:    string;
  onClose:  () => void;
  children: ReactNode;
  footer?:  ReactNode;
  wide?:    boolean;
}

export function Modal({ title, onClose, children, footer, wide }: Props) {
  return (
    <div
      className="fixed inset-0 z-40 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4 animate-[fadeIn_0.18s_ease-out]"
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div
        className="w-full max-h-[90vh] flex flex-col rounded-2xl bg-white dark:bg-slate-900 shadow-2xl animate-[modalIn_0.24s_cubic-bezier(0.22,1,0.36,1)] origin-center"
        style={{ maxWidth: wide ? 700 : 580 }}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-100 dark:border-slate-800">
          <h3 className="font-display font-bold text-base text-slate-800 dark:text-slate-100">{title}</h3>
          <button
            onClick={onClose}
            className="text-xl text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 transition-colors leading-none"
          >
            ×
          </button>
        </div>

        {/* Body */}
        <div className="px-6 py-5 overflow-y-auto flex-1">{children}</div>

        {/* Footer */}
        {footer && (
          <div className="px-6 py-4 border-t border-slate-100 dark:border-slate-800 flex justify-end gap-3">
            {footer}
          </div>
        )}
      </div>
    </div>
  );
}

export function Confirm({ msg, onOk, onNo }: { msg: string; onOk: () => void; onNo: () => void }) {
  return (
    <Modal
      title="⚠️ Confirmação"
      onClose={onNo}
      footer={
        <>
          <button className="btn btn-secondary" onClick={onNo}>Cancelar</button>
          <button className="btn btn-danger"    onClick={onOk}>Confirmar</button>
        </>
      }
    >
      <p className="text-slate-500 dark:text-slate-400 text-sm leading-relaxed">{msg}</p>
    </Modal>
  );
}

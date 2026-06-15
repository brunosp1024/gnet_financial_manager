import { LOGO_BASE64 } from '@/lib/logo';

export function Footer() {
  return (
    <footer className="flex items-center justify-between px-6 py-4 border-t border-slate-100 dark:border-slate-800 text-xs text-slate-400 dark:text-slate-500 font-body mt-auto">
      <div className="flex items-center gap-3">
        <img src={LOGO_BASE64} alt="" className="w-6 h-6 rounded object-contain" />
        <span className="font-display font-bold text-slate-600 dark:text-slate-300">
          GlobalNet<span className="text-brand-red">&apos;I</span>
        </span>
        <span className="opacity-30 mx-1">|</span>
        <span>Sistema de Gestão Financeira</span>
      </div>
      <div className="text-right">
        <div>📍 Brasil · CNPJ: 00.000.000/0001-00</div>
        <div className="opacity-40 mt-0.5">
          © {new Date().getFullYear()} GlobalNet&#39;I — Todos os direitos reservados
        </div>
      </div>
    </footer>
  );
}

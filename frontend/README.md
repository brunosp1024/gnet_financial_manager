# GlobalNet'I — Frontend

> Sistema de gestão financeira para provedores de internet.
>
> **Stack:** Next.js 14 (App Router) · TypeScript · Tailwind CSS

---

## 📁 Estrutura de Pastas

```
src/
├── app/              # Rotas e layouts do Next.js (App Router)
│   ├── layout.tsx    # Layout raiz (AuthProvider)
│   ├── page.tsx      # Redirecionamento inicial
│   └── ...           # Rotas: login, dashboard, cashflow, customers, employees, users
│
├── components/       # Componentes reutilizáveis
│   ├── ui/           # UI genérica: Toast, Modal, Badge, CrudPage
│   ├── layout/       # Sidebar, Topbar, Footer, AppShell
│   └── forms/        # Inputs customizados (DateInput, MoneyInput)
│
├── hooks/            # Hooks customizados (auth, money, toast)
│
├── lib/              # Utilitários e helpers globais
│   ├── api.ts        # Instância Axios com interceptors JWT
│   ├── utils.ts      # Funções utilitárias (formatação, máscaras, datas)
│   └── logo.ts       # Exportação do base64 da logo
│
├── services/         # Serviços de domínio (auth, finance, customers, employees, users)
│
├── types/            # Tipos TypeScript globais
│
└── styles/           # Estilos globais (Tailwind + custom)
```

---

## ⚙️ Principais Dependências

- **next** 14.2.x
- **react** 18.x
- **axios** (requisições HTTP)
- **clsx** (classes condicionais)
- **date-fns** (datas)
- **js-cookie** (cookies JWT)
- **recharts** (gráficos)
- **tailwindcss** 3.x
- **typescript** 5.x

---

## 🚀 Como rodar o projeto

```bash
# 1. Instale as dependências
npm install

# 2. Configure as variáveis de ambiente
cp .env.local.example .env.local
# Edite NEXT_PUBLIC_API_URL se necessário

# 3. Rode em modo desenvolvimento
npm run dev

# 4. Build e produção
npm run build && npm start
```

---

## 🔐 Autenticação

- JWT via cookies (`gn_access` + `gn_refresh`)
- Auto-refresh transparente no interceptor do Axios
- Redirecionamento automático para `/login` se não autenticado
- Guardas de autenticação em cada `layout.tsx` das rotas protegidas

---

## 🧩 CrudPage — CRUD Genérico

O componente `CrudPage<T>` recebe uma configuração (`CrudConfig<T>`) e gera automaticamente:

- Tabela com colunas dinâmicas
- Modal de criação/edição com validação
- Confirmação de exclusão
- Busca com debounce

Utilizado em: customers, employees, users

---

## 🛠️ Utilitários (`lib/utils.ts`)

Funções utilitárias principais:

- `cn` — Combina classes condicionalmente (usa clsx)
- `fmtMoney` — Formata valores monetários (R$)
- `isoToDisplay` / `displayToISO` — Conversão de datas ISO <-> dd/mm/aaaa
- `todayISO` — Data de hoje em ISO
- `cpfMask` — Máscara para CPF

---

## 🎨 Design System

Tokens principais:

| Token        | Valor             |
|--------------|------------------|
| Brand Blue   | `#1565c0`        |
| Brand Red    | `#d32f2f`        |
| Font Display | Playpen Sans Thai|
| Font Body    | DM Sans          |

Classes utilitárias em `globals.css`: `.btn`, `.card`, `.table-wrap`, `.page-header`, `.stats-grid`, `.tab-list`, `.badge`, etc.

---

## 📢 Observações

- O logo pode ser referenciado diretamente de `/public/images/logo.png` ou via constante em `lib/logo.ts`.
- Mantenha a consistência dos utilitários e serviços para facilitar manutenção.

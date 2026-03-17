# Backend (Django)

Guia rapido para rodar o backend localmente.

## 1. Ambiente

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## 2. Banco de dados

```bash
python manage.py migrate
```

## 3. Redis (necessario para Celery)

```bash
sudo apt install -y redis-server
sudo systemctl enable --now redis-server
```

## 4. Subir backend + worker + beat

```bash
chmod +x run.sh
./run.sh
```

Notas:
- `run.sh` sobe API Django, `celery worker` e `celery beat`.
- Se o Redis ja estiver ativo em `localhost:6379`, a instancia existente e reutilizada.

## 5. Popular dados iniciais

```bash
python manage.py setup
```

O comando `setup` carrega os fixtures iniciais, incluindo:
- grupos e permissoes
- usuarios iniciais
- clientes, funcionarios, faturas, transacoes e notificacoes

## 6. Credenciais iniciais dos usuários gerados no setup

- Admin
  - `username`: `admin`
  - `password`: `admin123`
- Gerente
  - `username`: `gerente`
  - `password`: `gerente123`
- Financeiro
  - `username`: `financeiro`
  - `password`: `financeiro123`

## 7. Opcional: iniciar sem fixtures

Se quiser iniciar com banco vazio, crie o superusuário e use suas credenciais:

```bash
python manage.py createsuperuser
```

Depois,

## Configuracoes uteis

Throttling via `.env`:
- `THROTTLE_ANON_RATE`
- `THROTTLE_USER_RATE`
- `THROTTLE_LOGIN_RATE`

Tasks periodicas executadas pelo Celery:
- `delete_old_notifications`
- `check_employee_birthdays`
- `check_overdue_invoices`
- `physical_delete_soft_deleted`

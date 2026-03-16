# Backend (Django)

Instruções rápidas:

1. Criar virtualenv e instalar dependências:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Variáveis de ambiente: copie `.env.example` para `.env` e ajuste.

```bash
cp .env.example .env
```

3. Rodar migrations:

```bash
python manage.py migrate
python manage.py createsuperuser
```

4. Rodar servidor:

```bash
python manage.py runserver
```

> O projeto já inclui limites de requisição (throttling) configuráveis por `.env`:
> `THROTTLE_ANON_RATE`, `THROTTLE_USER_RATE` e `THROTTLE_LOGIN_RATE`.

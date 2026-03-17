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

5. Rodar backend + Celery + Beat + Redis local de desenvolvimento:

> Antes, instalar e executar o redis-server
```bash
sudo apt install -y redis-server
sudo systemctl enable --now redis-server
```

```bash
chmod +x run.sh
./run.sh
```

> O script `run.sh` sobe `celery worker` e `celery beat` automaticamente.
> Se o Redis ja estiver ativo em `localhost:6379`, ele reutiliza a instancia existente.

> O projeto já inclui limites de requisição (throttling) configuráveis por `.env`:
> `THROTTLE_ANON_RATE`, `THROTTLE_USER_RATE` e `THROTTLE_LOGIN_RATE`.

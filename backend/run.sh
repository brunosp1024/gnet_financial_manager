#!/usr/bin/env bash

# Faz o script parar imediatamente se algum comando falhar.
set -e

# Descobre a pasta onde o próprio run.sh está localizado,
# garantindo que o script funcione independentemente de onde seja chamado.
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SRC_DIR="$ROOT_DIR/src"
VENV_PYTHON="$ROOT_DIR/.venv/bin/python"
CELERY_PID=""

# Kill process celery if it was started by the script.
cleanup() {
  if [[ -n "$CELERY_PID" ]] && kill -0 "$CELERY_PID" 2>/dev/null; then
    kill "$CELERY_PID" 2>/dev/null || true
  fi
}

# Ensure cleanup when the computer shuts down normally or interruption is received.
trap cleanup EXIT INT TERM

# Checks if the virtualenv python exists and is executable.
if [[ ! -x "$VENV_PYTHON" ]]; then
  echo "Python da virtualenv nao encontrado em: $VENV_PYTHON"
  echo "Crie a virtualenv e instale as dependencias antes de rodar este script."
  exit 1
fi

echo "Preparando ambiente de desenvolvimento..."

# Access src directory.
cd "$SRC_DIR"

# Start Celery worker with beat in the background.
echo "Subindo Celery worker com beat..."
"$VENV_PYTHON" -m celery -A core worker -B -l info &
CELERY_PID=$!

# Wait 2 seconds to give Celery time to start.
sleep 2

# Check if Celery is still running after the initial startup.
if ! kill -0 "$CELERY_PID" 2>/dev/null; then
  echo "Celery encerrou logo apos iniciar. Verifique se o Redis esta ativo em localhost:6379."
  exit 1
fi

echo "Servicos ativos:"
echo "- Django: http://127.0.0.1:8000"
echo "- Celery worker + beat: ativo"

echo "Iniciando Django runserver..."
exec "$VENV_PYTHON" manage.py runserver

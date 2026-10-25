#!/usr/bin/env bash
set -euo pipefail

# Run from the Django application directory on the cPanel server.
: "${APP_VENV:?Set APP_VENV to the cPanel Python virtual-environment directory}"

PYTHON="$APP_VENV/bin/python"
PIP="$APP_VENV/bin/pip"

"$PIP" install --requirement requirements.txt
"$PIP" install --requirement requirements-ai.txt
"$PYTHON" manage.py migrate --noinput
"$PYTHON" manage.py collectstatic --noinput
"$PYTHON" manage.py check --deploy
mkdir -p tmp
touch tmp/restart.txt

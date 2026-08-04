#!/usr/bin/env bash
# Start the Koha OPAC AI Assistant FastAPI Backend
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$REPO_ROOT/backend"

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
    source .venv/bin/activate
    pip install --upgrade pip
    pip install -r requirements.txt
else
    source .venv/bin/activate
fi

echo "Starting Koha OPAC AI Assistant Backend on http://0.0.0.0:8000 ..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000

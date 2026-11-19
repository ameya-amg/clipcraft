#!/bin/bash
# Startup script for ClipCraft AI

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

export PATH="/opt/homebrew/bin:$PATH"

if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3.12 -m venv .venv
    .venv/bin/pip install -r requirements.txt
fi

echo "Starting ClipCraft AI on http://localhost:8000 ..."
.venv/bin/uvicorn backend.app:app --host 0.0.0.0 --port 8000 --reload

#!/usr/bin/env bash
set -euo pipefail

# Run from repo root
cd "$(dirname "$0")"

if [[ ! -d ".venv" ]]; then
  echo "[run.sh] Creating virtual environment..."
  python3 -m venv .venv
fi

echo "[run.sh] Activating virtual environment..."
source .venv/bin/activate

echo "[run.sh] Installing requirements..."
pip install -r requirements.txt

if [[ ! -f ".env" ]]; then
  echo "[run.sh] .env not found. Creating from .env.example..."
  cp .env.example .env
  echo "[run.sh] Please edit .env with real values, then re-run."
  exit 1
fi

echo "[run.sh] Running..."
python cli.py

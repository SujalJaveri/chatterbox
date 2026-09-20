#!/usr/bin/env bash
# Chatterbox AI Voice Generator - 1-Click Launcher for macOS & Linux

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "======================================================="
echo "       Chatterbox AI Voice Generator Launcher"
echo "======================================================="
echo ""

# Find python 3.11 or python3
if [ -f ".venv/bin/python" ]; then
    PY_CMD=".venv/bin/python"
else
    if command -v python3.11 &>/dev/null; then
        BASE_PY="python3.11"
    elif command -v python3 &>/dev/null; then
        BASE_PY="python3"
    else
        echo "[ERROR] Python 3 is not installed. Please install Python 3.11."
        exit 1
    fi

    echo "Creating virtual environment (.venv)..."
    $BASE_PY -m venv .venv
    PY_CMD=".venv/bin/python"

    echo "Installing dependencies..."
    $PY_CMD -m pip install --upgrade pip
    $PY_CMD -m pip install -r requirements.txt
fi

echo ""
echo "Launching Chatterbox AI Voice Generator..."
echo "Opening in browser at http://127.0.0.1:7860"
echo ""
$PY_CMD app.py

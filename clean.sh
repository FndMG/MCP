#!/bin/bash
# Remove __pycache__ and venv directories

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Cleaning: $SCRIPT_DIR"

# Remove __pycache__
find "$SCRIPT_DIR" -type d -name "__pycache__" -print -exec rm -rf {} +

# Remove venv
if [ -d "$SCRIPT_DIR/venv" ]; then
    echo "Removing: $SCRIPT_DIR/venv"
    rm -rf "$SCRIPT_DIR/venv"
fi

if [ -d "$SCRIPT_DIR/.venv" ]; then
    echo "Removing: $SCRIPT_DIR/.venv"
    rm -rf "$SCRIPT_DIR/.venv"
fi

echo "Done."

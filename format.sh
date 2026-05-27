#!/bin/zsh

# fail on any error
set -e

# move to script directory
cd "$(dirname "$0")"

echo "=== isort ==="
python3 -m isort .

echo "=== black ==="
python3 -m black .

echo "=== flake8 ==="
python3 -m flake8 .

echo "=== mypy ==="
python3 -m mypy .

echo "All checks complete."
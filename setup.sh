#!/bin/bash
# ──────────────────────────────────────────────
# Security Guardian — Dev Environment Setup
# Run once when cloning the repo: bash setup.sh
# ──────────────────────────────────────────────

set -euo pipefail

echo ""
echo "──────────────────────────────────────────"
echo "  Security Guardian — Environment Setup"
echo "──────────────────────────────────────────"

# Move to script directory
cd "$(dirname "$0")"

# ── 1. Check Python version ──────────────────
echo ""
echo "▸ Checking Python version..."

if ! command -v python3 >/dev/null 2>&1; then
    echo "❌ Python3 not found. Install Python first."
    exit 1
fi

python3 --version

# ── 2. Create virtual environment ────────────
echo ""
if [ ! -d ".venv" ]; then
    echo "▸ Creating virtual environment (.venv)..."
    python3 -m venv .venv
else
    echo "▸ .venv already exists — skipping creation."
fi

# ── 3. Activate venv ─────────────────────────
echo ""
echo "▸ Activating virtual environment..."
source .venv/bin/activate

# ── 4. Upgrade pip ───────────────────────────
echo ""
echo "▸ Upgrading pip..."
python3 -m pip install --upgrade pip --quiet

# ── 5. Install dependencies ──────────────────
echo ""

if [ ! -f "requirements.txt" ]; then
    echo "❌ requirements.txt not found."
    exit 1
fi

echo "▸ Installing dependencies..."
python3 -m pip install -r requirements.txt

# ── 6. Create .env if it doesn't exist ───────
echo ""

if [ ! -f ".env" ]; then
    echo "▸ Creating .env template..."

    cat > .env << 'EOF'
# ── Security Guardian Environment Variables ──
GEMINI_API_KEY=your_api_key_here
EOF

    echo "⚠️  .env created — add your GEMINI_API_KEY before running."
else
    echo "▸ .env already exists — skipping."
fi

# ── 7. Done ───────────────────────────────────
echo ""
echo "──────────────────────────────────────────"
echo "✅ Setup complete!"
echo ""
echo "Activate venv:"
echo "source .venv/bin/activate"
echo ""
echo "Run app:"
echo "python3 guard.py"
echo "──────────────────────────────────────────"
echo ""
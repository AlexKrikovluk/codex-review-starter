#!/usr/bin/env bash
set -euo pipefail

echo "🔄 Migrating from v1.1 to v1.2..."

# Backup configs
if [ -f .env ]; then
    cp .env .env.backup
    echo "✅ Backed up .env"
fi

if [ -f scripts/multi_repo.json ]; then
    cp scripts/multi_repo.json scripts/multi_repo.json.backup
    echo "✅ Backed up multi_repo.json"
fi

# Pull latest
echo "📥 Pulling latest changes..."
git pull origin main

# Install new dependencies
echo "📦 Installing new dependencies..."
if command -v code >/dev/null 2>&1; then
    echo "  VS Code detected. Install extension:"
    echo "  code --install-extension extensions/codex-review-alerts/codex-review-alerts-1.0.0.vsix"
fi

# Restore configs
if [ -f .env.backup ]; then
    mv .env.backup .env
    echo "✅ Restored .env"
fi

if [ -f scripts/multi_repo.json.backup ]; then
    mv scripts/multi_repo.json.backup scripts/multi_repo.json
    echo "✅ Restored multi_repo.json"
fi

echo "🎉 Migration complete!"
echo ""
echo "New features available:"
echo "  - VS Code extension: extensions/codex-review-alerts/"
echo "  - Web dashboard: dashboard/"
echo "  - Templates: templates/django/, templates/flask/"
echo "  - Docs: docs/VSCODE_EXTENSION.md, docs/DASHBOARD.md"

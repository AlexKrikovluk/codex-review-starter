#!/usr/bin/env bash
set -euo pipefail

echo "🔄 Migrating from v1.0 to v1.1..."

# Backup .env if it exists
if [ -f .env ]; then
    cp .env .env.backup
    echo "✅ Backed up .env to .env.backup"
fi

# Pull latest changes
echo "📥 Pulling latest changes..."
git pull origin main

# Install new dependencies if needed
echo "📦 Installing new dependencies..."
if command -v pip >/dev/null 2>&1; then
    pip install -r requirements.txt 2>/dev/null || true
fi

# Create multi-repo config if it doesn't exist
if [ ! -f scripts/multi_repo.json ]; then
    echo "📝 Creating multi_repo.json template..."
    cat > scripts/multi_repo.json <<'EOF'
{
  "repos": [
    {
      "name": "my-repo",
      "url": "https://github.com/yourname/yourrepo.git",
      "path": "/path/to/your/repo",
      "schedule": "Mon,Wed,Fri 09:00:00"
    }
  ]
}
EOF
fi

# Restore .env if it was backed up
if [ -f .env.backup ]; then
    mv .env.backup .env
    echo "✅ Restored .env"
fi

echo "🎉 Migration complete!"
echo ""
echo "New features available:"
echo "  - FastAPI template: templates/fastapi/"
echo "  - Multi-repo: scripts/multi_repo.sh"
echo "  - Alerts: scripts/alerts/"
echo "  - Docker: docker-compose.yml"
echo "  - Docs: docs/GITHUB_APP.md, docs/MULTI_REPO.md"
echo ""
echo "Next steps:"
echo "  1. Edit scripts/multi_repo.json with your repos"
echo "  2. Configure alert webhooks in .env"
echo "  3. Try: ./scripts/multi_repo.sh all"

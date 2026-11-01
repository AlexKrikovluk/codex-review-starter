#!/usr/bin/env bash
set -euo pipefail

# Multi-repo orchestration for Codex Review Setup
# Usage: ./multi_repo.sh [repo_name]

source "$(dirname "$0")/lib.sh"

REPO_NAME="${1:-all}"
CONFIG_FILE="$(dirname "$0")/multi_repo.json"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "❌ Config file not found: $CONFIG_FILE"
    echo "Create it with repos array:"
    echo '[{"name":"repo1","url":"https://github.com/user/repo1.git","path":"/path/to/repo1"}]'
    exit 1
fi

run_repo() {
    local name="$1"
    local url="$2"
    local path="$3"

    echo "🔁 Reviewing $name..."
    if [ ! -d "$path" ]; then
        echo "  ⚠️  Path not found: $path"
        return 1
    fi

    pushd "$path" >/dev/null
    bash "$(dirname "$0")/codex_review.sh"
    popd >/dev/null
}

if [ "$REPO_NAME" = "all" ]; then
    python3 -c "
import json
from pathlib import Path
config = json.loads(Path('$CONFIG_FILE').read_text())
for repo in config['repos']:
    print(f\"{repo['name']}|{repo['url']}|{repo['path']}\")
" | while IFS='|' read -r name url path; do
        run_repo "$name" "$url" "$path"
    done
else
    python3 -c "
import json
from pathlib import Path
config = json.loads(Path('$CONFIG_FILE').read_text())
for repo in config['repos']:
    if repo['name'] == '$REPO_NAME':
        print(f\"{repo['name']}|{repo['url']}|{repo['path']}\")
        break
" | while IFS='|' read -r name url path; do
        if [ -z "$name" ]; then
            echo "❌ Repo not found: $REPO_NAME"
            exit 1
        fi
        run_repo "$name" "$url" "$path"
    done
fi

echo "✅ Multi-repo review complete"

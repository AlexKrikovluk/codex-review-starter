#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPORT_DIR="$HOME/.hermes/cron/output/news-digest"
DATE=$(date +%Y-%m-%d)
REPORT="$REPORT_DIR/digest-$DATE.md"
mkdir -p "$REPORT_DIR"

# Use project venv if available
VENV="$HOME/projects/codex-review-starter/.venv"
if [ -x "$VENV/bin/python" ]; then
  PYTHON="$VENV/bin/python"
else
  PYTHON=python3
fi

"$PYTHON" "$SCRIPT_DIR/news-monitor.py" --date "$DATE" --output "$REPORT"

echo "$REPORT"

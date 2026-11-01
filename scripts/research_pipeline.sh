#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="${1:-.}"
TOPIC="${2:-AI coding agents}"
OUTPUT_DIR="$REPO/research"
LOG_DIR="$OUTPUT_DIR"
SLUG="$(echo "$TOPIC" | tr '[:upper:]' '[:lower:]' | tr -cs 'a-z0-9' '-' | sed 's/^-*//;s/-*$//')"
REPORT="$OUTPUT_DIR/${SLUG}.md"
LOG="$OUTPUT_DIR/cron.log"

# shellcheck source=scripts/lib.sh
source "$SCRIPT_DIR/lib.sh"

ensure_dirs "$OUTPUT_DIR" "$LOG_DIR"

{
  echo "=== $(date -Iseconds) ==="
  echo "Topic: $TOPIC"
  set +e
  "$CODEX_BIN" --sandbox workspace-write exec "Run a quick research pass on: $TOPIC. Use web_search/web_extract. Save a concise markdown summary with claims, sources, dates, and confidence to $REPORT. If no useful sources are found, write NO_RESULTS. End the report with exactly one line: RESULT: CLEAN or RESULT: ISSUES_FOUND." > /tmp/codex-research-$(date +%Y%m%d-%H%M%S).log 2>&1 || true
  set -e
  echo "Report: $REPORT"
} >> "$LOG" 2>&1

echo "Report: $REPORT"

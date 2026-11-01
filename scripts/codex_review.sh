#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="${1:-.}"
REPORT="$REPO/.codex/review.txt"
LOG="$REPO/.codex/cron.log"

# shellcheck source=scripts/lib.sh
source "$SCRIPT_DIR/lib.sh"

ensure_dirs "$REPO/.codex"

{
  echo "=== $(date -Iseconds) ==="
  echo "Running pytest..."
  set +e
  "$PIP_BIN" -m pytest -q || true
  set -e

  echo "Running Codex review..."
  set +e
  "$CODEX_BIN" --sandbox workspace-write exec "Review recent git changes in this repo. Summarize material issues only. Do not modify files. End the report with exactly one line: RESULT: CLEAN or RESULT: ISSUES_FOUND." > "$REPORT" 2>&1 || true
  set -e

  echo "Review output:"
  cat "$REPORT"

  result=$(parse_codex_result "$REPORT")
  if [ "$result" = "ISSUES_FOUND" ]; then
    echo "Material issues found, sending Telegram notification..."
    send_telegram "Codex review found material issues. Check $REPORT"
  elif [ "$result" = "CLEAN" ]; then
    echo "Review clean."
  else
    echo "Review output missing expected RESULT line."
    send_telegram "Codex review produced an invalid report. Check $REPORT"
  fi
} >> "$LOG" 2>&1

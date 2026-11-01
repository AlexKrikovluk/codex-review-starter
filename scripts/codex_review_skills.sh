#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPORT="${2:-$HOME/.hermes/.codex/skills-review.txt}"
LOG="$(dirname "$REPORT")/cron.log"

# shellcheck source=scripts/lib.sh
source "$SCRIPT_DIR/lib.sh"

ensure_dirs "$(dirname "$REPORT")"

{
  echo "=== $(date -Iseconds) ==="
  echo "Scanning skills..."
  set +e
  "$CODEX_BIN" --sandbox workspace-write exec "Review recent changes under \$HOME/.hermes/skills. Summarize material issues only. Do not modify files. End the report with exactly one line: RESULT: CLEAN or RESULT: ISSUES_FOUND." > "$REPORT" 2>&1 || true
  set -e

  echo "Review output:"
  cat "$REPORT"

  result=$(parse_codex_result "$REPORT")
  if [ "$result" = "ISSUES_FOUND" ]; then
    echo "Material issues found, sending Telegram notification..."
    send_telegram "Codex review found material issues in skills. Check $REPORT"
  elif [ "$result" = "CLEAN" ]; then
    echo "Review clean."
  else
    echo "Review output missing expected RESULT line."
    send_telegram "Codex review for skills produced an invalid report. Check $REPORT"
  fi
} >> "$LOG" 2>&1

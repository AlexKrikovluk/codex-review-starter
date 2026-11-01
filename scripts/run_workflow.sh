#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="${1:-.}"
MODE="${2:-full}"

case "$MODE" in
  review|improve|test|full) ;;
  *) echo "Unsupported mode: $MODE"; exit 2 ;;
esac

# shellcheck source=scripts/lib.sh
source "$SCRIPT_DIR/lib.sh"

REPORT_DIR="$REPO/.codex/reports"
ensure_dirs "$REPORT_DIR"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
REPORT="$REPORT_DIR/$TIMESTAMP-$MODE.md"
CODEX_REPORT="/tmp/codex-report-$TIMESTAMP-$MODE.md"
LOG="$REPORT_DIR/cron.log"
CODEX_LOG="/tmp/codex-dev-workflow-$TIMESTAMP.log"
TEST_LOG="/tmp/codex-pytest-$TIMESTAMP.log"

{
  echo "=== $(date -Iseconds) ==="
  echo "Repo: $REPO"
  echo "Mode: $MODE"

  

  echo "Running baseline tests..."
  set +e
  run_pytest "$REPO" "$TEST_LOG"
  TEST_EXIT=$?
  set -e
  echo "Test exit code: $TEST_EXIT"
  echo "Test output:"
  cat "$TEST_LOG"

  PROMPT="Run a $MODE workflow for this repo. Follow the dev-workflow skill rules. Save the report to $CODEX_REPORT using the review-report template structure. Do not modify files unless in improve mode and changes are small. If material issues are found, include them with severity. Baseline pytest exit code was $TEST_EXIT; include that in the report."

  echo "Running Codex..."
  set +e
  run_codex "$PROMPT" "$CODEX_LOG"
  CODEX_EXIT=$?
  set -e

  echo "Codex exit code: $CODEX_EXIT"
  echo "Codex output:"
  cat "$CODEX_LOG"

  if [ -f "$CODEX_REPORT" ]; then
    mv "$CODEX_REPORT" "$REPORT"
    echo "Report saved to: $REPORT"
    echo "Report content:"
    cat "$REPORT"
  else
    echo "No report generated. Codex may have failed."
    if [ "$CODEX_EXIT" -ne 0 ]; then
      echo "Sending Telegram notification about failure..."
      send_telegram "Dev workflow ($MODE) failed for $REPO. Check $CODEX_LOG"
    fi
  fi
} >> "$LOG" 2>&1

echo "Report: $REPORT"

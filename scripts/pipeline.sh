#!/bin/bash
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="${1:-.}"

# shellcheck source=scripts/lib.sh
source "$SCRIPT_DIR/lib.sh"

REPORT_DIR="$REPO/.codex/reports"
LOG_DIR="$REPO/.codex"
ensure_dirs "$REPORT_DIR" "$LOG_DIR"
TIMESTAMP="$(date +%Y%m%d-%H%M%S)"
PIPELINE_LOG="$LOG_DIR/pipeline-$TIMESTAMP.log"
PIPELINE_REPORT="$REPORT_DIR/$TIMESTAMP-pipeline.md"
RESEARCH_REPORT="$REPO/research/pipeline-$TIMESTAMP.md"
TEST_LOG="/tmp/codex-pipeline-pytest-$TIMESTAMP.log"
REVIEW_LOG="/tmp/codex-pipeline-review-$TIMESTAMP.log"
RESEARCH_LOG="/tmp/codex-pipeline-research-$TIMESTAMP.log"

{
  echo "# Pipeline Report"
  echo ""
  echo "- **Repo:** $REPO"
  echo "- **Date:** $(date -Iseconds)"
  echo "- **Host:** $(hostname)"
  echo ""

  echo "## 1. Tests"
  set +e
  run_pytest "$REPO" "$TEST_LOG"
  TEST_EXIT=$?
  set -e
  echo "- Exit code: $TEST_EXIT"
  echo ""

  echo "## 2. Codex review"
  set +e
  run_codex "Review recent git changes in this repo. Summarize material issues only. Do not modify files. End the report with exactly one line: RESULT: CLEAN or RESULT: ISSUES_FOUND." "$REVIEW_LOG"
  REVIEW_EXIT=$?
  set -e
  echo "### Review output"
  cat "$REVIEW_LOG"
  echo ""
  result=$(parse_codex_result "$REVIEW_LOG")
  if [ "$result" = "ISSUES_FOUND" ]; then
    echo "- **Result:** ISSUES_FOUND"
  elif [ "$result" = "CLEAN" ]; then
    echo "- **Result:** CLEAN"
  else
    echo "- **Result:** INVALID"
  fi
  echo ""

  echo "## 3. Research pipeline"
  set +e
  "$CODEX_BIN" --sandbox workspace-write exec "Run a quick research pass on: ${PIPELINE_TOPIC:-AI coding agents}. Use web_search/web_extract. Save a concise markdown summary with claims, sources, dates, and confidence to $RESEARCH_REPORT. End the report with exactly one line: RESULT: CLEAN or RESULT: ISSUES_FOUND." > "$RESEARCH_LOG" 2>&1 || true
  RESEARCH_EXIT=$?
  set -e
  if [ -f "$RESEARCH_REPORT" ]; then
    echo "- Report: $RESEARCH_REPORT"
    tail -n 20 "$RESEARCH_REPORT"
  else
    echo "- No research report generated"
  fi
  echo ""

  echo "## 4. Summary"
  if [ "$TEST_EXIT" -eq 0 ]; then
    echo "- Tests: PASS"
  else
    echo "- Tests: FAIL"
  fi
  if [ "$REVIEW_EXIT" -eq 0 ] && [ "$result" = "CLEAN" ]; then
    echo "- Review: PASS"
  else
    echo "- Review: FAIL or INVALID"
  fi
  if [ "$RESEARCH_EXIT" -eq 0 ] && [ -f "$RESEARCH_REPORT" ]; then
    echo "- Research: PASS"
  else
    echo "- Research: FAIL"
  fi
} > "$PIPELINE_REPORT" 2>&1

echo "Pipeline report: $PIPELINE_REPORT"

if [ "$TEST_EXIT" -ne 0 ] || [ "$result" = "ISSUES_FOUND" ] || [ "$RESEARCH_EXIT" -ne 0 ]; then
  send_telegram "Pipeline had issues. Check $PIPELINE_REPORT"
else
  send_telegram "Pipeline passed. Check $PIPELINE_REPORT"
fi

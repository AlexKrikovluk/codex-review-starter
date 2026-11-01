#!/bin/bash
set -euo pipefail

export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export PIP_BIN="${PIP_BIN:-python3 -m pytest}"
export CODEX_BIN="${CODEX_BIN:-codex}"
export HERMES_SEND="${HERMES_SEND:-hermes send --to telegram}"

ensure_dirs() {
  local report_dir="$1"
  local log_dir="${2:-$report_dir}"
  mkdir -p "$report_dir" "$log_dir"
}

run_pytest() {
  local repo="$1"
  local test_log="${2:-/tmp/codex-pytest-$(date +%Y%m%d-%H%M%S).log}"
  set +e
  (cd "$repo" && "$PIP_BIN" -m pytest -q) > "$test_log" 2>&1
  local exit_code=$?
  set -e
  echo "$test_log"
  return "$exit_code"
}

run_codex() {
  local prompt="$1"
  local stdout_file="${2:-/tmp/codex-out-$(date +%Y%m%d-%H%M%S).log}"
  set +e
  "$CODEX_BIN" --sandbox workspace-write exec "$prompt" > "$stdout_file" 2>&1
  local exit_code=$?
  set -e
  echo "$stdout_file"
  return "$exit_code"
}

parse_codex_result() {
  local report_file="$1"
  if [ -s "$report_file" ] && grep -q '^RESULT: ISSUES_FOUND$' "$report_file"; then
    echo "ISSUES_FOUND"
  elif [ -s "$report_file" ] && grep -q '^RESULT: CLEAN$' "$report_file"; then
    echo "CLEAN"
  else
    echo "INVALID"
  fi
}

send_telegram() {
  local message="$1"
  if command -v hermes >/dev/null 2>&1; then
    $HERMES_SEND "$message"
  fi
}

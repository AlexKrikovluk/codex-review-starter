# 🔁 Codex Review Setup — Automated code reviews for Python projects

Hey everyone,

I automated code reviews for my Python repo using Codex CLI + systemd timers + Telegram alerts.

**Before:**
- Manual review when I remembered
- Inconsistent CI checks
- No automated research on dependencies/trends
- Forgotten reviews → missed issues
- Scattered scripts and cron jobs

**After:**
- Scheduled Codex reviews Mon/Wed/Thu
- Telegram alerts on material issues only
- Research pipeline runs automatically
- pytest + coverage + mypy + ruff in CI
- Centralized scripts with shared library
- Systemd timers with journal logging

**Results:**
- 31 passing tests
- 94.69% code coverage
- Clean mypy strict type check
- 0 critical issues in last review
- ~1 hour setup time

Template is open source if you want to set it up yourself: https://github.com/AlexKrikovluk/codex-review-starter

I'm also offering paid setup for indie devs — first 3 at 20% off.

#devtools #automation #python #opensource #codequality

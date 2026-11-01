# First Post — X/Twitter

**Thread:**

1/ I automated code reviews for my Python repo.

Codex CLI + systemd timers + Telegram alerts.

Now it reviews itself 3x/week and I only get pinged for actual issues.

Template: https://github.com/AlexKrikovluk/codex-review-starter

2/ Before:
- Manual review when remembered
- Inconsistent CI checks
- No automated research
- Missed issues

After:
- Scheduled reviews Mon/Wed/Thu
- Telegram alerts on material issues only
- Research pipeline runs automatically
- pytest + coverage + mypy + ruff in CI

3/ Results:
- 31 passing tests
- 94.69% coverage
- Clean mypy strict
- 0 critical issues

Setup time: ~1 hour.

Buy the ready-to-use package: https://krikovluk.gumroad.com/l/httpsgithubcomAlexKrikovlukcodex-review-starter

#devtools #python #automation #opensource

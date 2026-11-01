# First Post — Reddit r/selfhosted

**Title:** I automated code reviews for my Python repo — Codex CLI + systemd + Telegram

**Body:**
I built a fully self-hosted review stack for Python projects. No SaaS, no cloud dependency — everything runs on my machine via systemd timers.

What it does:
- Scheduled Codex CLI reviews (Mon/Wed/Thu)
- pytest + coverage + mypy + ruff in GitHub Actions
- Telegram alerts only for material issues
- Research pipeline for any topic
- Centralized scripts with shared library

Results:
- 31 passing tests
- 94.69% coverage
- mypy strict — zero errors
- 0 critical issues in last review

Template is open source if you want to DIY: https://github.com/AlexKrikovluk/codex-review-starter

I also made it a $29 digital product for those who want the ready-to-use package.

Happy to answer questions.

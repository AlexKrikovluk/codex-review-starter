# Show HN: Codex Review Setup — Automated code reviews for Python repos

I built a fully automated review stack for Python projects using Codex CLI, systemd timers, and Telegram alerts.

**What it does:**
- Runs Codex CLI reviews on a schedule (Mon/Wed/Thu)
- pytest + coverage + mypy + ruff in CI
- Alerts only for material issues via Telegram
- Research pipeline for any topic
- Uses systemd user timers instead of cron

**Why I built it:**
I kept forgetting to review my own code. Manual reviews are easy to skip and hard to schedule. This stack automates the boring parts and only notifies me when something actually needs attention.

**Template:** https://github.com/AlexKrikovluk/codex-review-starter

I'm also offering setup services for indie devs who want it done for them.

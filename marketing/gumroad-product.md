# Codex Review Setup

Automated code reviews for Python repos — Codex CLI, systemd timers, Telegram alerts, GitHub Actions CI.

---

## Stop forgetting to review your own code

Manual reviews are easy to skip. Issues slip through. CI only runs when you push.

This template turns your repo into a self-reviewing project. It runs on a schedule, checks quality gates automatically, and only alerts you when something actually needs attention.

No more "I'll review it later." No more missed issues. No more review fatigue.

---

## What you get

- **6 production-ready bash scripts** — review, research, pipeline, alerts
- **5 systemd user service/timer units** — Mon/Wed/Thu 9am, no cron
- **GitHub Actions CI** — lint, tests, coverage, mypy, ruff, secret scan
- **pytest suite** — 94.69% coverage example included
- **Research pipeline** — auto-generate topic reports with citations
- **Telegram alerts** — only for material issues, no noise
- **Full documentation** — QUICKSTART, CONTRIBUTING, CHANGELOG
- **MIT license** — free to use commercially

**v1.1.0 Expansion Pack included:**
- FastAPI project template
- Multi-repo orchestration
- Discord/Slack/email alerts
- Docker Compose one-liner
- GitHub App integration guide

## Who this is for

- Solo developers who forget to review their own code
- Indie hackers shipping fast who need quality gates
- Python maintainers who want automated CI without the overhead
- Small teams without dedicated review resources

## Setup time

Under 1 hour. Clone, configure `.env`, run `install.sh`.

## Tech stack

- OpenAI Codex CLI (review + research)
- pytest + coverage + mypy + ruff
- systemd user timers
- Telegram bot notifications
- GitHub Actions

## Real results

Used on [python-scripts](https://github.com/AlexKrikovluk/python-scripts):

- 31 passing tests
- 94.69% coverage
- mypy strict — zero errors
- 3x/week automated reviews
- Telegram alerts only for material issues

---

## Price

**$29** one-time

Instant download + GitHub access. No subscription. No support. Use it, modify it, ship it.

---

## FAQ

**Do I need Codex CLI installed?**
Yes, but it takes 5 minutes to authorize. The template includes setup instructions.

**Can I customize the schedule?**
Yes — systemd timers are easy to modify. Default is Mon/Wed/Thu 9am.

**What if I don't use Telegram?**
Alerts can go to Discord, Slack, or email. The template shows how to switch.

**Do you offer support?**
No — this is a digital product, not a service. The docs and community should cover most use cases.

**Can I use this for commercial projects?**
Yes — MIT license, free to use commercially.

---

## License

MIT — free to use, modify, and ship.

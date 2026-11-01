# Codex Review Setup

Automated code reviews for Python repos — Codex CLI, systemd timers, Telegram alerts, GitHub Actions CI.

---

## Stop forgetting to review your own code

Manual reviews are easy to skip. Issues slip through. CI only runs when you push.

This template turns your repo into a self-reviewing project. It runs on a schedule, checks quality gates automatically, and only alerts you when something actually needs attention.

---

## What you get

- **6 ready-to-use bash scripts** with shared library
- **5 systemd user service/timer units** — Mon/Wed/Thu 9am
- **GitHub Actions CI** — lint, tests, coverage, mypy, ruff, secret scan
- **pytest suite** — 94.69% coverage example included
- **Research pipeline** — auto-generate topic reports
- **Telegram alerts** — only for material issues
- **Full docs** — QUICKSTART, CONTRIBUTING, CHANGELOG
- **MIT license** — free to use commercially

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

## Results

We used this on the [python-scripts](https://github.com/AlexKrikovluk/python-scripts) repo:

- 31 passing tests
- 94.69% coverage
- mypy strict — zero errors
- 3x/week automated reviews
- Telegram alerts only for material issues

---

## Price

$29 one-time

Instant download + GitHub access.

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

---

## License

MIT — free to use, modify, and ship.

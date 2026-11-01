# Codex Review Setup

Automated code reviews for Python projects using OpenAI Codex CLI, pytest, and systemd timers.

Most repos rely on manual PR reviews or occasional CI runs. That leaves gaps between commits and bugs slipping through. Codex Review Setup gives you scheduled, structured reviews without changing your workflow.

**What it does:**
- Runs Codex CLI reviews on your repo on a schedule
- Executes pytest with coverage and type checking
- Sends Telegram alerts only for material issues
- Uses systemd user timers instead of cron
- Includes GitHub Actions CI with lint, tests, and secret scan

**What you get:**
- 6 ready-to-use bash scripts
- 5 systemd unit files
- Full CI workflow
- Documentation and quickstart guide

**Pricing:** $297-$797 for setup services, or free template for DIY.

**Use cases:**
- Solo devs who want automated quality gates
- Small teams without dedicated review resources
- Open source maintainers
- Indie hackers shipping fast

Built by AlexKrikovluk. Template: github.com/AlexKrikovluk/codex-review-starter

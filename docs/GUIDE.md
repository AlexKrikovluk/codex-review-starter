# Codex Review Setup — Complete Setup Guide

**Version:** 1.0.0  
**Price:** $29  
**License:** MIT

---

## Table of Contents

1. Introduction
2. Prerequisites
3. Installation
4. Configuration
5. Running Your First Review
6. Customizing the Schedule
7. Understanding the Scripts
8. CI/CD Integration
9. Troubleshooting
10. Advanced Usage
11. Legal & License

---

## 1. Introduction

This guide walks you through setting up automated code reviews for your Python repository using Codex CLI, systemd timers, and Telegram alerts.

**What you'll get:**
- Scheduled Codex reviews every Monday, Wednesday, and Thursday
- Automatic research pipeline for any topic
- Telegram notifications only for material issues
- Full GitHub Actions CI with lint, tests, coverage, mypy, ruff, and secret scan
- Production-ready bash scripts with shared library

**Time to complete:** 45-60 minutes

---

## 2. Prerequisites

Before you begin, ensure you have:

- **Python 3.14+** installed
- **Codex CLI** authorized (`codex --version` works)
- **Telegram bot token** from [@BotFather](https://t.me/BotFather)
- **Git** installed
- **GitHub repository** with tests

### Getting a Telegram Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/BotFather)
2. Send `/newbot`
3. Follow the prompts to name your bot
4. Copy the token (format: `123456:ABC-DEF...`)
5. Save it somewhere safe

### Getting Your Telegram Chat ID

1. Send any message to your bot
2. Visit `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
3. Find `"chat":{"id":...}` in the response
4. Copy the numeric ID

---

## 3. Installation

### Step 1: Clone the Template

```bash
git clone https://github.com/AlexKrikovluk/codex-review-starter.git
cd codex-review-starter
```

### Step 2: Install Dependencies

```bash
python -m pip install pytest pytest-cov mypy ruff
```

### Step 3: Copy Environment File

```bash
cp .env.example .env
```

### Step 4: Configure Environment

Edit `.env` with your values:

```env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
TELEGRAM_CHAT_ID=756046528
OPENAI_API_KEY=sk-...
REPO_URL=https://github.com/yourname/yourrepo.git
CODEX_MODEL=o3
ALERT_ONLY_MATERIAL=true
```

### Step 5: Run Install Script

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

This will:
- Link systemd units to `~/.config/systemd/user/`
- Reload systemd daemon
- Enable all timers

---

## 4. Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TELEGRAM_BOT_TOKEN` | Bot token from @BotFather | Yes |
| `TELEGRAM_CHAT_ID` | Your Telegram chat ID | Yes |
| `OPENAI_API_KEY` | OpenAI API key for Codex CLI | Yes |
| `REPO_URL` | GitHub repo to review | Yes |
| `CODEX_MODEL` | Codex model to use | No (default: o3) |
| `ALERT_ONLY_MATERIAL` | Alert only on material issues | No (default: true) |

### Systemd Timers

The template includes 3 timers:

1. **codex-review@.timer** — Runs Codex review on your repo (Mon/Wed/Thu 9am)
2. **codex-review-skills.timer** — Reviews Hermes skills (Wed 9am)
3. **research-pipeline.timer** — Runs research pipeline (Thu 9am)

To customize schedule, edit the timer files in `systemd/user/`:

```bash
# Example: change to Tue/Thu/Sat at 10am
# OnCalendar=Tue,Thu,Sat 10:00:00
```

Then reload:

```bash
systemctl --user daemon-reload
systemctl --user restart codex-review@.timer
```

---

## 5. Running Your First Review

### Manual Review

```bash
./scripts/codex_review.sh
```

### Check Timer Status

```bash
systemctl --user list-timers
```

### View Logs

```bash
journalctl --user -u codex-review -f
```

### Run Tests

```bash
pytest
```

---

## 6. Customizing the Schedule

### Changing Timer Frequency

Edit `systemd/user/codex-review@.timer`:

```ini
[Timer]
OnCalendar=Mon,Wed,Fri 09:00:00
Persistent=true
```

Supported formats:
- `Mon,Wed,Fri 09:00:00` — specific days
- `daily 09:00:00` — every day
- `weekly 09:00:00` — once a week
- `*-*-* 09:00:00` — every day at 9am

### Disabling a Timer

```bash
systemctl --user disable --now codex-review@.timer
```

### Enabling a Timer

```bash
systemctl --user enable --now codex-review@.timer
```

---

## 7. Understanding the Scripts

### scripts/lib.sh

Shared library with common functions:

- `ensure_dirs` — Create required directories
- `run_pytest` — Run pytest with coverage
- `run_codex` — Execute Codex CLI review
- `parse_codex_result` — Parse Codex output
- `send_telegram` — Send Telegram alerts

### scripts/codex_review.sh

Main review script. Runs Codex CLI on your repo and sends alerts.

### scripts/research_pipeline.sh

Runs automated research on any topic. Generates markdown reports with citations.

### scripts/pipeline.sh

Combined pipeline: runs tests, Codex review, and research in sequence.

### scripts/run_workflow.sh

Dev workflow runner. Executes full workflow with reporting.

---

## 8. CI/CD Integration

### GitHub Actions

The template includes `.github/workflows/ci.yml` with 4 jobs:

1. **lint-and-type** — ruff + mypy
2. **test** — pytest + coverage
3. **security** — secret scan
4. **workflow** — bash syntax validation

### Enabling CI

1. Go to your repo Settings → Actions
2. Enable GitHub Actions
3. Push the `.github/workflows/ci.yml` file
4. CI will run on every push/PR

### Customizing CI

Edit `.github/workflows/ci.yml` to:
- Change Python version
- Add/remove jobs
- Adjust coverage threshold
- Add notifications

---

## 9. Troubleshooting

### Codex CLI Not Found

```bash
# Verify installation
codex --version

# If not found, install:
npm install -g @openai/codex
codex auth login
```

### Telegram Bot Not Responding

1. Check token is correct in `.env`
2. Verify chat ID is correct
3. Ensure bot is not blocked
4. Check `journalctl --user -u hermes-gateway` for errors

### Timer Not Running

```bash
# Check timer status
systemctl --user status codex-review@.timer

# Check service logs
journalctl --user -u codex-review@.service

# Reload and restart
systemctl --user daemon-reload
systemctl --user restart codex-review@.timer
```

### mypy Errors in Tests

If you see mypy errors in test files, add type annotations:

```python
def test_something() -> None:
    ...
```

Or configure `mypy.ini` to ignore tests:

```ini
[mypy-tests.*]
ignore_errors = True
```

### pytest Not Found

Ensure you're using the project venv:

```bash
source /tmp/codex-hermes-work/.venv/bin/activate
pytest
```

---

## 10. Advanced Usage

### Adding Custom Scripts

Create a new script in `scripts/` and source `lib.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/lib.sh"

# Your custom logic here
ensure_dirs
run_codex "your custom prompt"
```

### Custom Telegram Alerts

Edit `scripts/lib.sh` to customize alert format:

```bash
send_telegram() {
    local message="$1"
    # Custom formatting
    echo "$message" | telegram-send --config .env
}
```

### Multi-Repo Setup

To monitor multiple repos, create multiple timer instances:

```bash
systemctl --user enable --now codex-review@repo1.timer
systemctl --user enable --now codex-review@repo2.timer
```

---

## 11. Legal & License

### MIT License

This template is released under the MIT License. You are free to:

- Use commercially
- Modify and adapt
- Distribute copies
- Include in proprietary software

### Attribution

Attribution is appreciated but not required. If you use this template in a public project, a mention or star on GitHub helps.

### No Warranty

This software is provided "as is", without warranty of any kind. Use at your own risk.

---

## Support

This is a digital product, not a service. For issues:

1. Check the troubleshooting section
2. Search existing GitHub issues
3. Open a new issue with details

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

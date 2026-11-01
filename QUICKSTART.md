# Quick Start

Get automated Codex review up and running in 4 steps.

## Prerequisites

- Python 3.14+
- OpenAI Codex CLI authorized (`codex auth login`)
- Telegram bot token (optional, for alerts)
- Git repo with tests

## Step 1: Copy Scripts

```bash
cp -r scripts/ /path/to/your/repo/scripts/
chmod +x /path/to/your/repo/scripts/*.sh
```

## Step 2: Install Dev Dependencies

```bash
python -m pip install pytest pytest-cov mypy ruff
```

## Step 3: Configure Systemd Timers (Linux)

```bash
cp systemd/user/*.service ~/.config/systemd/user/
cp systemd/user/*.timer ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now codex-review.timer codex-review-skills.timer
```

## Step 4: Verify

```bash
bash scripts/codex_review.sh
journalctl --user -u codex-review -f
```

## What's Next

- Customize `scripts/lib.sh` paths for your project
- Adjust timer schedules in `.timer` files
- Add your Telegram chat ID to alerts
- Enable GitHub Actions by copying `.github/workflows/ci.yml`

## Support

- Docs: [link to docs]
- Issues: [link to issues]
- Contact: [your contact]

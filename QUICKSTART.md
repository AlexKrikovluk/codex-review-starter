# Quick Start

Get Codex Review Setup running in 5 minutes.

## Prerequisites

- Python 3.14+
- Codex CLI authorized (`codex --version` works)
- Telegram bot token from [@BotFather](https://t.me/BotFather)
- Git

## Installation

```bash
git clone https://github.com/AlexKrikovluk/codex-review-starter.git
cd codex-review-starter
cp .env.example .env
chmod +x scripts/install.sh
./scripts/install.sh
```

## Configuration

Edit `.env`:

```env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
TELEGRAM_CHAT_ID=your_chat_id_here
OPENAI_API_KEY=sk-...
REPO_URL=https://github.com/yourname/yourrepo.git
CODEX_MODEL=o3
ALERT_ONLY_MATERIAL=true
```

## Verify

```bash
# Check timers
systemctl --user list-timers

# Run a manual review
./scripts/codex_review.sh

# Run tests
pytest
```

## What's Next

- Customize schedule in `systemd/user/*.timer`
- Add custom scripts to `scripts/`
- Enable GitHub Actions in your repo settings
- Add screenshots to `docs/screenshots/` for your README

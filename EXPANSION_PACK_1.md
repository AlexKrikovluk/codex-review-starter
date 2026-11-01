# Expansion Pack 1 — FastAPI + GitHub App + Multi-Platform Alerts

**Release:** v1.1.0  
**Price:** Free update for existing buyers  
**New features:**
- FastAPI project template with automated reviews
- GitHub App integration for PR comments
- Discord/Slack/email alert templates
- Multi-repo orchestration script
- Docker Compose one-liner deploy

---

## What's New

### 1. FastAPI Project Template

New template for FastAPI projects with:
- Pre-configured pytest + coverage + mypy
- Automated Codex reviews for API endpoints
- Telegram/Discord/Slack alerts
- systemd timers

### 2. GitHub App Integration

Automated PR reviews via GitHub App:
- Codex reviews posted as PR comments
- Status checks on PRs
- Auto-merge gates for critical issues

### 3. Multi-Platform Alerts

New alert backends:
- Discord webhooks
- Slack incoming webhooks
- Email via SMTP
- Keep Telegram as default

### 4. Multi-Repo Orchestration

New script `scripts/multi_repo.sh`:
- Monitor multiple repos from one place
- Centralized alert routing
- Per-repo schedule customization

### 5. Docker Compose Deploy

One-liner deployment:
```bash
docker compose up -d
```

Includes:
- Codex review worker
- Alert dispatcher
- Research pipeline
- All on one network

---

## Installation

```bash
# Pull latest changes
git pull origin main

# Run new install script
chmod +x scripts/install_expansion.sh
./scripts/install_expansion.sh
```

---

## Migration from v1.0

If you're upgrading from v1.0:

1. Backup your `.env` file
2. Pull latest changes
3. Run `scripts/migrate_v1_to_v1.1.sh`
4. Restore your `.env`
5. Restart timers: `systemctl --user daemon-reload && systemctl --user restart codex-review@.timer`

---

## New Files

- `templates/fastapi/` — FastAPI project template
- `scripts/multi_repo.sh` — multi-repo orchestration
- `scripts/github_app.py` — GitHub App integration
- `scripts/alerts/discord.sh` — Discord alerts
- `scripts/alerts/slack.sh` — Slack alerts
- `scripts/alerts/email.sh` — email alerts
- `docker-compose.yml` — one-liner deploy
- `docs/GITHUB_APP.md` — GitHub App setup guide
- `docs/MULTI_REPO.md` — multi-repo setup guide

---

## Breaking Changes

None. v1.1 is fully backward compatible with v1.0.

---

## Support

This is a digital product update. Check docs and existing issues for help.

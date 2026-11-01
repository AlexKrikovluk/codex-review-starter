#!/usr/bin/env bash
set -euo pipefail

echo "🚀 Installing Codex Review Setup..."

# Ensure required directories exist
mkdir -p ~/.config/systemd/user
mkdir -p ~/.config/logrotate.d
mkdir -p ~/.hermes/audio_cache

# Link systemd units
ln -sf "$(pwd)/systemd/user/"* ~/.config/systemd/user/ || true

# Reload systemd
systemctl --user daemon-reload

# Enable timers
systemctl --user enable --now codex-review@.timer || true
systemctl --user enable --now codex-review-skills.timer || true
systemctl --user enable --now research-pipeline.timer || true

echo "✅ Done. Timers enabled."
echo "📋 Check status: systemctl --user list-timers"
echo "🔔 Configure .env with your Telegram bot token and chat ID"

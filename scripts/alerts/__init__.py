"""Shared alert functions for multiple platforms."""

from __future__ import annotations

import json
import logging
import os
import smtplib
from email.mime.text import MIMEText
from pathlib import Path
from typing import Any

import requests

LOGGER = logging.getLogger(__name__)


def _load_env() -> dict[str, str]:
    env_path = Path(".env")
    if not env_path.exists():
        return {}
    data: dict[str, str] = {}
    for line in env_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        data[key.strip()] = value.strip()
    return data


_ENV = _load_env()


def send_telegram(message: str) -> bool:
    token = _ENV.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = _ENV.get("TELEGRAM_CHAT_ID", "")
    if not token or not chat_id:
        LOGGER.warning("Telegram not configured")
        return False
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except requests.RequestException as exc:
        LOGGER.error("Telegram send failed: %s", exc)
        return False


def send_discord(message: str) -> bool:
    webhook_url = _ENV.get("DISCORD_WEBHOOK_URL", "")
    if not webhook_url:
        LOGGER.warning("Discord not configured")
        return False
    payload = {"content": message}
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except requests.RequestException as exc:
        LOGGER.error("Discord send failed: %s", exc)
        return False


def send_slack(message: str) -> bool:
    webhook_url = _ENV.get("SLACK_WEBHOOK_URL", "")
    if not webhook_url:
        LOGGER.warning("Slack not configured")
        return False
    payload = {"text": message}
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except requests.RequestException as exc:
        LOGGER.error("Slack send failed: %s", exc)
        return False


def send_email(subject: str, body: str) -> bool:
    smtp_host = _ENV.get("SMTP_HOST", "")
    smtp_port = int(_ENV.get("SMTP_PORT", "587"))
    smtp_user = _ENV.get("SMTP_USER", "")
    smtp_password = _ENV.get("SMTP_PASSWORD", "")
    to_email = _ENV.get("ALERT_EMAIL", "")

    if not all([smtp_host, smtp_user, smtp_password, to_email]):
        LOGGER.warning("Email not configured")
        return False

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = to_email

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, [to_email], msg.as_string())
        return True
    except (smtplib.SMTPException, OSError) as exc:
        LOGGER.error("Email send failed: %s", exc)
        return False


def send_all(message: str) -> dict[str, bool]:
    results: dict[str, bool] = {
        "telegram": send_telegram(message),
        "discord": send_discord(message),
        "slack": send_slack(message),
    }
    if "SMTP_HOST" in _ENV:
        results["email"] = send_email("Codex Review Alert", message)
    return results

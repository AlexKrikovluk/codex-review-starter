#!/usr/bin/env python3
"""Telegram voice command bot for Hermes.

Uses local faster-whisper for STT.
Maps voice commands to Hermes actions.
"""

from __future__ import annotations

import argparse
import logging
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

try:
    from faster_whisper import WhisperModel
except ImportError:
    WhisperModel = None


VOICE_DIR = Path(os.environ.get("HERMES_VOICE_DIR", "/home/alexk/.hermes/cache/voice"))
VOICE_DIR.mkdir(parents=True, exist_ok=True)
SCRIPT_DIR = Path("/home/alexk/projects/codex-review-starter/scripts")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ensure_model(model_size: str = "small") -> Any:
    if WhisperModel is None:
        raise RuntimeError("faster_whisper is not installed")
    return WhisperModel(model_size, compute_type="int8")


def transcribe(audio_path: Path, model_size: str = "small") -> str:
    model = ensure_model(model_size)
    segments, _info = model.transcribe(
        str(audio_path),
        beam_size=5,
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 500},
    )
    parts = [segment.text for segment in segments]
    return " ".join(parts).strip()


def convert_to_wav(input_path: Path, output_path: Path) -> None:
    ffmpeg = os.environ.get("HERMES_FFMPEG") or "/home/alexk/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffmpeg"
    if not Path(ffmpeg).exists():
        ffmpeg = "ffmpeg"
    subprocess.run(
        [ffmpeg, "-y", "-i", str(input_path), "-ar", "16000", "-ac", "1", str(output_path)],
        check=True,
        capture_output=True,
    )


def normalize_command(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^а-яa-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def map_command(text: str) -> dict[str, Any]:
    t = normalize_command(text)
    mapping: dict[str, dict[str, Any]] = {
        "статус": {"action": "status", "label": "System status"},
        "health": {"action": "status", "label": "System status"},
        "как дела": {"action": "status", "label": "System status"},
        "что нового": {"action": "status", "label": "System status"},
        "самоулучшение": {"action": "self-improvement", "label": "Self-improvement checks"},
        "проверка": {"action": "self-improvement", "label": "Self-improvement checks"},
        "проверь": {"action": "self-improvement", "label": "Self-improvement checks"},
        "дайджест": {"action": "digest", "label": "News digest"},
        "новости": {"action": "digest", "label": "News digest"},
        "digest": {"action": "digest", "label": "News digest"},
        "финансы": {"action": "finance", "label": "Finance summary"},
        "деньги": {"action": "finance", "label": "Finance summary"},
        "finance": {"action": "finance", "label": "Finance summary"},
        "баланс": {"action": "finance", "label": "Finance summary"},
        "help": {"action": "help", "label": "Help"},
        "помощь": {"action": "help", "label": "Help"},
        "помощ": {"action": "help", "label": "Help"},
    }
    for key, value in mapping.items():
        if key in t:
            return value
    return {"action": "chat", "label": "Chat", "text": text}


def run_status() -> dict[str, Any]:
    try:
        out = subprocess.run(
            ["bash", "-lc", "systemctl --user status news-monitor.timer self-improvement.timer 2>&1 | tail -n 25"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        ).stdout
        return {"ok": True, "output": out}
    except (OSError, subprocess.SubprocessError) as exc:
        return {"ok": False, "output": str(exc)}


def run_self_improvement() -> dict[str, Any]:
    script = SCRIPT_DIR / "self-improvement.sh"
    try:
        out = subprocess.run(["bash", str(script)], check=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True).stdout
        return {"ok": True, "output": out}
    except (OSError, subprocess.SubprocessError) as exc:
        return {"ok": False, "output": str(exc)}


def run_digest() -> dict[str, Any]:
    script = SCRIPT_DIR / "news-monitor.sh"
    try:
        out = subprocess.run(["bash", str(script)], check=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True).stdout
        return {"ok": True, "output": out}
    except (OSError, subprocess.SubprocessError) as exc:
        return {"ok": False, "output": str(exc)}


def run_finance() -> dict[str, Any]:
    script = SCRIPT_DIR / "finance-tracker.py"
    try:
        now = datetime.now(timezone.utc)
        out = subprocess.run(
            ["python3", str(script), "health-check", str(now.year), str(now.month)],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        ).stdout
        return {"ok": True, "output": out}
    except (OSError, subprocess.SubprocessError) as exc:
        return {"ok": False, "output": str(exc)}


def execute(command: str, text: str) -> dict[str, Any]:
    if command == "status":
        return run_status()
    if command == "self-improvement":
        return run_self_improvement()
    if command == "digest":
        return run_digest()
    if command == "finance":
        return run_finance()
    if command == "help":
        return {
            "ok": True,
            "output": (
                "Голосовые команды:\n"
                "- статус / как дела\n"
                "- дайджест / новости\n"
                "- финансы / деньги\n"
                "- самоулучшение / проверка\n"
                "- помощь\n"
            ),
        }
    return {"ok": True, "output": f"Распознал: {text}"}


async def process_voice_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.voice or not update.effective_message:
        return

    voice = update.message.voice
    file = await voice.get_file()
    oga_path = VOICE_DIR / f"voice_{update.effective_message.id}.oga"
    wav_path = VOICE_DIR / f"voice_{update.effective_message.id}.wav"

    try:
        await file.download_to_drive(custom_path=str(oga_path))
        convert_to_wav(oga_path, wav_path)
        text = transcribe(wav_path)
        command = map_command(text)
        result = execute(command["action"], command.get("text", text))
        output = result.get("output", "")
        if not output:
            output = "Команда выполнена."
        await update.message.reply_text(f"Распознал: {text}\n\n{output[:4000]}")
    except Exception as exc:
        logger.exception("Voice processing failed")
        await update.message.reply_text(f"Ошибка обработки голоса: {exc}")
    finally:
        for p in [oga_path, wav_path]:
            if p.exists():
                p.unlink(missing_ok=True)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.effective_message:
        return
    await update.effective_message.reply_text(
        "Голосовой помощник активен.\n"
        "Отправь голосовое сообщение с командой:\n"
        "- статус / как дела\n"
        "- дайджест / новости\n"
        "- финансы / деньги\n"
        "- самоулучшение / проверка\n"
        "- помощь"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Telegram voice command bot")
    parser.add_argument("--token", help="Telegram bot token")
    args = parser.parse_args()

    token = args.token or os.environ.get("TELEGRAM_VOICE_BOT_TOKEN") or os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        parser.print_help(sys.stderr)
        print("Set TELEGRAM_VOICE_BOT_TOKEN or TELEGRAM_BOT_TOKEN", file=sys.stderr)
        return 1

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.VOICE, process_voice_message))
    app.run_polling()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Local voice command processor for Hermes.

Features:
- Accepts Telegram voice/audio messages
- Transcribes with local faster-whisper (no external API)
- Maps transcript to Hermes commands
- Replies with action result or text

Supported commands:
- статус / health / как дела / что нового → system status
- дайджест / новости / digest → run news monitor
- финансы / деньги / finance → show finance summary
- самоулучшение / проверка / self-improvement → run checks
- код / код ревью / review → run codex review
- помощь / помощь / help → show commands
- anything else → normal chat reply via Hermes
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from faster_whisper import WhisperModel
except ImportError:
    WhisperModel = None


VOICE_DIR = Path(os.environ.get("HERMES_VOICE_DIR", "/home/alexk/.hermes/cache/voice"))
VOICE_DIR.mkdir(parents=True, exist_ok=True)


def ensure_model(model_size: str = "small") -> WhisperModel:
    if WhisperModel is None:
        raise RuntimeError("faster_whisper is not installed")
    return WhisperModel(model_size, compute_type="int8")


def transcribe(audio_path: str | Path, model_size: str = "small") -> str:
    model = ensure_model(model_size)
    segments, _info = model.transcribe(
        str(audio_path),
        beam_size=5,
        vad_filter=True,
        vad_parameters={"min_silence_duration_ms": 500},
    )
    parts = [segment.text for segment in segments]
    text = " ".join(parts).strip()
    return text


def convert_to_wav(input_path: str | Path, output_path: str | Path) -> None:
    input_path = str(input_path)
    output_path = str(output_path)
    ffmpeg = os.environ.get("HERMES_FFMPEG") or "/home/alexk/.hermes/tools/ffmpeg-9.0.1-linux-x64/bin/ffmpeg"
    if not Path(ffmpeg).exists():
        ffmpeg = "ffmpeg"
    subprocess.run(
        [ffmpeg, "-y", "-i", input_path, "-ar", "16000", "-ac", "1", output_path],
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
    script = "/home/alexk/projects/codex-review-starter/scripts/self-improvement.sh"
    try:
        out = subprocess.run(["bash", script], check=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True).stdout
        return {"ok": True, "output": out}
    except (OSError, subprocess.SubprocessError) as exc:
        return {"ok": False, "output": str(exc)}


def run_digest() -> dict[str, Any]:
    script = "/home/alexk/projects/codex-review-starter/scripts/news-monitor.sh"
    try:
        out = subprocess.run(["bash", script], check=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True).stdout
        return {"ok": True, "output": out}
    except (OSError, subprocess.SubprocessError) as exc:
        return {"ok": False, "output": str(exc)}


def run_finance() -> dict[str, Any]:
    script = "/home/alexk/projects/codex-review-starter/scripts/finance-tracker.py"
    try:
        out = subprocess.run(
            ["python3", script, "health-check", str(datetime.now(timezone.utc).year), str(datetime.now(timezone.utc).month)],
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


def process_voice(input_path: str | Path, model_size: str = "small") -> dict[str, Any]:
    input_path = Path(input_path)
    wav = VOICE_DIR / f"{input_path.stem}.wav"
    try:
        convert_to_wav(input_path, wav)
        text = transcribe(wav, model_size=model_size)
        command = map_command(text)
        result = execute(command["action"], command.get("text", text))
        return {
            "transcript": text,
            "command": command,
            "result": result,
        }
    except (OSError, RuntimeError, ValueError) as exc:
        return {"error": str(exc)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Local voice command processor")
    parser.add_argument("audio", help="Path to voice/audio file")
    parser.add_argument("--model", default="small", help="Whisper model size: tiny, base, small, medium, large-v3")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    args = parser.parse_args()

    result = process_voice(args.audio, model_size=args.model)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result.get("transcript", ""))
        print(result.get("command", {}).get("label", ""))
        print(result.get("result", {}).get("output", ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

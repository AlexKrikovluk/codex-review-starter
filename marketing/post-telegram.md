# Codex Review Setup — автоматизация ревью для Python репо

Привет,

Я автоматизировал код-ревью для своего Python-репозитория: Codex CLI + systemd таймеры + Telegram уведомления.

**Было:**
- Ручной ревью когда вспомню
- Нестабильные CI проверки
- Нет автоматических исследований зависимостей
- Пропущенные issues
- Разрозненные скрипты и cron

**Стало:**
- Scheduled Codex ревью Пн/Ср/Чт
- Telegram alerts только по material issues
- Research pipeline запускается сам
- pytest + coverage + mypy + ruff в CI
- Централизованные скрипты с shared lib
- Systemd таймеры с journal логированием

**Результаты:**
- 31 passing test, 94.69% coverage
- Чистый mypy strict
- 0 critical issues в последнем ревью
- ~1 час на установку

Шаблон open source: https://github.com/AlexKrikovluk/codex-review-starter

Также предлагаю платный setup для инди-девов — первые 3 со скидкой 20%.

#devtools #automation #python #opensource

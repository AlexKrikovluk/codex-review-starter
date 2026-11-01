# Flask Template

Flask project with automated Codex reviews.

## Structure

```
templates/flask/
├── app.py
├── pyproject.toml
├── README.md
└── tests/
    └── test_app.py
```

## Setup

```bash
python -m pip install flask pytest pytest-cov mypy ruff
pytest
```

## Included

- Flask 2.3+ setup
- pytest configuration
- GitHub Actions CI
- systemd timers for scheduled reviews

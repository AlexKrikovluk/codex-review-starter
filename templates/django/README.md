# Django Template

Django project with automated Codex reviews.

## Structure

```
templates/django/
├── manage.py
├── pyproject.toml
├── README.md
├── tests/
│   └── test_views.py
└── myapp/
    ├── __init__.py
    ├── views.py
    └── urls.py
```

## Setup

```bash
python -m pip install django pytest pytest-cov mypy ruff
python manage.py test
```

## Included

- Django 4.2+ setup
- pytest configuration
- GitHub Actions CI
- systemd timers for scheduled reviews

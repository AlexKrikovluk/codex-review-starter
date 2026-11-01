# Contributing

Thanks for your interest in contributing!

## Setup

```bash
git clone https://github.com/AlexKrikovluk/codex-review-starter.git
cd codex-review-starter
cp .env.example .env
./scripts/install.sh
```

## Scripts

- `scripts/codex_review.sh` — run Codex review on a repo
- `scripts/codex_review_skills.sh` — review Hermes skills
- `scripts/research_pipeline.sh` — research any topic
- `scripts/pipeline.sh` — combined CI pipeline
- `scripts/run_workflow.sh` — dev workflow runner

## Tests

```bash
pytest
```

## Lint

```bash
ruff check .
mypy .
```

## Commit Convention

Use Conventional Commits: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`.

## Code of Conduct

Be respectful. No harassment, no trolling.

# Expansion Pack 2 — VS Code Extension + Web Dashboard + Enhanced CI

**Release:** v1.2.0  
**Price:** Free update for existing buyers  
**New features:**
- VS Code extension for inline alerts
- Web dashboard for review history
- Enhanced GitHub Actions with matrix testing
- New templates: FastAPI, Django, Flask
- Automated changelog generation

---

## What's New

### 1. VS Code Extension

New extension package:
- Inline review alerts in editor
- One-click fix suggestions
- Status bar integration
- Workspace-specific settings

### 2. Web Dashboard

Local web UI for review history:
- View past reviews
- Filter by severity/date
- Export reports as PDF/HTML
- Dark/light theme

### 3. Enhanced CI

GitHub Actions improvements:
- Matrix testing across Python 3.10-3.14
- Parallel job execution
- Automated changelog from commits
- Dependency review action

### 4. New Templates

Additional project templates:
- FastAPI template
- Django template
- Flask template
- Each with pytest + coverage + mypy

### 5. Automated Changelog

New script `scripts/generate_changelog.sh`:
- Parses conventional commits
- Generates CHANGELOG.md
- Groups by type: feat, fix, docs, etc.

---

## Installation

```bash
# Pull latest changes
git pull origin main

# Install VS Code extension
code --install-extension extensions/codex-review-alerts/codex-review-alerts-1.0.0.vsix

# Run new install script
chmod +x scripts/install_expansion_v2.sh
./scripts/install_expansion_v2.sh
```

---

## Migration from v1.1

If you're upgrading from v1.1:

1. Backup your `.env` and `scripts/multi_repo.json`
2. Pull latest changes
3. Run `scripts/migrate_v1.1_to_v1.2.sh`
4. Restore your configs
5. Restart timers: `systemctl --user daemon-reload && systemctl --user restart codex-review@.timer`

---

## New Files

- `extensions/codex-review-alerts/` — VS Code extension
- `dashboard/` — web dashboard
- `templates/django/` — Django template
- `templates/flask/` — Flask template
- `scripts/generate_changelog.sh` — automated changelog
- `.github/workflows/ci-enhanced.yml` — enhanced CI
- `docs/VSCODE_EXTENSION.md` — extension guide
- `docs/DASHBOARD.md` — dashboard guide

---

## Breaking Changes

None. v1.2 is fully backward compatible with v1.0 and v1.1.

---

## Support

This is a digital product update. Check docs and existing issues for help.

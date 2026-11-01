# VS Code Extension

This guide shows how to install and use the Codex Review Alerts VS Code extension.

## Installation

### From VSIX

```bash
code --install-extension extensions/codex-review-alerts/codex-review-alerts-1.0.0.vsix
```

### From Marketplace

Coming soon to VS Code Marketplace.

## Features

- **Inline Alerts:** See Codex review issues directly in the editor
- **Status Bar:** Quick access to run reviews
- **History Panel:** View past review results
- **Quick Fixes:** One-click suggestions for common issues

## Configuration

Add to your `.vscode/settings.json`:

```json
{
  "codexReview.enabled": true,
  "codexReview.schedule": "Mon,Wed,Fri 09:00:00",
  "codexReview.alertOn": ["critical", "high", "medium"]
}
```

## Commands

- `Codex Review: Run Review` — run review on current workspace
- `Codex Review: Show History` — open review history panel

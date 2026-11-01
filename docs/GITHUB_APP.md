# GitHub App Integration

This guide shows how to set up GitHub App integration for automated PR reviews.

## Prerequisites

- GitHub App registered in your organization
- App permissions: Issues, Pull requests, Checks
- Webhook URL configured

## Setup

1. Create a GitHub App in your org settings
2. Set webhook URL to your server
3. Install the app on your repos
4. Configure permissions:
   - Issues: Read & Write
   - Pull requests: Read & Write
   - Checks: Read & Write
5. Generate and download private key

## Configuration

Add to `.env`:

```env
GITHUB_APP_ID=12345
GITHUB_APP_INSTALLATION_ID=123456
GITHUB_APP_PRIVATE_KEY_PATH=/path/to/private-key.pem
```

## Usage

The GitHub App will automatically:
- Post Codex review as PR comment
- Create status checks
- Block merge on critical issues
- Send alerts to configured platforms

## Files

- `scripts/github_app.py` — GitHub App webhook handler
- `scripts/github_app_worker.py` — background worker for PR reviews

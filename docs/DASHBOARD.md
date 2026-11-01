# Web Dashboard

Local web UI for viewing Codex review history and metrics.

## Setup

```bash
# Option 1: Docker Compose
docker compose -f dashboard/docker-compose.yml up -d

# Option 2: Direct
cd dashboard
python -m http.server 8080
```

## Access

Open http://localhost:8080 in your browser.

## Features

- Review history table
- Severity filtering
- Export to PDF/HTML
- Dark/light theme toggle
- Real-time metrics

## Configuration

Edit `dashboard/config.json` to customize:

```json
{
  "refreshInterval": 300,
  "defaultTheme": "dark",
  "reportsPath": "../research/"
}
```

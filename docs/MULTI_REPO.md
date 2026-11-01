# Multi-Repo Setup

This guide shows how to monitor multiple repositories with Codex Review Setup.

## Configuration

Edit `scripts/multi_repo.json`:

```json
{
  "repos": [
    {
      "name": "repo1",
      "url": "https://github.com/user/repo1.git",
      "path": "/path/to/repo1",
      "schedule": "Mon,Wed,Fri 09:00:00"
    },
    {
      "name": "repo2",
      "url": "https://github.com/user/repo2.git",
      "path": "/path/to/repo2",
      "schedule": "Tue,Thu 09:00:00"
    }
  ]
}
```

## Usage

### Review all repos

```bash
./scripts/multi_repo.sh all
```

### Review specific repo

```bash
./scripts/multi_repo.sh repo1
```

### Scheduled reviews

Create a systemd timer for multi-repo reviews:

```ini
# ~/.config/systemd/user/multi-repo.timer
[Unit]
Description=Multi-repo Codex review timer

[Timer]
OnCalendar=Mon,Wed,Fri 09:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

```ini
# ~/.config/systemd/user/multi-repo.service
[Unit]
Description=Multi-repo Codex review

[Service]
Type=oneshot
WorkingDirectory=%h/projects/codex-review-starter
ExecStart=%h/projects/codex-review-starter/scripts/multi_repo.sh all
```

Enable the timer:

```bash
systemctl --user daemon-reload
systemctl --user enable --now multi-repo.timer
```

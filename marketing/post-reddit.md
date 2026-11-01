# I built automated Codex reviews for my repo — here's what changed

I kept forgetting to review my own code. Not because I didn’t care, but because manual reviews are easy to skip and hard to schedule consistently.

So I automated it.

**The setup:**
- **Codex CLI** runs scheduled reviews on my repo
- **pytest + coverage + mypy + ruff** run in CI
- **Telegram alerts** notify me only when something actually needs attention
- **systemd timers** replace fragile cron
- **Research pipeline** auto-generates topic reports

**The result:**
- Reviews happen without me remembering
- I only get pinged for material issues
- My repo now has 31 passing tests, 94% coverage, and clean mypy
- Total setup time: ~1 hour

**The template:**
I packaged the whole stack into a starter repo so other devs can do the same:
github.com/AlexKrikovluk/codex-review-starter

Includes scripts, systemd units, CI workflow, and docs.

Would you use automated reviews if they took 5 minutes to set up?

#python #automation #devtools #opensource #codequality

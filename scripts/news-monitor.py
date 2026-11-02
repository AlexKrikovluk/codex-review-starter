#!/usr/bin/env python3
"""Daily news digest collector.

Sources:
- Hacker News top stories
- Reddit: Python, opensource, selfhosted, indiehackers
- GitHub Trending Python
- Product Hunt RSS
- OpenAI/Codex blog updates

Output: markdown digest file.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET


def fetch(url: str, timeout: int = 20) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "codex-review-digest/1.0 (+https://github.com/AlexKrikovluk/codex-review-starter)"
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def fetch_text(url: str, timeout: int = 20) -> str:
    return fetch(url, timeout=timeout).decode("utf-8", errors="replace")


def fetch_json(url: str, timeout: int = 20) -> dict[str, object]:
    return json.loads(fetch_text(url, timeout=timeout))


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def hn_top(limit: int = 8) -> list[dict]:
    try:
        data = fetch_json("https://hacker-news.firebaseio.com/v0/topstories.json", timeout=20)
        ids = data[:limit]
        items: list[dict] = []
        for item_id in ids:
            try:
                item = fetch_json(f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json", timeout=15)
                if item and item.get("type") == "story":
                    items.append(
                        {
                            "title": clean(item.get("title", "")),
                            "url": item.get("url") or f"https://news.ycombinator.com/item?id={item_id}",
                            "source": "HN",
                            "score": item.get("score", 0),
                        }
                    )
            except Exception:
                continue
        return items
    except Exception:
        return []


def reddit_hot(subreddits: list[str], limit: int = 6) -> list[dict]:
    try:
        url = f"https://www.reddit.com/r/{'+'.join(subreddits)}/hot.json?limit={limit}"
        data = fetch_json(url, timeout=25)
        items: list[dict] = []
        for child in data.get("data", {}).get("children", []):
            post = child.get("data", {})
            if post.get("stickied"):
                continue
            items.append(
                {
                    "title": clean(post.get("title", "")),
                    "url": f"https://reddit.com{post.get('permalink', '')}",
                    "source": f"r/{post.get('subreddit', 'reddit')}",
                    "score": post.get("score", 0),
                }
            )
        return items[:limit]
    except Exception:
        return []


def github_trending_python(limit: int = 6) -> list[dict]:
    try:
        html = fetch_text("https://github.com/trending/python?since=daily", timeout=25)
        items: list[dict] = []
        # Very lightweight parser: repo links usually in article h2 > a
        for m in re.finditer(r'<a href="(/[^"]+)"[^>]*>\s*<span[^>]*>([^<]+)</span>', html):
            path = m.group(1)
            name = clean(m.group(2))
            if name and "/" in path:
                items.append(
                    {
                        "title": name,
                        "url": f"https://github.com{path}",
                        "source": "GitHub Trending",
                        "score": 0,
                    }
                )
            if len(items) >= limit:
                break
        return items
    except Exception:
        return []


def producthunt_rss(limit: int = 6) -> list[dict]:
    try:
        xml = fetch_text("https://www.producthunt.com/feed", timeout=25)
        root = ET.fromstring(xml)
        items: list[dict] = []
        for item in root.findall(".//item")[:limit]:
            title = clean(item.findtext("title") or "")
            link = clean(item.findtext("link") or "")
            if title:
                items.append({"title": title, "url": link or "https://www.producthunt.com", "source": "Product Hunt", "score": 0})
        return items
    except Exception:
        return []


def openai_blog(limit: int = 4) -> list[dict]:
    try:
        html = fetch_text("https://openai.com/blog", timeout=25)
        items: list[dict] = []
        for m in re.finditer(r'<a href="(/blog/[^"]+)"[^>]*>\s*<[^>]+>([^<]+)</', html):
            path = m.group(1)
            title = clean(m.group(2))
            if title and "blog" in path:
                items.append({"title": title, "url": f"https://openai.com{path}", "source": "OpenAI Blog", "score": 0})
            if len(items) >= limit:
                break
        return items
    except Exception:
        return []


def competitor_matches(text: str) -> bool:
    keywords = [
        "code review",
        "codex",
        "ai review",
        "automated review",
        "github actions",
        "python automation",
        "devtool",
        "developer tool",
    ]
    lowered = text.lower()
    return any(k in lowered for k in keywords)


def filter_items(items: list[dict], competitor: bool = False) -> list[dict]:
    if competitor:
        return [it for it in items if competitor_matches(it.get("title", ""))]
    return items


def render_section(title: str, icon: str, items: list[dict], competitor: bool = False) -> str:
    lines = [f"## {icon} {title}", ""]
    filtered = filter_items(items, competitor=competitor)
    if not filtered:
        lines.append("_No matching items today._")
        lines.append("")
        return "\n".join(lines)

    for item in filtered[:8]:
        lines.append(f"- [{item['title']}]({item['url']}) — *{item['source']}*")
    lines.append("")
    return "\n".join(lines)


def build_digest(date: str) -> str:
    hn = hn_top(8)
    reddit = reddit_hot(["Python", "opensource", "selfhosted", "indiehackers"], 6)
    trending = github_trending_python(6)
    ph = producthunt_rss(6)
    blog = openai_blog(4)

    sections = [
        render_section("Your Product & Brand", "🎯", [] + reddit + hn, competitor=True),
        render_section("Competitors & Alternatives", "🛠️", trending + ph + hn, competitor=True),
        render_section("Ecosystem", "🌐", blog + hn + trending, competitor=False),
        render_section("Indie Hackers", "💡", ph + reddit, competitor=False),
        render_section("Content Trends", "🎬", reddit + hn, competitor=False),
    ]

    # Top stories: highest-score HN + any with strong keywords
    candidates = [it for it in hn + ph + reddit if it.get("score", 0) > 50 or competitor_matches(it.get("title", ""))]
    candidates = sorted(candidates, key=lambda x: x.get("score", 0), reverse=True)[:5]

    top_lines = ["## 🔥 Top Stories", ""]
    if candidates:
        for i, it in enumerate(candidates, 1):
            top_lines.append(f"{i}. [{it['title']}]({it['url']}) — *{it['source']}*")
    else:
        top_lines.append("1. _No top stories yet._")
    top_lines.append("")

    return f"""# 📰 Daily Tech Digest

**Date:** {date}
**Sources:** Hacker News, Reddit, GitHub Trending, Product Hunt, OpenAI Blog

---

{''.join(sections)}

{''.join(top_lines)}

*Auto-generated by news-monitor.py*
"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--date", default=datetime.date.today().isoformat())
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output) or ".", exist_ok=True)
    digest = build_digest(args.date)
    with open(args.output, "w", encoding="utf-8") as f:
        f.write(digest)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
update_index.py
- Scan docs/*.md for posts.
- Extract: day (from H1 starting with "Day"), category (from brackets in H1 like "# Day1 – [Verilog]"),
  and title (from first H2 or fallback to H1 text without brackets).
- Update index.md by replacing content between <!-- posts:start --> and <!-- posts:end -->.
"""
from __future__ import annotations
import re, os, sys, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent if (pathlib.Path(__file__).resolve().parent.name == "tools") else pathlib.Path(__file__).resolve().parent
DOCS = ROOT / "docs"
INDEX = ROOT / "index.md"

def parse_post(md_path: pathlib.Path):
    text = md_path.read_text(encoding="utf-8", errors="ignore")
    # Find first H1
    m_h1 = re.search(r'^\s*#\s+(.*)', text, flags=re.M)
    if not m_h1:
        return None
    h1 = m_h1.group(1).strip()
    # day like "Day1" or "Day 1"
    m_day = re.search(r'\bDay\s*([0-9]+)\b', h1, flags=re.I)
    day = f"Day{m_day.group(1)}" if m_day else None
    # category in [...]
    m_cat = re.search(r'\[([^\]]+)\]', h1)
    category = m_cat.group(1).strip() if m_cat else None
    # title from first H2
    m_h2 = re.search(r'^\s*##\s+([^\n]+)', text, flags=re.M)
    title = m_h2.group(1).strip() if m_h2 else h1
    # Make a relative link
    rel = md_path.as_posix()
    return {
        "path": rel,
        "day": day or h1,
        "category": category or "General",
        "title": title,
    }

def collect_posts():
    posts = []
    if DOCS.exists():
        for p in sorted(DOCS.glob("*.md")):
            info = parse_post(p)
            if info:
                posts.append(info)
    # Sort by day number if possible, else by name
    def day_key(item):
        import re
        m = re.search(r'(\d+)', item["day"])
        return int(m.group(1)) if m else 0
    posts.sort(key=day_key, reverse=True)
    return posts

def render_posts_md(posts):
    lines = []
    for post in posts:
        lines.append(f'- **[{post["title"]}]({post["path"]})**  \n  Category: `{post["category"]}` · {post["day"]}')
    return "\n".join(lines) if lines else "_No posts yet._"

def update_index():
    posts = collect_posts()
    posts_md = render_posts_md(posts)
    # markers
    start_marker = "<!-- posts:start -->"
    end_marker = "<!-- posts:end -->"
    if not INDEX.exists():
        # Create a minimal index with markers
        INDEX.write_text(f"# Brandon's Tech Blog\n\nWelcome!\n\n## 📚 Recent Posts\n{start_marker}\n{posts_md}\n{end_marker}\n", encoding="utf-8")
        print("index.md created with posts section.")
        return
    text = INDEX.read_text(encoding="utf-8", errors="ignore")
    if start_marker in text and end_marker in text:
        new_text = re.sub(
            start_marker + r".*?" + end_marker,
            start_marker + "\n" + posts_md + "\n" + end_marker,
            text,
            flags=re.S,
        )
    else:
        # Append a Recent Posts section at the end
        new_text = text.rstrip() + f"\n\n## 📚 Recent Posts\n{start_marker}\n{posts_md}\n{end_marker}\n"
    if new_text != text:
        INDEX.write_text(new_text, encoding="utf-8")
        print("index.md updated.")
    else:
        print("index.md unchanged.")

if __name__ == "__main__":
    update_index()

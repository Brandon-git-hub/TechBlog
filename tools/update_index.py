#!/usr/bin/env python3
"""
update_index.py (front matter aware)
- Scans docs/*.md
- Reads YAML front matter (title, categories) if present:
    ---
    layout: page
    title: "Day 1"
    categories: [Verilog]
    ---
- Extracts:
    day: from title "Day 1" (-> Day1) or from first H1 "Day 1"
    category: from 'categories' (first item) or bracket in H1 "[Verilog]" or "General"
    title_for_list: from first H2 as the display title; if missing, fall back to front matter 'title' or H1
- Writes the list into index.md between <!-- posts:start --> and <!-- posts:end --> using RELATIVE links.
"""
from __future__ import annotations
import re, os, pathlib

THIS = pathlib.Path(__file__).resolve()
ROOT = THIS.parent.parent if THIS.parent.name == "tools" else THIS.parent
DOCS = ROOT / "docs"
INDEX = ROOT / "index.md"

def parse_front_matter(text: str) -> dict:
    # Only parse if file starts with ---\n
    if not text.lstrip().startswith('---'):
        return {}
    # Find first two '---' delimiters at start
    m = re.match(r'^\s*---\s*\n(.*?)\n---\s*\n', text, flags=re.S)
    if not m:
        return {}
    block = m.group(1)
    fm = {}
    # crude YAML parsing for simple key: value and key: [a, b]
    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith('#'): 
            continue
        if ':' not in line:
            continue
        k, v = line.split(':', 1)
        k = k.strip().lower()
        v = v.strip()
        # strip quotes
        if v.startswith('"') and v.endswith('"'):
            v = v[1:-1]
        elif v.startswith("'") and v.endswith("'"):
            v = v[1:-1]
        # list like [A, B]
        if v.startswith('[') and v.endswith(']'):
            inside = v[1:-1].strip()
            items = []
            if inside:
                for part in inside.split(','):
                    s = part.strip()
                    if s.startswith('"') and s.endswith('"'): s = s[1:-1]
                    if s.startswith("'") and s.endswith("'"): s = s[1:-1]
                    items.append(s)
            fm[k] = items
        else:
            fm[k] = v
    return fm

def parse_post(md_path: pathlib.Path):
    text = md_path.read_text(encoding='utf-8', errors='ignore')
    fm = parse_front_matter(text)
    content = text
    # remove front matter from content when searching H1/H2
    if fm:
        content = re.sub(r'^\s*---\s*\n(.*?)\n---\s*\n', '', text, count=1, flags=re.S)

    # First H2 as display title if available
    m_h2 = re.search(r'^\s*##\s+([^\n]+)', content, flags=re.M)
    title_for_list = m_h2.group(1).strip() if m_h2 else None

    # Front matter 'title'
    fm_title = fm.get('title') if fm else None

    # Derive 'day'
    day = None
    if fm_title:
        m_day = re.search(r'\bDay\s*([0-9]+)\b', fm_title, flags=re.I)
        if m_day:
            day = f"Day{m_day.group(1)}"
    if not day:
        # fall back to first H1
        m_h1 = re.search(r'^\s*#\s+(.*)', content, flags=re.M)
        if m_h1:
            h1 = m_h1.group(1).strip()
            m_day = re.search(r'\bDay\s*([0-9]+)\b', h1, flags=re.I)
            if m_day:
                day = f"Day{m_day.group(1)}"
    if not day:
        day = "Day?"

    # Category
    category = "General"
    if fm:
        cats = fm.get('categories') or fm.get('category') or fm.get('tags')
        if isinstance(cats, list) and cats:
            category = str(cats[0])
        elif isinstance(cats, str) and cats:
            category = cats.strip()
    if category == "General":
        # fallback to bracket in H1 like [Verilog]
        m_h1 = re.search(r'^\s*#\s+(.*)', content, flags=re.M)
        if m_h1:
            h1 = m_h1.group(1).strip()
            m_cat = re.search(r'\[([^\]]+)\]', h1)
            if m_cat:
                category = m_cat.group(1).strip()

    # Display title
    if not title_for_list:
        title_for_list = fm_title or "Untitled"

    rel = os.path.relpath(md_path, ROOT).replace('\\', '/')
    return {"path": rel, "day": day, "category": category, "title": title_for_list}

def collect_posts():
    posts = []
    if DOCS.exists():
        for p in sorted(DOCS.glob("*.md")):
            info = parse_post(p)
            if info:
                posts.append(info)
    # Sort by day number desc if possible
    def day_key(item):
        m = re.search(r'(\d+)', item.get("day",""))
        return int(m.group(1)) if m else -1
    posts.sort(key=day_key, reverse=True)
    return posts

def render_posts_md(posts):
    if not posts:
        return "_No posts yet._"
    lines = []
    for post in posts:
        lines.append(f'- **[{post["title"]}]({post["path"]})**  \n  Category: `{post["category"]}` · {post["day"]}')
    return "\n".join(lines)

def update_index():
    posts = collect_posts()
    posts_md = render_posts_md(posts)
    start_marker = "<!-- posts:start -->"
    end_marker = "<!-- posts:end -->"
    if not INDEX.exists():
        INDEX.write_text(
            f"# Brandon's Tech Blog\n\nWelcome!\n\n## 📚 Recent Posts\n{start_marker}\n{posts_md}\n{end_marker}\n",
            encoding="utf-8"
        )
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
        new_text = text.rstrip() + f"\n\n## 📚 Recent Posts\n{start_marker}\n{posts_md}\n{end_marker}\n"
    if new_text != text:
        INDEX.write_text(new_text, encoding="utf-8")
        print("index.md updated.")
    else:
        print("index.md unchanged.")

if __name__ == "__main__":
    update_index()

---
layout: page
title: "Categories"
permalink: /categories/
---

{%- assign docs_pages = site.pages | where_exp: "p", "p.path contains 'docs/'" -%}

{%- comment -%}
蒐集所有分類 → uniq → sort
{%- endcomment -%}
{%- assign all_cats = "" | split: "" -%}
{%- for p in docs_pages -%}
  {%- if p.categories -%}
    {%- for c in p.categories -%}
      {%- assign all_cats = all_cats | push: c -%}
    {%- endfor -%}
  {%- endif -%}
{%- endfor -%}
{%- assign uniq_cats = all_cats | uniq | sort -%}

# 🗂️ Categories
<ul>
{%- for c in uniq_cats -%}
  <li><a href="#{{ c | slugify }}">{{ c }}</a></li>
{%- endfor -%}
</ul>

<hr/>

{%- for c in uniq_cats -%}
### {{ c }}
<div id="{{ c | slugify }}"></div>
<ul>
  {%- for p in docs_pages -%}
    {%- if p.categories and p.categories contains c -%}
      {%- comment -%}
      抓該頁第一個二級標題（## ...）；如果沒有，退回 title/name
      {%- endcomment -%}
      {%- assign chunks = p.content | split: "## " -%}
      {%- assign first_h2_block = chunks[1] -%}
      {%- assign first_h2_line = first_h2_block | split: "\n" | first -%}
      {%- if first_h2_line -%}
        {%- assign topic = first_h2_line | strip -%}
      {%- else -%}
        {%- assign topic = p.title | default: p.name -%}
      {%- endif -%}

      <li>
        <a href="{{ p.url | relative_url }}">
          {{ p.title | default: p.name }} — {{ topic }}
        </a>
      </li>
    {%- endif -%}
  {%- endfor -%}
</ul>
{%- endfor -%}

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
      對每頁：
      1) 轉 HTML
      2) 擷取第一個 <h2> 內文
      3) 失敗就用 title/name
      {%- endcomment -%}
      {%- assign html = p.content | markdownify -%}
      {%- assign h2_blocks = html | split: '<h2' -%}
      {%- assign topic = nil -%}
      {%- if h2_blocks.size > 1 -%}
        {%- assign first_h2_tail = h2_blocks[1] -%}
        {%- assign after_gt = first_h2_tail | split: '>' | last -%}
        {%- assign h2_inner = after_gt | split: '</h2>' | first -%}
        {%- assign topic = h2_inner | strip_html | strip -%}
      {%- endif -%}
      {%- if topic == nil or topic == '' -%}
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

---
layout: page
title: "Technique Learning Note"
---

Welcome to my blog！  
I will update my technical learning notes here.
Recent Interests:
* Verilog 
* IC Design

## 📚 Recent Posts
{%- assign docs_pages = site.pages | where_exp: "p", "p.path contains 'docs/'" -%}
{%- assign sorted_docs = docs_pages | sort: "path" | reverse -%}
<ul>
{%- for p in sorted_docs limit:10 -%}
  {%- comment -%}
  1) 把內容轉成 HTML
  2) 取第一個 <h2>…</h2> 的內文作為主題
  3) 若沒有 <h2>，退回 title/name
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
      📌 {{ p.title | default: p.name }} — {{ topic }}
    </a>
    {%- if p.categories -%}
      <span> · Category: <code>{{ p.categories | join: ', ' }}</code></span>
    {%- endif -%}
  </li>
{%- endfor -%}
</ul>

<p><a href="{{ '/categories/' | relative_url }}">Browse by category →</a></p>

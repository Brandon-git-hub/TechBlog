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
  取第一個出現的二級標題（## ...）
  若沒有，退回用該頁的 title/name
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
      📌 {{ p.title | default: p.name }} — {{ topic }}
    </a>
    {%- if p.categories -%}
      <span> · Category: <code>{{ p.categories | join: ', ' }}</code></span>
    {%- endif -%}
  </li>
{%- endfor -%}
</ul>

<p><a href="{{ '/categories/' | relative_url }}">Browse by category →</a></p>

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

{%- capture posts_md -%}
{%- for p in sorted_docs limit:10 -%}
  {%- comment -%} 取第一個 <h2> 的文字當作主題（抓不到就退回 title） {%- endcomment -%}
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

- [📌 {{ p.title | default: p.name }} — {{ topic }}]({{ p.url | relative_url }}){% if p.categories %} · Category: `{{ p.categories | join: ', ' }}`{% endif %}
{%- endfor -%}
{%- endcapture -%}

{{ posts_md | markdownify }}

<p><a href="{{ '/categories/' | relative_url }}">Browse by category →</a></p>

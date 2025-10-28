---
layout: page
title: "Technique Learning Note"
---

Welcome to my blog！  
I will update my technical learning notes here.
Recent Interests:
* Verilog 
* IC Design
* Analog/Memory IC

## 📚 Recent Posts

{%- comment -%} 1) 取出 docs 目錄下、且有 day 欄位的頁面 {%- endcomment -%}
{%- assign docs_pages = site.pages | where_exp: "p", "p.path contains 'docs/'" | where_exp: "p", "p.day != nil" -%}

{%- comment -%} 2) 將每頁轉成一行 <零填充day>|<url>，其中 day = 單值或陣列的最大值 {%- endcomment -%}
{%- assign lines = '' | split: ',' -%}
{%- for p in docs_pages -%}
  {%- capture day_str -%}{{ p.day }}{%- endcapture -%}
  {%- assign day_str = day_str | replace: ' ', '' -%}
  {%- assign day_arr = day_str | split: ',' -%}
  {%- assign maxd = -999999 -%}
  {%- for d in day_arr -%}
    {%- assign n = d | plus: 0 -%}
    {%- if n > maxd -%}{%- assign maxd = n -%}{%- endif -%}
  {%- endfor -%}
  {%- comment -%} 零填充方便字典序排序（最多 6 位數） {%- endcomment -%}
  {%- assign key = maxd | prepend: '000000' | slice: -6, 6 -%}
  {%- assign line = key | append: '|' | append: p.url -%}
  {%- assign lines = lines | push: line -%}
{%- endfor -%}

{%- comment -%} 3) 依 key 排序、反轉讓最新在前 {%- endcomment -%}
{%- assign sorted_lines = lines | sort | reverse -%}

{%- comment -%} 4) 輸出清單：用 URL 回查頁面物件（即可存取 title、categories 等） {%- endcomment -%}
<ul>
{%- for line in sorted_lines limit: 10 -%}
  {%- assign parts = line | split: '|' -%}
  {%- assign url = parts[1] -%}
  {%- assign p = site.pages | where: "url", url | first -%}
  <li>
    <a href="{{ p.url | relative_url }}">{{ p.title }}</a><br/>
    <small>Category:
      <code>{% if p.categories %}{{ p.categories | join: ', ' }}{% else %}Uncategorized{% endif %}</code>
    </small>
  </li>
{%- endfor -%}
</ul>

<p><a href="{{ '/categories/' | relative_url }}">Browse by category →</a></p>

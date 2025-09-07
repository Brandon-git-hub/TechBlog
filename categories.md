---
layout: page
title: "Categories"
permalink: /categories/
---

{% assign docs_pages = site.pages | where_exp: "p", "p.path contains 'docs/'" %}

{%- comment -%}
建立一個 { category_name => [pages...] } 的 map。
Liquid 無法直接建 map，所以用技巧：先收集所有分類到一個扁平陣列，再 uniq。
{%- endcomment -%}

{% assign all_cats = "" | split: "" %}
{% for p in docs_pages %}
  {% if p.categories %}
    {% for c in p.categories %}
      {% assign all_cats = all_cats | push: c %}
    {% endfor %}
  {% endif %}
{% endfor %}
{% assign uniq_cats = all_cats | uniq | sort %}

# 🗂️ Categories
<ul>
{% for c in uniq_cats %}
  <li><a href="#{{ c | slugify }}">{{ c }}</a></li>
{% endfor %}
</ul>

<hr/>

{% for c in uniq_cats %}
### {{ c }}
<div id="{{ c | slugify }}"></div>
<ul>
  {% for p in docs_pages %}
    {% if p.categories and p.categories contains c %}
      <li>
        <a href="{{ p.url | relative_url }}">{{ p.title | default: p.name }}</a>
        {%- comment -%} 你也可以在這裡顯示 DayX，若每頁有 Day 編號可加在 title 或 front-matter {%- endcomment -%}
      </li>
    {% endif %}
  {% endfor %}
</ul>
{% endfor %}

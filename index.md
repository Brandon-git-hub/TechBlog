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

{% assign docs_pages = site.pages | where_exp: "p", "p.path contains 'docs/'" %}

{% comment %} 過濾掉沒有 day 屬性的頁面，避免 Liquid 嘗試對 nil 或空陣列排序 {% endcomment %}
{% assign day_pages = docs_pages | where_exp: "p", "p.day != nil" %}

{% comment %} 使用自定義的 Liquid 排序邏輯，取 day 陣列的第一個元素進行排序 {% endcomment %}
{% assign sorted_docs = day_pages | sort_by: "day[0]" | reverse %}

{% capture posts_md %}
{% for p in sorted_docs limit:10 %}
- 📌 [{{ p.title }}]({{ p.url | relative_url }})<br/>Category: <code>{% if p.categories %}{{ p.categories | join: ', ' }}{% else %}Uncategorized{% endif %}</code>
{% endfor %}
{% endcapture %}

{{ posts_md | markdownify }}

<p><a href="{{ '/categories/' | relative_url }}">Browse by category →</a></p>

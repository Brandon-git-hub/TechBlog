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

{% comment %} 0. 取得所有 docs 頁面 {% endcomment %}
{% assign docs_pages = site.pages | where_exp: "p", "p.path contains 'docs/'" %}

{% comment %} 1. 過濾掉沒有 'day' 屬性的頁面 (p.day != nil) {% endcomment %}
{% assign docs_pages = docs_pages | where_exp: "p", "p.day != nil" %}

{% comment %} 2. 建立一個新陣列，包含頁面本身和一個用於排序的數字鍵值 (number_day) {% endcomment %}
{% assign sortable_docs = '' | split: ',' %}
{% for p in docs_pages %}
  {% comment %} 取出 day 陣列或單一值的第一個元素，並用 | plus: 0 將其強制轉換為數字 {% endcomment %}
  {% assign first_day_value = p.day | first | plus: 0 %} 
  
  {% comment %} 將頁面和數字鍵值存入一個暫時的陣列，再將此陣列 push 到 sortable_docs 中 {% endcomment %}
  {% assign item = p | append: '' | split: ',' %}
  {% assign item = item | push: first_day_value %}
  {% assign sortable_docs = sortable_docs | push: item %}
{% endfor %}

{% comment %} 3. 對新陣列進行排序：使用第二個元素 (即 number_day) 進行數字排序 {% endcomment %}
{% assign sorted_docs = sortable_docs | sort: 1 | reverse %}

{% comment %} 4. 照常輸出，但現在我們需要從 sorted_docs 的子陣列中取出頁面物件 p[0] {% endcomment %}
{% capture posts_md %}
{% for item in sorted_docs limit:10 %}
  {% assign p = item[0] %}
- 📌 [{{ p.title }}]({{ p.url | relative_url }})<br/>Category: <code>{% if p.categories %}{{ p.categories | join: ', ' }}{% else %}Uncategorized{% endif %}</code>
{% endfor %}
{% endcapture %}

{{ posts_md | markdownify }}

<p><a href="{{ '/categories/' | relative_url }}">Browse by category →</a></p>

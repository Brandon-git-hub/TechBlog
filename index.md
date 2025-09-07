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

{% assign docs_pages = site.pages | where_exp: "p", "p.path contains 'docs/'" %}
{% assign sorted_docs = docs_pages | sort: "day" | reverse %}

{% capture posts_md %}
{% for p in sorted_docs limit:10 %}
- 📌 [{{ p.title }}]({{ p.url | relative_url }})<br/>Category: <code>{% if p.categories %}{{ p.categories | join: ', ' }}{% else %}Uncategorized{% endif %}</code>
{% endfor %}
{% endcapture %}

{{ posts_md | markdownify }}

<p><a href="{{ '/categories/' | relative_url }}">Browse by category →</a></p>

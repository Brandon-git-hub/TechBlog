---
layout: page
title: "Technique Learning Note"
---

Welcome to my blog！  
I will update my technical learning notes here.
Recent Interests:
* Embedded System
* Verilog 
* IC Design
* Design for Testing

## 📚 Recent Posts

{% capture list_md %}
{% for p in site.posts limit:10 %}
- 📌 [{{ p.title }}]({{ p.url | relative_url }})  
  <small>Category: <code>{% if p.categories %}{{ p.categories | join: ', ' }}{% else %}Uncategorized{% endif %}</code></small>
{% endfor %}
{% endcapture %}

{{ list_md | markdownify }}

[Browse by category →]({{ '/categories/' | relative_url }})

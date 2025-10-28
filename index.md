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

{% assign docs_pages = site.pages | where_exp: "p", "p.path contains 'docs/'" | where_exp: "p", "p.day != nil" %}

{% assign lines = '' | split: ',' %}
{% for p in docs_pages %}
  {% capture day_str %}{{ p.day }}{% endcapture %}
  {% assign day_str = day_str | replace: ' ', '' %}
  {% assign day_arr = day_str | split: ',' %}
  {% assign maxd = -999999 %}
  {% for d in day_arr %}
    {% assign n = d | plus: 0 %}
    {% if n > maxd %}{% assign maxd = n %}{% endif %}
  {% endfor %}
  {% assign key = maxd | prepend: '000000' | slice: -6, 6 %}
  {% capture line %}{{ key }}|{{ p.url }}{% endcapture %}
  {% assign lines = lines | push: line %}
{% endfor %}

{% assign sorted_lines = lines | sort | reverse %}

{% capture list_md %}
{% for line in sorted_lines limit:10 %}
  {% assign parts = line | split: '|' %}
  {% assign url = parts[1] %}
  {% assign p = site.pages | where: "url", url | first %}
- 📌 [{{ p.title }}]({{ p.url | relative_url }})  
  <small>Category: <code>{% if p.categories %}{{ p.categories | join: ', ' }}{% else %}Uncategorized{% endif %}</code></small>
{% endfor %}
{% endcapture %}

{{ list_md | markdownify }}

[Browse by category →]({{ '/categories/' | relative_url }})

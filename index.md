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
{% assign sorted_docs = docs_pages | sort: "path" | reverse %}
<ul>
{% for p in sorted_docs limit:10 %}
  <li>
    <a href="{{ p.url | relative_url }}">📌 {{ p.title | default: p.name }}</a>
    {%- if p.categories -%}
      <span> · Category: <code>{{ p.categories | join: ', ' }}</code></span>
    {%- endif -%}
  </li>
{% endfor %}
</ul>

<p><a href="{{ '/categories/' | relative_url }}">Browse by category →</a></p>


---
layout: page
title: "Categories"
permalink: /categories/
---

{% assign docs_pages = site.pages | where_exp: "p", "p.path contains 'docs/'" %}

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

{% capture cats_md %}
{% for c in uniq_cats %}
- [{{ c }}](#{{ c | slugify }})
{% endfor %}
{% endcapture %}

{{ cats_md | markdownify }}

---

{% for c in uniq_cats %}

### {{ c }}

{% capture list_md %}
{% for p in docs_pages %}
  {% if p.categories and p.categories contains c %}
    {% assign html = p.content | markdownify %}
    {% assign h2_blocks = html | split: '<h2' %}
    {% assign topic = nil %}
    {% if h2_blocks.size > 1 %}
      {% assign first_h2_tail = h2_blocks[1] %}
      {% assign after_gt = first_h2_tail | split: '>' | last %}
      {% assign h2_inner = after_gt | split: '</h2>' | first %}
      {% assign topic = h2_inner | strip_html | strip %}
    {% endif %}
    {% if topic == nil or topic == '' %}
      {% assign topic = p.title | default: p.name %}
    {% endif %}
- [{{ p.title | default: p.name }} — {{ topic }}]({{ p.url | relative_url }})
  {% endif %}
{% endfor %}
{% endcapture %}

{{ list_md | markdownify }}

{% endfor %}

---
layout: page
title: "Categories"
permalink: /categories/
---

{% assign posts = site.posts %}

{% assign all_cats = "" | split: "" %}
{% for p in posts %}
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
{% for p in posts %}
{% if p.categories and p.categories contains c %}
- 📌 [{{ p.title }}]({{ p.url | relative_url }})
{% endif %}
{% endfor %}
{% endcapture %}

{{ list_md | markdownify }}

{% endfor %}
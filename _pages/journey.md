---
layout: page
title: journey
permalink: /journey/
description: A timeline of my journey, including activities, talks, certifications, awards and more.
nav: true
nav_order: 3
---

{% assign items = site.data.activities | sort: "date" | reverse %}
{% assign types = items | map: "type" | uniq %}

{% if items.size == 0 %}
<p>Coming soon.</p>
{% else %}
<div class="activity-filters" role="group" aria-label="Filter by type">
  <button type="button" class="btn btn-sm active" data-filter="all">All</button>
  {% for t in types %}
  <button type="button" class="btn btn-sm" data-filter="{{ t | slugify }}">{{ t }}</button>
  {% endfor %}
</div>

<div class="timeline">
  {% assign current_year = "" %}
  {% for item in items %}
    {% assign year = item.date | date: "%Y" %}
    {% if year != current_year %}
      {% assign current_year = year %}
      <div class="timeline-year" data-year="{{ year }}"><span>{{ year }}</span></div>
    {% endif %}
    <article class="timeline-item" data-type="{{ item.type | slugify }}">
      <div class="timeline-dot"></div>
      <div class="timeline-card">
        <div class="timeline-meta">
          <time datetime="{{ item.date | date: '%Y-%m-%d' }}">{% if item.date_text %}{{ item.date_text }}{% else %}{{ item.date | date: "%-d %b %Y" }}{% endif %}</time>
          {% if item.type %}<span class="timeline-badge">{{ item.type }}</span>{% endif %}
        </div>
        <h3 class="timeline-title">{{ item.title }}</h3>
        {% if item.place %}<div class="timeline-place">{{ item.place }}</div>{% endif %}
        {% if item.description %}<p>{{ item.description | markdownify | remove: '<p>' | remove: '</p>' }}</p>{% endif %}
        {% if item.photos %}
        <div class="timeline-photos{% if item.thumbs_wide %} wide{% endif %}">
          {% for photo in item.photos %}
          {% assign thumb = photo | replace: '/activity/photos/', '/activity/thumbs/' | replace: '/activity/certs/', '/activity/thumbs/' %}
          <img src="{{ thumb | relative_url }}" data-full="{{ photo | relative_url }}" alt="{{ item.title | escape }}" loading="lazy" draggable="false">
          {% endfor %}
        </div>
        {% endif %}
        {% if item.link %}<a class="timeline-link" href="{{ item.link }}" target="_blank" rel="noopener">{{ item.link_text | default: "View" }} &rarr;</a>{% endif %}
        {% if item.links %}
        <div class="timeline-links">
          {% for l in item.links %}<a class="timeline-link" href="{{ l.url }}" target="_blank" rel="noopener">{{ l.text }} &rarr;</a>{% endfor %}
        </div>
        {% endif %}
      </div>
    </article>
  {% endfor %}
</div>

<script>
  document.querySelectorAll('.activity-filters button').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var f = btn.dataset.filter;
      document.querySelectorAll('.activity-filters button').forEach(function (b) { b.classList.toggle('active', b === btn); });
      document.querySelectorAll('.timeline-item').forEach(function (el) {
        el.style.display = (f === 'all' || el.dataset.type === f) ? '' : 'none';
      });
      document.querySelectorAll('.timeline-year').forEach(function (y) {
        var n = y.nextElementSibling, show = false;
        while (n && !n.classList.contains('timeline-year')) { if (n.style.display !== 'none') show = true; n = n.nextElementSibling; }
        y.style.display = show ? '' : 'none';
      });
    });
  });
</script>
{% endif %}

---
layout: page
title: projects
permalink: /projects/
description: Main projects I am building and contributing to.
nav: true
nav_order: 2
display_categories: [main]
horizontal: false
---

<!-- pages/projects.md -->
<div class="projects">
{%- if site.enable_project_categories and page.display_categories %}
  <!-- Display categorized projects -->
  {%- for category in page.display_categories %}
  <h2 class="category">{% if category == "main" %}Projects{% else %}{{ category }}{% endif %}</h2>
  {%- assign categorized_projects = site.projects | where: "category", category -%}
  {%- assign sorted_projects = categorized_projects | sort: "importance" %}
  <!-- Generate cards for each project -->
  {% if page.horizontal -%}
  <div class="container">
    <div class="row row-cols-2">
    {%- for project in sorted_projects -%}
      {% include projects_horizontal.html %}
    {%- endfor %}
    </div>
  </div>
  {%- else -%}
  <div class="grid">
    {%- for project in sorted_projects -%}
      {% include projects.html %}
    {%- endfor %}
  </div>
  {%- endif -%}
  {% endfor %}

{%- else -%}
<!-- Display projects without categories -->
  {%- assign sorted_projects = site.projects | sort: "importance" -%}
  <!-- Generate cards for each project -->
  {% if page.horizontal -%}
  <div class="container">
    <div class="row row-cols-2">
    {%- for project in sorted_projects -%}
      {% include projects_horizontal.html %}
    {%- endfor %}
    </div>
  </div>
  {%- else -%}
  <div class="grid">
    {%- for project in sorted_projects -%}
      {% include projects.html %}
    {%- endfor %}
  </div>
  {%- endif -%}
{%- endif -%}

<h2 class="category">{{ site.data.grants.title }}</h2>
<div class="timeline grants-timeline">
  {% assign grant_years = site.data.grants.contents | group_by_exp: "g", "g.year | split: ' ' | last" %}
  {% for group in grant_years %}
  <section class="timeline-group" data-year="{{ group.name }}">
    <button type="button" class="timeline-year" aria-expanded="false">
      <span class="year-label">{{ group.name }}</span>
      <span class="year-count">{{ group.items.size }}</span>
      <span class="year-chevron" aria-hidden="true"></span>
    </button>
    <div class="timeline-group-body">
    {% for g in group.items %}
      <article class="timeline-item">
        <div class="timeline-dot"></div>
        <div class="timeline-card">
          <div class="timeline-meta"><time>{{ g.year }}</time></div>
          <h3 class="timeline-title">{{ g.title }}</h3>
          <div class="timeline-place">{{ g.institution }}</div>
        </div>
      </article>
    {% endfor %}
    </div>
    {% if group.items.size > 1 %}
    <button type="button" class="timeline-more" aria-expanded="false">Show {{ group.items.size | minus: 1 }} more</button>
    {% endif %}
  </section>
  {% endfor %}
</div>
</div>

<script>
  (function () {
    var groups = Array.prototype.slice.call(document.querySelectorAll('.grants-timeline .timeline-group'));
    // Each year shows its newest grant; the rest sit under a "Show more" button.
    function layout(g) {
      var items = g.querySelectorAll('.timeline-item');
      var expanded = g.classList.contains('expanded');
      items.forEach(function (el, i) { el.style.display = (i === 0 || expanded) ? '' : 'none'; });
      var more = g.querySelector('.timeline-more');
      if (more) {
        more.textContent = expanded ? 'Show less' : 'Show ' + (items.length - 1) + ' more';
        more.setAttribute('aria-expanded', expanded ? 'true' : 'false');
      }
      g.querySelector('.timeline-year').setAttribute('aria-expanded', expanded ? 'true' : 'false');
    }
    groups.forEach(function (g) {
      function flip() { g.classList.toggle('expanded'); layout(g); window.dispatchEvent(new Event('resize')); }
      g.querySelector('.timeline-year').addEventListener('click', flip);
      var more = g.querySelector('.timeline-more');
      if (more) more.addEventListener('click', flip);
      layout(g);
    });
  })();
</script>

---
layout: page
permalink: /publications/
title: publications
description: Automatically synced from my Google Scholar profile.
nav: true
nav_order: 1
---
{%- assign sch = site.data.scholar -%}
<div class="publications scholar-pubs">

{%- if sch and sch.publications.size > 0 %}
  <h3 class="stats-heading"><i class="ai ai-google-scholar"></i> Google Scholar</h3>
  <div class="scholar-stats">
    <div><span>{{ sch.publications.size }}</span>publications</div>
    <div><span>{{ sch.stats.h_index }}</span>h-index</div>
    <div><span>{{ sch.stats.citations }}</span>citations</div>
    <div><span>{{ sch.stats.i10_index }}</span>i10-index</div>
  </div>
  {%- if sch.scopus %}
  <h3 class="stats-heading"><i class="ai ai-scopus"></i> Scopus</h3>
  <div class="scholar-stats">
    <div><span>{{ sch.scopus.documents }}</span>publications</div>
    <div><span>{{ sch.scopus.h_index }}</span>h-index</div>
    <div><span>{{ sch.scopus.citations }}</span>citations</div>
  </div>
  {%- endif %}
  <p class="scholar-meta">
    <a href="{{ sch.profile_url }}" target="_blank" rel="noopener"><i class="ai ai-google-scholar"></i> Google Scholar profile</a>
    {%- if sch.scopus %} &middot; <a href="{{ sch.scopus.profile_url }}" target="_blank" rel="noopener"><i class="ai ai-scopus"></i> Scopus profile</a>{% endif %}
    &middot; last synced {{ sch.updated }}
  </p>

  {%- if site.data.books.size > 0 %}
  <h3 class="stats-heading"><i class="fas fa-book"></i> Books</h3>
  <ol class="pub-list">
    {%- for b in site.data.books %}
    <li class="pub-item book-item">
      {%- if b.cover %}<img class="book-cover" src="{{ b.cover | relative_url }}" alt="{{ b.title | escape }}" loading="lazy">{% endif %}
      <div class="book-info">
      <span class="pub-title">{{ b.title }}</span>
      <div class="pub-authors">{{ b.authors }}{% if b.editors %}; editors: {{ b.editors }}{% endif %}</div>
      <div class="pub-venue">{{ b.publisher }} &middot; {{ b.pages }} pages &middot; {{ b.category }} &middot; ISBN {{ b.isbn }}{% if b.note %} <span class="pub-cites">{{ b.note }}</span>{% endif %}</div>
      </div>
    </li>
    {%- endfor %}
  </ol>
  {%- endif %}

  {%- assign by_year = sch.publications | group_by: "year" | sort: "name" | reverse -%}
  {%- assign this_year = site.time | date: "%Y" -%}
  <div class="timeline pubs-timeline">
  {%- for g in by_year %}
    <section class="timeline-group{% if g.name == this_year %} expanded{% endif %}" data-year="{{ g.name }}">
      <button type="button" class="timeline-year" aria-expanded="false">
        <span class="year-label">{{ g.name }}</span>
        <span class="year-count">{{ g.items.size }}</span>
        <span class="year-chevron" aria-hidden="true"></span>
      </button>
      <div class="timeline-group-body">
      {%- for p in g.items %}
        <article class="timeline-item">
          <div class="timeline-dot"></div>
          <div class="timeline-card">
            {%- if p.citations > 0 %}
            <div class="timeline-meta"><span class="timeline-badge">Cited by {{ p.citations }}</span></div>
            {%- endif %}
            <h3 class="timeline-title"><a href="{{ p.url }}" target="_blank" rel="noopener">{{ p.title }}</a></h3>
            <div class="timeline-place">{{ p.authors }}</div>
            {%- if p.venue != "" %}<p>{{ p.venue }}</p>{% endif %}
          </div>
        </article>
      {%- endfor %}
      </div>
      {%- if g.items.size > 1 %}
      <button type="button" class="timeline-more" aria-expanded="false">Show {{ g.items.size | minus: 1 }} more</button>
      {%- endif %}
    </section>
  {%- endfor %}
  </div>
  <script>
    (function () {
      var groups = Array.prototype.slice.call(document.querySelectorAll('.pubs-timeline .timeline-group'));
      // Each year shows its newest publication; the rest sit under a "Show more" button.
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
{%- else %}
  {%- assign years = "2026,2025,2024,2023,2022,2021,2020,2019,2018,2017,2016" | split: "," -%}
  {%- for y in years %}
  <h2 class="year">{{y}}</h2>
  {% bibliography -f {{ site.scholar.bibliography }} -q @*[year={{y}}]* %}
  {% endfor %}
{%- endif %}

</div>

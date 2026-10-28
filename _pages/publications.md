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

  {%- assign by_year = sch.publications | group_by: "year" | sort: "name" | reverse -%}
  {%- for g in by_year %}
  <h2 class="year">{{ g.name }}</h2>
  <ol class="pub-list">
    {%- for p in g.items %}
    <li class="pub-item">
      <a class="pub-title" href="{{ p.url }}" target="_blank" rel="noopener">{{ p.title }}</a>
      <div class="pub-authors">{{ p.authors }}</div>
      <div class="pub-venue">{{ p.venue }}{% if p.citations > 0 %} <span class="pub-cites">Cited by {{ p.citations }}</span>{% endif %}</div>
    </li>
    {%- endfor %}
  </ol>
  {%- endfor %}
{%- else %}
  {%- assign years = "2026,2025,2024,2023,2022,2021,2020,2019,2018,2017,2016" | split: "," -%}
  {%- for y in years %}
  <h2 class="year">{{y}}</h2>
  {% bibliography -f {{ site.scholar.bibliography }} -q @*[year={{y}}]* %}
  {% endfor %}
{%- endif %}

</div>

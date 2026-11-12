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
  {% assign year_groups = items | group_by_exp: "i", "i.date | date: '%Y'" %}
  {% for group in year_groups %}
  {% assign year = group.name %}
  <section class="timeline-group" data-year="{{ year }}">
    <button type="button" class="timeline-year" aria-expanded="false">
      <span class="year-label">{{ year }}</span>
      <span class="year-count">{{ group.items.size }}</span>
      <span class="year-chevron" aria-hidden="true"></span>
    </button>
    <div class="timeline-group-body">
  {% for item in group.items %}
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
    {% if group.items.size > 1 %}
    <button type="button" class="timeline-more" aria-expanded="false">Show {{ group.items.size | minus: 1 }} more</button>
    {% endif %}
  </section>
  {% endfor %}
</div>

<script>
  (function () {
    var groups = Array.prototype.slice.call(document.querySelectorAll('.timeline-group'));
    var filter = 'all';

    // Each year shows its newest activity; the rest sit under a "Show more" button.
    function layout(g) {
      var matches = Array.prototype.filter.call(g.querySelectorAll('.timeline-item'), function (el) {
        return filter === 'all' || el.dataset.type === filter;
      });
      // A type filter lists every match; only "All" folds the extras under the button.
      var filtered = filter !== 'all';
      var expanded = filtered || g.classList.contains('expanded');
      g.querySelectorAll('.timeline-item').forEach(function (el) {
        var i = matches.indexOf(el);
        el.style.display = (i === 0 || (i > 0 && expanded)) ? '' : 'none';
      });
      g.style.display = matches.length ? '' : 'none';
      g.querySelector('.year-count').textContent = matches.length;
      var more = g.querySelector('.timeline-more');
      if (more) {
        var extra = matches.length - 1;
        more.style.display = (extra > 0 && !filtered) ? '' : 'none';
        more.textContent = expanded ? 'Show less' : 'Show ' + extra + ' more';
        more.setAttribute('aria-expanded', expanded ? 'true' : 'false');
      }
      g.querySelector('.timeline-year').setAttribute('aria-expanded', expanded ? 'true' : 'false');
    }
    function setExpanded(g, on) { g.classList.toggle('expanded', on); layout(g); }
    function refresh() {
      window.dispatchEvent(new Event('resize'));   // re-measure the timeline line
    }

    groups.forEach(function (g) {
      function flip() { setExpanded(g, !g.classList.contains('expanded')); refresh(); }
      g.querySelector('.timeline-year').addEventListener('click', flip);
      var more = g.querySelector('.timeline-more');
      if (more) more.addEventListener('click', flip);
    });

    document.querySelectorAll('.activity-filters button').forEach(function (btn) {
      btn.addEventListener('click', function () {
        document.querySelectorAll('.activity-filters button').forEach(function (b) { b.classList.toggle('active', b === btn); });
        filter = btn.dataset.filter;
        groups.forEach(layout);
        refresh();
      });
    });

    // A link such as /journey/#2025 opens that year fully
    var hash = location.hash.replace('#', '');
    groups.forEach(function (g) { if (g.dataset.year === hash) g.classList.add('expanded'); });
    groups.forEach(layout);
    refresh();
  })();
</script>
{% endif %}

/* Site animations: scroll reveal, count-up numbers, typed headline,
   timeline progress line and the interactive hero background.
   Everything is skipped for visitors who prefer reduced motion. */
(function () {
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function ready(fn) {
    if (document.readyState !== 'loading') fn();
    else document.addEventListener('DOMContentLoaded', fn);
  }

  function observe(els, cb, threshold) {
    if (!('IntersectionObserver' in window)) { els.forEach(function (el) { cb(el); }); return; }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { cb(e.target); io.unobserve(e.target); }
      });
    }, { threshold: threshold || 0.12 });
    els.forEach(function (el) { io.observe(el); });
  }

  // 4. Scroll reveal
  function reveal() {
    if (reduce) return;
    var sel = '.post article h2, .pub-item, .timeline-item, .feature, .flow-step, ' +
              '.research-card, .projects .grid-item, .cv .card, .scholar-stats > div';
    var els = Array.prototype.slice.call(document.querySelectorAll(sel));
    els.forEach(function (el, i) {
      el.classList.add('reveal');
      el.style.transitionDelay = ((i % 6) * 60) + 'ms';
    });
    observe(els, function (el) { el.classList.add('in'); });
  }

  // 6. Animated numbers
  function countUp() {
    if (reduce) return;
    var els = Array.prototype.slice.call(document.querySelectorAll('.scholar-stats span'));
    els.forEach(function (el) {
      var target = parseInt(el.textContent, 10);
      if (isNaN(target)) return;
      el.textContent = '0';
      observe([el], function () {
        var start = null, dur = 1000;
        function step(t) {
          if (start === null) start = t;
          var p = Math.min((t - start) / dur, 1);
          el.textContent = Math.round(target * (1 - Math.pow(1 - p, 3)));
          if (p < 1) requestAnimationFrame(step);
        }
        requestAnimationFrame(step);
      }, 0.4);
    });
  }

  // 5. Typed headline
  function typed() {
    var line = document.querySelector('.typed-line');
    if (!line || reduce) return;
    var words;
    try { words = JSON.parse(line.getAttribute('data-words')); } catch (e) { return; }
    if (!words || words.length < 2) return;
    var out = line.querySelector('.typed-text');
    var w = 0, c = words[0].length, deleting = true;
    function tick() {
      var word = words[w];
      if (deleting) { c--; } else { c++; }
      out.textContent = word.slice(0, c);
      var delay = deleting ? 35 : 70;
      if (!deleting && c === word.length) { deleting = true; delay = 1800; }
      else if (deleting && c === 0) { deleting = false; w = (w + 1) % words.length; delay = 350; }
      setTimeout(tick, delay);
    }
    setTimeout(tick, 1800);
  }

  // 8. Timeline line follows scroll
  function timeline() {
    var tl = document.querySelector('.timeline');
    if (!tl || reduce) return;
    function update() {
      var r = tl.getBoundingClientRect();
      var p = (window.innerHeight * 0.6 - r.top) / r.height;
      tl.style.setProperty('--tl-progress', Math.max(0, Math.min(1, p)) * 100 + '%');
    }
    update();
    window.addEventListener('scroll', update, { passive: true });
    window.addEventListener('resize', update);
  }

  // 9. Interactive hero background (desktop only)
  function hero() {
    var canvas = document.querySelector('.hero-canvas');
    if (!canvas || reduce || window.innerWidth < 768) return;
    var ctx = canvas.getContext('2d');
    var w, h, dots = [], mouse = { x: -999, y: -999 }, running = true;
    var colors = ['20,184,166', '79,107,237'];

    function size() {
      var r = canvas.getBoundingClientRect();
      var dpr = window.devicePixelRatio || 1;
      w = r.width; h = r.height;
      canvas.width = w * dpr; canvas.height = h * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Math.min(70, Math.round((w * h) / 4500));
      dots = [];
      for (var i = 0; i < n; i++) {
        dots.push({
          x: Math.random() * w, y: Math.random() * h,
          vx: (Math.random() - 0.5) * 0.35, vy: (Math.random() - 0.5) * 0.35,
          c: colors[i % 2]
        });
      }
    }

    function frame() {
      if (!running) return;
      ctx.clearRect(0, 0, w, h);
      for (var i = 0; i < dots.length; i++) {
        var a = dots[i];
        var dx = a.x - mouse.x, dy = a.y - mouse.y, d2 = dx * dx + dy * dy;
        if (d2 < 120 * 120 && d2 > 1) { var f = (1 - Math.sqrt(d2) / 120) * 0.6; a.x += dx / Math.sqrt(d2) * f; a.y += dy / Math.sqrt(d2) * f; }
        a.x += a.vx; a.y += a.vy;
        if (a.x < 0 || a.x > w) a.vx *= -1;
        if (a.y < 0 || a.y > h) a.vy *= -1;
        ctx.fillStyle = 'rgba(' + a.c + ',0.7)';
        ctx.beginPath(); ctx.arc(a.x, a.y, 2, 0, 6.283); ctx.fill();
        for (var j = i + 1; j < dots.length; j++) {
          var b = dots[j], lx = a.x - b.x, ly = a.y - b.y, d = lx * lx + ly * ly;
          if (d < 110 * 110) {
            ctx.strokeStyle = 'rgba(' + a.c + ',' + (0.28 * (1 - Math.sqrt(d) / 110)) + ')';
            ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
          }
        }
      }
      requestAnimationFrame(frame);
    }

    size();
    window.addEventListener('resize', size);
    var header = canvas.parentElement;
    header.addEventListener('mousemove', function (e) {
      var r = canvas.getBoundingClientRect();
      mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top;
    });
    header.addEventListener('mouseleave', function () { mouse.x = mouse.y = -999; });
    if ('IntersectionObserver' in window) {
      new IntersectionObserver(function (es) {
        var vis = es[0].isIntersecting;
        if (vis && !running) { running = true; requestAnimationFrame(frame); }
        running = vis;
      }).observe(canvas);
    }
    requestAnimationFrame(frame);
  }

  // Block "Save image as" and dragging for Journey photos (deters casual copying only)
  function protectImages() {
    function isProtected(el) {
      return el && el.tagName === 'IMG' &&
        (el.closest('.timeline-photos') || el.closest('.lightbox'));
    }
    document.addEventListener('contextmenu', function (e) { if (isProtected(e.target)) e.preventDefault(); });
    document.addEventListener('dragstart', function (e) { if (isProtected(e.target)) e.preventDefault(); });
  }

  // Click a Journey photo to see the whole picture at its own proportions
  function lightbox() {
    var thumbs = Array.prototype.slice.call(document.querySelectorAll('.timeline-photos img'));
    if (!thumbs.length) return;
    var box = null, group = [], idx = 0;

    function show(i) {
      idx = (i + group.length) % group.length;
      box.querySelector('img').src = group[idx].src;
      box.querySelector('img').alt = group[idx].alt;
    }
    function close() {
      if (!box) return;
      document.body.removeChild(box);
      box = null;
      document.removeEventListener('keydown', onKey);
    }
    function onKey(e) {
      if (e.key === 'Escape') close();
      else if (e.key === 'ArrowRight' && group.length > 1) show(idx + 1);
      else if (e.key === 'ArrowLeft' && group.length > 1) show(idx - 1);
    }
    thumbs.forEach(function (img) {
      img.addEventListener('click', function () {
        group = Array.prototype.slice.call(img.parentElement.querySelectorAll('img'));
        idx = group.indexOf(img);
        box = document.createElement('div');
        box.className = 'lightbox';
        box.setAttribute('role', 'dialog');
        box.innerHTML = '<img draggable="false" alt="">';
        box.addEventListener('click', close);
        document.body.appendChild(box);
        show(idx);
        document.addEventListener('keydown', onKey);
      });
    });
  }

  ready(function () { protectImages(); lightbox(); reveal(); countUp(); typed(); timeline(); hero(); });
})();

(function () {
  "use strict";
  var root = document.currentScript.getAttribute("data-root") || "";
  var doc = document.documentElement;

  /* Theme: follow the system until the reader picks one. */
  function effectiveTheme() {
    return doc.dataset.theme || (matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light");
  }
  function syncFrames() {
    document.querySelectorAll("iframe[data-sync-theme]").forEach(function (f) {
      try {
        var d = f.contentDocument && f.contentDocument.documentElement;
        if (d) d.dataset.theme = effectiveTheme();
      } catch (e) { /* cross-origin or not loaded */ }
    });
  }
  var themeBtn = document.querySelector("[data-theme-toggle]");
  if (themeBtn) themeBtn.addEventListener("click", function () {
    var next = effectiveTheme() === "dark" ? "light" : "dark";
    doc.dataset.theme = next;
    try { localStorage.setItem("theme", next); } catch (e) {}
    syncFrames();
  });
  document.querySelectorAll("iframe[data-sync-theme]").forEach(function (f) {
    f.addEventListener("load", syncFrames);
  });

  /* Mobile navigation drawer. */
  var menuBtn = document.querySelector("[data-menu]");
  var scrim = document.querySelector("[data-scrim]");
  function setMenu(open) {
    document.body.classList.toggle("menu-open", open);
    if (menuBtn) menuBtn.setAttribute("aria-expanded", open ? "true" : "false");
    if (scrim) scrim.hidden = !open;
  }
  if (menuBtn) menuBtn.addEventListener("click", function () {
    setMenu(!document.body.classList.contains("menu-open"));
  });
  if (scrim) scrim.addEventListener("click", function () { setMenu(false); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") setMenu(false); });

  /* Keep the current week visible in the sidebar. */
  var cur = document.querySelector(".side-nav a[aria-current='page']");
  if (cur && cur.scrollIntoView) cur.scrollIntoView({ block: "center" });

  /* Highlight the section being read in the table of contents. */
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll(".toc li a"));
  if (tocLinks.length && "IntersectionObserver" in window) {
    var byId = {};
    tocLinks.forEach(function (a) { byId[decodeURIComponent(a.hash.slice(1))] = a; });
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && byId[en.target.id]) {
          tocLinks.forEach(function (a) { a.classList.remove("active"); });
          byId[en.target.id].classList.add("active");
        }
      });
    }, { rootMargin: "-10% 0px -75% 0px" });
    document.querySelectorAll(".prose h2[id]").forEach(function (h) { obs.observe(h); });
  }

  /* Filter boxes on the gallery, labs and bibliography pages. */
  var filter = document.querySelector("[data-filter]");
  if (filter) {
    var count = document.querySelector("[data-filter-count]");
    var items = Array.prototype.slice.call(document.querySelectorAll("[data-filter-item]"));
    var groups = Array.prototype.slice.call(document.querySelectorAll("[data-filter-group]"));
    var texts = items.map(function (el) { return el.textContent.toLowerCase(); });
    var run = function () {
      var terms = filter.value.toLowerCase().split(/\s+/).filter(Boolean);
      var shown = 0;
      items.forEach(function (el, i) {
        var ok = terms.every(function (t) { return texts[i].indexOf(t) >= 0; });
        el.hidden = !ok;
        if (ok) shown++;
      });
      groups.forEach(function (g) {
        var groupText = (g.querySelector("h2, summary") || g).textContent.toLowerCase();
        var groupMatch = terms.length && terms.every(function (t) { return groupText.indexOf(t) >= 0; });
        if (groupMatch) g.querySelectorAll("[data-filter-item]").forEach(function (el) { el.hidden = false; });
        var any = g.querySelector("[data-filter-item]:not([hidden])");
        g.hidden = !any;
        if (g.tagName === "DETAILS") g.open = !!(terms.length && any);
      });
      if (count) count.textContent = terms.length
        ? document.querySelectorAll("[data-filter-item]:not([hidden])").length + " of " + items.length
        : items.length + " items";
    };
    filter.addEventListener("input", run);
    run();
  }

  /* Site search over a prebuilt index, loaded on first use. */
  var input = document.getElementById("q");
  var box = document.getElementById("q-results");
  if (!input || !box) return;
  var index = null, loading = null, active = -1, results = [];

  function load() {
    if (index) return Promise.resolve();
    if (loading) return loading;
    loading = new Promise(function (resolve) {
      var s = document.createElement("script");
      s.src = root + "assets/search-index.js";
      s.onload = function () { index = window.SEARCH_INDEX || []; resolve(); };
      s.onerror = function () { index = []; resolve(); };
      document.head.appendChild(s);
    });
    return loading;
  }
  var kindRank = { course: 30, lecture: 12, interactive: 10, lab: 6, assessment: 4, page: 8 };
  function search(q) {
    var terms = q.toLowerCase().split(/\s+/).filter(Boolean);
    if (!terms.length) return [];
    var out = [];
    for (var i = 0; i < index.length; i++) {
      var e = index[i], score = kindRank[e.k] || 0, ok = true, title = e.t.toLowerCase();
      for (var j = 0; j < terms.length; j++) {
        var t = terms[j];
        if (e.s.indexOf(t) < 0) { ok = false; break; }
        if (title.indexOf(t) >= 0) score += 25;
        if (e.c.toLowerCase() === t) score += 40;
      }
      if (ok) out.push([score, e]);
    }
    out.sort(function (a, b) { return b[0] - a[0]; });
    return out.slice(0, 30).map(function (x) { return x[1]; });
  }
  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; });
  }
  function render() {
    if (!input.value.trim()) { box.hidden = true; return; }
    box.hidden = false;
    if (!results.length) { box.innerHTML = '<div class="empty">No matches.</div>'; return; }
    box.innerHTML = results.map(function (e, i) {
      return '<a role="option" href="' + esc(root + e.u) + '" aria-selected="' + (i === active) + '">' +
        '<span class="k ' + e.k + '">' + e.k + "</span><span>" + esc(e.t) + "</span><small>" + esc(e.x) + "</small></a>";
    }).join("");
  }
  function update() {
    load().then(function () { results = search(input.value); active = results.length ? 0 : -1; render(); });
  }
  input.addEventListener("focus", function () { load(); if (input.value) update(); });
  input.addEventListener("input", update);
  input.addEventListener("keydown", function (e) {
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      if (!results.length) return;
      e.preventDefault();
      active = (active + (e.key === "ArrowDown" ? 1 : -1) + results.length) % results.length;
      render();
      var el = box.querySelector('[aria-selected="true"]');
      if (el) el.scrollIntoView({ block: "nearest" });
    } else if (e.key === "Enter" && active >= 0 && results[active]) {
      e.preventDefault();
      location.href = root + results[active].u;
    } else if (e.key === "Escape") {
      input.value = ""; box.hidden = true; input.blur();
    }
  });
  document.addEventListener("click", function (e) {
    if (!e.target.closest || !e.target.closest(".search")) box.hidden = true;
  });
  document.addEventListener("keydown", function (e) {
    var tag = (e.target.tagName || "").toLowerCase();
    if (e.key === "/" && tag !== "input" && tag !== "textarea" && !e.target.isContentEditable) {
      e.preventDefault();
      input.focus();
    }
  });
})();

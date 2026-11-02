/* Fret Finder: on every arrangement page,
   - the fret number beside a diagram is made huge, so a shape up the neck is never read as first position;
   - while the track plays, the dot of each note lights up and rings as that note sounds.
   It reads the page's own arrangement data and only adds classes; it changes nothing else. */
(function () {
  "use strict";

  var css = [
    ":root{--ff-ring:#E3A008;--ff-edge:#4A3000}",
    "@media (prefers-color-scheme:dark){:root{--ff-ring:#FFCB4D;--ff-edge:#FFF0C2}}",
    "svg text.ff-big{font-weight:800;fill:var(--ink,var(--cp-ink,currentColor));letter-spacing:-.03em;font-variant-numeric:lining-nums}",
    "svg text.ff-big-fr{font-weight:700;fill:var(--muted,var(--cp-muted,currentColor))}",
    "@keyframes ff-ring{0%{transform:scale(1)}30%{transform:scale(1.6)}100%{transform:scale(1.18)}}",
    "@keyframes ff-halo{0%{opacity:.7;transform:scale(1)}100%{opacity:0;transform:scale(2.6)}}",
    "svg .ff-on{fill:var(--ff-ring)!important;stroke:var(--ff-edge)!important;stroke-width:1.4px!important;transform-box:fill-box;transform-origin:center;transform:scale(1.22)}",
    "svg .ff-ring{animation:ff-ring .45s ease-out}",
    "svg .ff-halo{fill:none;stroke:var(--ff-ring);stroke-width:2;transform-box:fill-box;transform-origin:center;animation:ff-halo .6s ease-out forwards;pointer-events:none}",
    ".step.ff-now{background:var(--accent-soft,rgba(192,57,43,.12))}",
    /* the page's own play buttons light a whole chord: its dots ring with it */
    ".step.on svg circle.dot,.step.on svg circle.root,.step.on svg circle.open,.step.on svg rect.bar,svg circle.rdot.on,.cp-card.on svg circle.d,.cp-card.on svg circle.dr,.cp-card.on svg circle.dl{fill:var(--ff-ring);stroke:var(--ff-edge);stroke-width:1.4px;transform-box:fill-box;transform-origin:center;animation:ff-ring .45s ease-out}",
    "svg text.ff-tab-on{fill:var(--ff-edge)!important;font-weight:800;paint-order:stroke;stroke:var(--ff-ring);stroke-width:3px;stroke-linejoin:round}",
    "@media (prefers-reduced-motion:reduce){svg .ff-ring,svg .ff-halo,.step.on svg circle,svg circle.rdot.on{animation:none!important}}"
  ].join("\n");
  var st = document.createElement("style");
  st.textContent = css;
  document.head.appendChild(st);

  /* ---------- huge fret numbers ---------- */
  var LABELS = "svg text.fno, svg text.fn, svg text.fret-no, svg text.pos, .hold svg text";
  function num(v) { return parseFloat(v) || 0; }
  function enlarge(t) {
    if (t.getAttribute("data-ff-big")) return;
    var m = /\d+/.exec(t.textContent || "");
    var svg = t.ownerSVGElement;
    if (!m || !svg || !svg.viewBox || !svg.viewBox.baseVal) return;
    var lines = Array.prototype.slice.call(svg.querySelectorAll("line"));
    var vl = lines.filter(function (l) { return num(l.getAttribute("x1")) === num(l.getAttribute("x2")); });
    var hl = lines.filter(function (l) { return num(l.getAttribute("y1")) === num(l.getAttribute("y2")); });
    if (vl.length < 4 || hl.length < 2) return;
    t.setAttribute("data-ff-big", "1");
    var xs = vl.map(function (l) { return num(l.getAttribute("x1")); });
    var ys = hl.map(function (l) { return num(l.getAttribute("y1")); }).filter(function (v, i, a) { return a.indexOf(v) === i; }).sort(function (a, b) { return a - b; });
    var left = Math.min.apply(null, xs), right = Math.max.apply(null, xs), top = ys[0], fh = ys[1] - ys[0];
    var n = m[0], size = fh * (n.length > 1 ? 1.4 : 2), need = size * 0.6 * n.length + 3;
    var vb = svg.viewBox.baseVal, X = vb.x, Y = vb.y, W = vb.width, H = vb.height, grow = 0;
    var onRight = num(t.getAttribute("x")) > right;
    if (onRight) {
      grow = Math.max(0, need - (X + W - (right + 4)));
      svg.setAttribute("viewBox", [X, Y, W + grow, H].join(" "));
      t.setAttribute("x", right + 4);
      t.setAttribute("text-anchor", "start");
    } else {
      grow = Math.max(0, need - (left - 4 - X));
      svg.setAttribute("viewBox", [X - grow, Y, W + grow, H].join(" "));
      t.setAttribute("x", left - 4);
      t.setAttribute("text-anchor", "end");
    }
    t.setAttribute("y", top + size * 0.78);
    t.textContent = n;
    t.style.fontSize = size + "px";
    t.classList.add("ff-big");
    var fr = document.createElementNS("http://www.w3.org/2000/svg", "text");
    fr.setAttribute("x", t.getAttribute("x"));
    fr.setAttribute("y", top + size * 0.78 + size * 0.42);
    fr.setAttribute("text-anchor", t.getAttribute("text-anchor"));
    fr.setAttribute("class", "ff-big-fr");
    fr.style.fontSize = size * 0.34 + "px";
    fr.textContent = "fret";
    t.parentNode.insertBefore(fr, t.nextSibling);
    if (grow) {
      var mw = parseFloat(getComputedStyle(svg).maxWidth);
      if (mw) svg.style.maxWidth = (mw * (W + grow) / W).toFixed(1) + "px";
    }
  }
  function scan(root) { Array.prototype.forEach.call(root.querySelectorAll(LABELS), enlarge); }
  scan(document);
  new MutationObserver(function (muts) {
    muts.forEach(function (mu) {
      Array.prototype.forEach.call(mu.addedNodes, function (nd) {
        if (nd.nodeType !== 1) return;
        if (nd.matches && nd.matches(LABELS)) enlarge(nd); else if (nd.querySelectorAll) scan(nd);
      });
    });
  }).observe(document.body, { childList: true, subtree: true });

  /* ---------- ringing dots while the track plays ---------- */
  function ring(el) {
    el.classList.remove("ff-ring");
    void el.getBoundingClientRect();
    el.classList.add("ff-on", "ff-ring");
    if (el.tagName.toLowerCase() === "circle" && el.parentNode) {
      var h = document.createElementNS("http://www.w3.org/2000/svg", "circle");
      h.setAttribute("cx", el.getAttribute("cx")); h.setAttribute("cy", el.getAttribute("cy")); h.setAttribute("r", el.getAttribute("r"));
      h.setAttribute("class", "ff-halo");
      el.parentNode.appendChild(h);
      setTimeout(function () { if (h.parentNode) h.parentNode.removeChild(h); }, 650);
    }
  }
  // Follows one audio player: every event {t, e} that is sounding has its dots lit; each new one rings.
  function follow(audio, ev, targets) {
    if (!audio || !ev.length) return;
    ev.sort(function (a, b) { return a.t - b.t; });
    var live = new Map(), raf = 0, MAXLEN = 0;
    ev.forEach(function (x) { MAXLEN = Math.max(MAXLEN, x.e - x.t); });
    function lo(now) { var a = 0, b = ev.length; while (a < b) { var m = (a + b) >> 1; if (ev[m].t < now - MAXLEN) a = m + 1; else b = m; } return a; }
    function frame() {
      var now = audio.currentTime + 0.03, act = new Map();
      for (var i = lo(now); i < ev.length && ev[i].t <= now; i++) if (ev[i].e > now) act.set(i, ev[i]);
      var keep = new Set();
      act.forEach(function (_, j) { var o = live.get(j); if (o) { o.dots.forEach(function (d) { keep.add(d); }); o.steps.forEach(function (x) { keep.add(x); }); } });
      live.forEach(function (tg, i) {
        if (act.has(i)) return;
        tg.dots.forEach(function (d) { if (!keep.has(d)) d.classList.remove("ff-on", "ff-ring"); });
        tg.steps.forEach(function (x) { if (!keep.has(x)) x.classList.remove("ff-now"); });
        live.delete(i);
      });
      act.forEach(function (x, i) {
        if (live.has(i)) return;
        var tg = targets(x);
        tg.dots.forEach(ring);
        tg.steps.forEach(function (st) { st.classList.add("ff-now"); });
        live.set(i, tg);
      });
      if (!audio.paused && !audio.ended) raf = requestAnimationFrame(frame);
    }
    function clearAll() {
      live.forEach(function (tg) { tg.dots.forEach(function (d) { d.classList.remove("ff-on", "ff-ring"); }); tg.steps.forEach(function (x) { x.classList.remove("ff-now"); }); });
      live.clear();
    }
    audio.addEventListener("play", function () { cancelAnimationFrame(raf); raf = requestAnimationFrame(frame); });
    audio.addEventListener("seeked", function () { clearAll(); frame(); });
    audio.addEventListener("pause", function () { cancelAnimationFrame(raf); });
    audio.addEventListener("ended", function () { cancelAnimationFrame(raf); clearAll(); });
  }
  function when(fn) {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", function () { setTimeout(fn, 0); });
    else setTimeout(fn, 0);
  }

  /* Tab pages with a highlight that moves along the notes: the fret numbers under it light up. */
  function litTab(r) {
    var svg = r.ownerSVGElement; if (!svg) return;
    (svg.__ffLit || []).forEach(function (t) { t.classList.remove("ff-tab-on"); });
    svg.__ffLit = [];
    if (r.getAttribute("visibility") === "hidden") return;
    var x0 = num(r.getAttribute("x")), w = num(r.getAttribute("width"));
    Array.prototype.forEach.call(svg.querySelectorAll("text.fr"), function (t) {
      var x = num(t.getAttribute("x"));
      if (x > x0 && x < x0 + w) { t.classList.add("ff-tab-on"); svg.__ffLit.push(t); }
    });
  }
  var tabObs = new MutationObserver(function (muts) { muts.forEach(function (m) { litTab(m.target); }); });
  when(function () {
    Array.prototype.forEach.call(document.querySelectorAll("svg.tab rect.now"), function (r) { tabObs.observe(r, { attributes: true, attributeFilter: ["x", "visibility"] }); });
  });

  /* Pages whose bars hold chord diagrams, runs and picking patterns (const DATA with tracks of bars). */
  var D = (typeof DATA !== "undefined") ? DATA : null; // eslint-disable-line no-undef
  if (D && (D.tracks || D.full)) when(function () {
    var TRACKS = D.tracks || [Object.assign({ key: "full" }, D.full)];
    // which strings a picking pattern plays: the same reading the page uses for its tab
    function pick(m, idx) {
      if (Array.isArray(m)) return m.map(function (s) { return 6 - s; });
      return m === "b" ? [idx[0]] : m === "t" ? idx.slice(1) : m === "h" ? idx.slice(-3) : m === "a" ? idx : [];
    }
    // walks a bar's items the way the page numbers its diagrams (one number per chord, per run note, per pair)
    function walk(items, cb) {
      var t = 0, col = 0, px = null;
      items.forEach(function (it) {
        var k = it[0];
        if (k === "X") { px = it[1]; return; }
        if (k === "W") { t += +it[1] || 0; return; }
        if (k === "H") { cb(t, col++, null, 1); return; }
        if (k === "C") { px = null; cb(t, col++, null, it[3]); t += it[3]; return; }
        if (k === "K") {
          px = null;
          var c = col++, f = it[2], idx = f.map(function (x, i) { return x >= 0 ? i : -1; }).filter(function (i) { return i >= 0; });
          it[3].forEach(function (h) { if (h[1] !== "-") cb(t, c, pick(h[1], idx), h[0]); t += h[0]; });
          return;
        }
        if (k === "Y") { px = null; it[2].forEach(function (tri, j) { cb(t, col++, null, it[3][j]); t += it[3][j]; }); return; }
        if (k === "T") {
          var c2 = col++, o = it[4] || {}, n8 = Math.round(it[3] * 2), mel = [];
          (o.mel || []).forEach(function (p) { for (var q = 0; q < p[1]; q++) mel.push(p[0]); });
          for (var q = 0; q < n8; q++) {
            var th = (o.thumb || [])[q], mm = mel[q], pv = q ? mel[q - 1] : null;
            if (th) cb(t + q * 0.5, c2, [6 - th[0]], 0.5);
            if (mm && (!pv || pv[0] !== mm[0] || pv[1] !== mm[1])) {
              var held = 1; while (mel[q + held] && mel[q + held][0] === mm[0] && mel[q + held][1] === mm[1]) held++;
              cb(t + q * 0.5, c2, [6 - mm[0]], held * 0.5);
            }
          }
          t += it[3];
          return;
        }
        if (k === "R" || k === "P") {
          if (px) { cb(t, col++, null, 0.5); px = null; }
          (it[2] || []).forEach(function (d) { cb(t, col++, null, d); t += d; });
        }
      });
      return t;
    }
    // the dot (or barre) on each string of a chord diagram, found from where the strings are drawn
    function stringDots(svg) {
      if (svg.__ffDots) return svg.__ffDots;
      var xs = Array.prototype.slice.call(svg.querySelectorAll("line.str, line.s")).map(function (l) { return num(l.getAttribute("x1")); }).sort(function (a, b) { return a - b; });
      var out = [[], [], [], [], [], []];
      if (xs.length === 6) Array.prototype.forEach.call(svg.querySelectorAll("circle, rect.bar"), function (el) {
        if (el.classList.contains("ff-halo")) return;
        if (el.tagName.toLowerCase() === "rect") {
          var x0 = num(el.getAttribute("x")), x1 = x0 + num(el.getAttribute("width"));
          xs.forEach(function (x, i) { if (x >= x0 && x <= x1) out[i].push(el); });
        } else {
          var cx = num(el.getAttribute("cx"));
          xs.forEach(function (x, i) { if (Math.abs(x - cx) < 2.5) out[i].push(el); });
        }
      });
      svg.__ffDots = out;
      return out;
    }
    function targets(ev) {
      var els = Array.prototype.slice.call(document.querySelectorAll('[data-mark~="' + ev.mark + '"]'));
      var dots = els.filter(function (e) { return e.tagName.toLowerCase() === "circle"; });
      var steps = els.filter(function (e) { return e.classList && e.classList.contains("step"); });
      if (!dots.length) steps.forEach(function (stp) {
        var svg = stp.querySelector("svg"); if (!svg) return;
        var byS = stringDots(svg);
        (ev.s || [0, 1, 2, 3, 4, 5]).forEach(function (i) { (byS[i] || []).forEach(function (d) { if (dots.indexOf(d) < 0) dots.push(d); }); });
      });
      return { dots: dots, steps: steps.filter(function (x) { return !x.classList.contains("is-run"); }) };
    }
    TRACKS.forEach(function (T) {
      var K = T.key || "full", ev = [], bars = T.bars || [], last = 0.6, sw = +T.swing || 0;
      // swung tracks: the off-beat eighth falls later in the beat (sw of the way through), as it does in the audio
      var sx = function (x) { if (!(sw > 0.5 && sw < 1)) return x; var b = Math.floor(x + 1e-9), f = x - b; return f <= 0.5 ? b + f * 2 * sw : b + sw + (f - 0.5) * 2 * (1 - sw); };
      bars.forEach(function (b, i) {
        var total = walk(b.items || [], function () {});
        if (!total) return;
        var next = bars[i + 1], spb = next && next.start > b.start ? (next.start - b.start) / total : last;
        last = spb;
        walk(b.items || [], function (at, col, strings, len) {
          ev.push({ t: b.start + sx(at) * spb, e: b.start + sx(at + Math.max(len, 0.25)) * spb, mark: "fs-" + K + "-" + i + "-" + col, s: strings });
        });
      });
      follow(document.getElementById("ta-" + K), ev, targets);
    });
  });

  /* Pages with a play-through of bars split into chords (.ptb > .ptb-seg): when the page marks a bar as
     playing, each chord's dots ring on its beat. */
  when(function () {
    var bars = document.querySelectorAll("article.ptb");
    if (!bars.length) return;
    var J = null; try { J = JSON.parse((document.getElementById("data") || {}).textContent || "null"); } catch (e) { J = null; }
    var bpm = (J && !Array.isArray(J) && J.bpm) || 60, audio = document.getElementById("pt-audio") || document.querySelector("audio");
    var timers = [], lit = [];
    function off() { lit.forEach(function (d) { d.classList.remove("ff-on", "ff-ring"); }); lit = []; }
    function clear() { timers.forEach(clearTimeout); timers = []; off(); }
    function start(el) {
      clear();
      if (!audio || audio.paused) return;
      var spb = 60 / bpm / (audio.playbackRate || 1), at = 0;
      Array.prototype.forEach.call(el.querySelectorAll(".ptb-seg"), function (seg) {
        var beats = parseFloat(seg.style.flex) || 1, t = at; at += beats;
        // a grip named again ("back to X") lights the diagram it was first drawn in
        var src = seg.querySelector("svg") ? seg : (document.getElementById(seg.getAttribute("data-same") || "") || seg);
        timers.push(setTimeout(function () { off(); Array.prototype.forEach.call(src.querySelectorAll("svg circle"), function (c) { ring(c); lit.push(c); }); }, t * spb * 1000));
      });
    }
    var obs = new MutationObserver(function (muts) {
      muts.forEach(function (m) { var el = m.target; if (el.classList.contains("now") && !/\bnow\b/.test(m.oldValue || "")) start(el); });
    });
    Array.prototype.forEach.call(bars, function (b) { obs.observe(b, { attributes: true, attributeFilter: ["class"], attributeOldValue: true }); });
    if (audio) { audio.addEventListener("pause", clear); audio.addEventListener("ended", clear); }
  });

  /* Song-map pages (bars .bar[data-dur] of chords .ch[data-beats]): when the page marks a bar as playing,
     each chord's dots ring on its beat; a chord named again ("back to X") lights the diagram it was drawn in. */
  when(function () {
    var bars = document.querySelectorAll(".bar[data-dur]");
    if (!bars.length) return;
    var audio = document.getElementById("audio") || document.querySelector("audio");
    var timers = [], lit = [];
    function off() { lit.forEach(function (d) { d.classList.remove("ff-on", "ff-ring"); }); lit = []; }
    function clear() { timers.forEach(clearTimeout); timers = []; off(); }
    function start(el) {
      clear();
      if (!audio || audio.paused) return;
      var chs = el.querySelectorAll(".ch[data-beats]"), tot = 0, at = 0;
      Array.prototype.forEach.call(chs, function (c) { tot += parseFloat(c.getAttribute("data-beats")) || 0; });
      var spb = (parseFloat(el.getAttribute("data-dur")) || 2) / (tot || 1) / (audio.playbackRate || 1);
      Array.prototype.forEach.call(chs, function (c) {
        var t = at; at += parseFloat(c.getAttribute("data-beats")) || 0;
        var src = c.querySelector("svg") ? c : (document.getElementById(c.getAttribute("data-same") || "") || c);
        timers.push(setTimeout(function () { off(); Array.prototype.forEach.call(src.querySelectorAll("svg circle"), function (d) { ring(d); lit.push(d); }); }, t * spb * 1000));
      });
    }
    var obs = new MutationObserver(function (muts) {
      muts.forEach(function (m) { var el = m.target; if (el.classList.contains("now") && !/\bnow\b/.test(m.oldValue || "")) start(el); });
    });
    Array.prototype.forEach.call(bars, function (b) { obs.observe(b, { attributes: true, attributeFilter: ["class"], attributeOldValue: true }); });
    if (audio) { audio.addEventListener("pause", clear); audio.addEventListener("ended", clear); }
  });

  /* Pages with one diagram per beat and numbered notes (a JSON list of pieces, e.g. the Bach Prelude and Fugue). */
  var dataEl = document.getElementById("data"), PIECES = null;
  if (dataEl) { try { PIECES = JSON.parse(dataEl.textContent); } catch (e) { PIECES = null; } }
  if (Array.isArray(PIECES)) when(function () {
    PIECES.forEach(function (P) {
      if (!P || !P.data || !P.data.bars) return;
      var flat = [];
      P.data.bars.forEach(function (b) { (b.beats || []).forEach(function (bt, k) { flat.push({ b: b.n, k: k, bt: bt }); }); });
      var ev = [];
      flat.forEach(function (x, i) {
        var t0 = x.bt.t, nx = flat[i + 1], dur = nx ? nx.bt.t - t0 : 0.6;
        if (!(dur > 0)) return;
        var steps = x.bt.steps || [];
        steps.forEach(function (st, j) {
          var at = t0 + (st.t / 4) * dur, end = steps[j + 1] ? t0 + (steps[j + 1].t / 4) * dur : t0 + dur;
          ev.push({ t: at, e: Math.max(end, at + 0.08), el: P.id + "-bt-" + x.b + "-" + x.k, num: String(j + 1) });
        });
      });
      follow(document.getElementById(P.id + "-audio"), ev, function (x) {
        var box = document.getElementById(x.el), dots = [];
        if (box) Array.prototype.forEach.call(box.querySelectorAll("svg circle"), function (c) {
          var lab = c.nextElementSibling;
          if (lab && lab.tagName.toLowerCase() === "text" && lab.textContent.split("·").indexOf(x.num) >= 0) dots.push(c);
        });
        return { dots: dots, steps: [] };
      });
    });
  });
})();

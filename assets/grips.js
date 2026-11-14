/* Fret Finder: arrows under each chord diagram of an arrangement step through other ways to play it there.
   First the same notes in other places on the neck, the nearest to the chords around it first; then the other
   chords the page itself suggests for that bar. A tap draws the new grip in place, sounds it, and is remembered
   on this device for that spot. Pages that don't draw their diagrams this way are left as they are. */
(function () {
  "use strict";
  var OPEN = [40, 45, 50, 55, 59, 64];
  var PCN = { C: 0, "C#": 1, Db: 1, D: 2, "D#": 3, Eb: 3, E: 4, F: 5, "F#": 6, Gb: 6, G: 7, "G#": 8, Ab: 8, A: 9, "A#": 10, Bb: 10, B: 11 };
  var KEY = "ff.grip:" + location.pathname;

  var css = [
    ".ffg{display:flex;align-items:center;justify-content:center;gap:2px;margin:1px auto 0;font:600 12px/1 var(--sans,system-ui,sans-serif);color:var(--muted,#777);user-select:none}",
    ".ffg button{all:unset;cursor:pointer;width:26px;height:22px;display:grid;place-items:center;border-radius:11px;font-size:17px;line-height:1;color:var(--ink,#333)}",
    ".ffg button:hover{background:var(--accent-soft,rgba(160,40,30,.1))}",
    ".ffg button:focus-visible{outline:2px solid var(--accent,#a0281e);outline-offset:1px}",
    ".ffg .ffg-n{min-width:2.6em;text-align:center;font-variant-numeric:tabular-nums}",
    ".step.ff-alt .sn{color:var(--accent,#a0281e)}",
    ".ffg-why{display:block;max-width:12em;margin:1px auto 0;font:italic 11px/1.25 var(--serif,Georgia,serif);color:var(--muted,#777);text-align:center}"
  ].join("\n");

  function parse(svg) {
    var m = /^(.*), ([x\d ]+)$/.exec(svg.getAttribute("aria-label") || "");
    if (!m) return null;
    var s = m[2].trim(), f = (s.indexOf(" ") >= 0 ? s.split(/\s+/) : s.split("")).map(function (x) { return x === "x" ? -1 : +x; });
    return f.length === 6 && f.some(function (x) { return x >= 0; }) ? { name: m[1], f: f } : null;
  }
  var plain = function (n) { return String(n).replace(/♭/g, "b").replace(/♯/g, "#"); };
  var disp = function (n) {
    return String(n).replace(/^([A-G])b/, "$1♭").replace(/^([A-G])#/, "$1♯").replace(/\/([A-G])b/, "/$1♭").replace(/\/([A-G])#/, "/$1♯")
      .replace(/b9/g, "♭9").replace(/b13/g, "♭13").replace(/b5/g, "♭5").replace(/#5/g, "♯5").replace(/#9/g, "♯9").replace(/#11/g, "♯11");
  };
  function rootPc(name) { var m = /^([A-G](?:#|b)?)/.exec(plain(name)); return m ? PCN[m[1]] : null; }
  function degLabel(iv, name) {
    var q = plain(name).replace(/^[A-G](#|b)?/, "").replace(/\/.*/, "");
    var map = { 0: "R", 1: "♭9", 2: "9", 3: "♭3", 4: "3", 5: "11", 6: "♭5", 7: "5", 8: "♭13", 9: "13", 10: "♭7", 11: "7" };
    if (iv === 5 && /sus4/.test(q)) return "4";
    if (iv === 9 && /6/.test(q) && !/13/.test(q)) return "6";
    if (iv === 9 && /dim7/.test(q)) return "♭♭7";
    if (iv === 8 && (/aug/.test(q) || /#5/.test(q))) return "♯5";
    if (iv === 3 && /7#9/.test(q)) return "♯9";
    if (iv === 6 && /#11/.test(q)) return "♯11";
    if (iv === 6 && /m7b5|dim/.test(q)) return "♭5";
    return map[iv];
  }
  var notes = function (f) { return f.map(function (x, i) { return x >= 0 ? OPEN[i] + x : null; }); };
  var fstr = function (f) {
    var big = f.some(function (x) { return x > 9; });
    return f.map(function (x) { return x < 0 ? "x" : String(x); }).join(big ? " " : "");
  };
  var pos = function (f) { var p = f.filter(function (x) { return x > 0; }); return p.length ? Math.min.apply(null, p) : 0; };
  function ordinal(n) { var s = ["th", "st", "nd", "rd"], v = n % 100; return n + (s[(v - 20) % 10] || s[v] || s[0]); }
  var SNAME = ["low E", "A", "D", "G", "B", "high E"];
  function describe(f) {
    var p = pos(f), lo = f.findIndex(function (x) { return x >= 0; });
    var top = Math.max.apply(null, f), opens = f.some(function (x) { return x === 0; });
    if (!p) return "Open position";
    var fr = top > p ? ordinal(p) + "–" + ordinal(top) + " fret" : ordinal(p) + " fret";
    return "Bass on the " + SNAME[lo] + " string, " + fr + (opens ? ", with open strings" : "");
  }

  /* the diagram, drawn the way the arrangement pages draw theirs */
  function barreOf(f) {
    var fr = [];
    f.forEach(function (x, i) { if (x > 0) fr.push([x, i]); });
    if (fr.length < 3) return null;
    var lo = Math.min.apply(null, fr.map(function (p) { return p[0]; }));
    var at = fr.filter(function (p) { return p[0] === lo; }).map(function (p) { return p[1]; });
    if (at.length < 2) return null;
    var a = at[0], b = at[at.length - 1];
    for (var k = a; k <= b; k++) if (f[k] < lo) return null;
    if (b - a < 2) return null;
    return [lo, a, b];
  }
  function chordSVG(f, name, degs) {
    var played = f.filter(function (x) { return x > 0; });
    var minF = played.length ? Math.min.apply(null, played) : 1, maxF = played.length ? Math.max.apply(null, played) : 1;
    var start = maxF <= 5 ? 1 : minF, rows = Math.max(4, maxF - start + 1);
    var SW = 14, FH = 16, L = 12, T = 17, W = L + 5 * SW + 26, H = T + rows * FH + 17, g = "", r = rootPc(name), i, k;
    for (i = 0; i < 6; i++) g += '<line class="str" x1="' + (L + i * SW) + '" y1="' + T + '" x2="' + (L + i * SW) + '" y2="' + (T + rows * FH) + '"/>';
    for (k = 0; k <= rows; k++) {
      var y = T + k * FH;
      g += (k === 0 && start === 1) ? '<line class="nut" x1="' + (L - 1) + '" y1="' + y + '" x2="' + (L + 5 * SW + 1) + '" y2="' + y + '"/>'
        : '<line class="frt" x1="' + L + '" y1="' + y + '" x2="' + (L + 5 * SW) + '" y2="' + y + '"/>';
    }
    if (start > 1) g += '<text class="fno" x="' + (L + 5 * SW + 9) + '" y="' + (T + FH * 0.72) + '">' + start + "fr</text>";
    var bar = barreOf(f);
    if (bar) { var by = T + (bar[0] - start + 0.5) * FH; g += '<rect class="bar" x="' + (L + bar[1] * SW - 5.5) + '" y="' + (by - 5.5) + '" width="' + ((bar[2] - bar[1]) * SW + 11) + '" height="11" rx="5.5"/>'; }
    f.forEach(function (x, i) {
      var cx = L + i * SW;
      if (x < 0) { g += '<text class="mute" x="' + cx + '" y="' + (T - 6) + '">×</text>'; return; }
      var m = OPEN[i] + x, iv = r === null ? null : ((m - r) % 12 + 12) % 12;
      var lab = degs && degs[m % 12] ? degs[m % 12] : (iv === null ? "" : degLabel(iv, name));
      if (x === 0) g += '<circle class="open" cx="' + cx + '" cy="' + (T - 9) + '" r="3.6"/>';
      else {
        var onBar = bar && x === bar[0] && i >= bar[1] && i <= bar[2];
        if (!onBar || iv === 0) g += '<circle class="' + (iv === 0 ? "root" : "dot") + '" cx="' + cx + '" cy="' + (T + (x - start + 0.5) * FH) + '" r="5.4"/>';
      }
      if (lab) g += '<text class="deg" x="' + cx + '" y="' + (H - 4) + '">' + lab + "</text>";
    });
    var el = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    el.setAttribute("class", "dg"); el.setAttribute("viewBox", "0 0 " + W + " " + H); el.setAttribute("role", "img");
    el.setAttribute("aria-label", disp(name) + ", " + fstr(f));
    el.innerHTML = g;
    return el;
  }

  /* the same notes elsewhere on the neck */
  function sameChord(f0, near) {
    var n0 = notes(f0), have = n0.filter(function (m) { return m !== null; });
    var pcs = {}; have.forEach(function (m) { pcs[m % 12] = 1; });
    var npc = Object.keys(pcs).length, bass = Math.min.apply(null, have) % 12, top0 = Math.max.apply(null, have), cnt = have.length;
    var opens0 = f0.some(function (x) { return x === 0; });
    var opt = OPEN.map(function (o) {
      var a = [-1];
      for (var fr = 0; fr <= 15; fr++) if (pcs[(o + fr) % 12]) a.push(fr);
      return a;
    });
    var out = [], f = [0, 0, 0, 0, 0, 0];
    (function rec(i) {
      if (i === 6) { check(f.slice()); return; }
      for (var j = 0; j < opt[i].length; j++) { f[i] = opt[i][j]; rec(i + 1); }
    })(0);
    function check(f) {
      var ns = notes(f), on = [];
      ns.forEach(function (m, i) { if (m !== null) on.push(i); });
      if (on.length < Math.max(3, Math.min(cnt, 4) - 1) || on.length > Math.min(6, cnt + 1)) return;
      var got = {}; ns.forEach(function (m) { if (m !== null) got[m % 12] = 1; });
      if (Object.keys(got).length !== npc) return;
      var low = Math.min.apply(null, ns.filter(function (m) { return m !== null; }));
      if (low % 12 !== bass) return;
      var inner = 0;
      for (var s = on[0]; s <= on[on.length - 1]; s++) if (f[s] < 0) inner++;
      if (inner > 1) return;
      var fr = f.filter(function (x) { return x > 0; });
      var hasOpen = f.some(function (x) { return x === 0; });
      if (!fr.length) return;
      var lo = Math.min.apply(null, fr), hi = Math.max.apply(null, fr);
      if (hasOpen && !opens0 && hi > 4) return;
      if (hi - lo > (lo >= 7 ? 4 : 3)) return;
      var fingers = fr.length;
      if (fingers > 4) {
        var at = []; f.forEach(function (x, i) { if (x === lo) at.push(i); });
        var a = at[0], b = at[at.length - 1], ok = at.length >= 2;
        for (var k = a; ok && k <= b; k++) if (f[k] < lo) ok = false;
        if (!ok || fr.length - at.length + 1 > 4) return;
      }
      if (fstr(f) === fstr(f0)) return;
      var p = lo, d = near.reduce(function (s, q) { return s + q[1] * Math.abs(p - q[0]); }, 0);
      var topN = Math.max.apply(null, ns.filter(function (m) { return m !== null; }));
      var score = d - 0.35 * on.length + (topN === top0 ? -0.6 : 0) + (hasOpen ? 0.8 : 0) + (inner ? 0.4 : 0) + 0.15 * (hi - lo);
      out.push({ f: f, score: score, p: p });
    }
    out.sort(function (a, b) { return a.score - b.score; });
    var keep = [];
    out.forEach(function (o) {
      if (keep.length >= 7) return;
      // one grip per hand position and string set: a near twin of one already kept adds nothing
      if (keep.some(function (k) { return Math.abs(k.p - o.p) <= 1 && k.f.map(function (x) { return x < 0; }).join() === o.f.map(function (x) { return x < 0; }).join(); })) return;
      keep.push(o);
    });
    return keep.map(function (o) { return { name: null, f: o.f, why: describe(o.f) }; });
  }

  /* the other chords the page suggests for this bar (its compendium's chord options) */
  var CP = null;
  try { var cpEl = document.getElementById("cp-data"); if (cpEl) CP = JSON.parse(cpEl.textContent); } catch (e) { CP = null; }
  var D = (typeof DATA !== "undefined") ? DATA : null; // eslint-disable-line no-undef
  function pageOptions(step, k, nChords) {
    var out = [];
    if (!CP || !CP.opts || !D || !D.tracks) return out;
    var m = /^fs-(.+)-(\d+)-(\d+)$/.exec(step.getAttribute("data-mark") || "");
    if (!m) return out;
    var T = D.tracks.filter(function (t) { return (t.key || "full") === m[1]; })[0];
    var B = T && T.bars && T.bars[+m[2]];
    if (!B) return out;
    var row = CP.opts.filter(function (o) { return o.bar === B.label; })[0];
    if (!row) return out;
    var groups = {}, order = [];
    (row.opts || []).forEach(function (o) {
      if (!o.ch || o.ch.length !== nChords || !o.f || !o.f[k]) return;
      if ((o.rub || []).length) return;
      var g = o.grp || "";
      if (!groups[g]) { groups[g] = []; order.push(g); }
      groups[g].push({ name: plain(o.ch[k][0]), f: o.f[k], why: o.why || "" });
    });
    // a few of each kind: other colors, stand-ins, darker chords, bass moves
    for (var r = 0; out.length < 6 && r < 6; r++) order.forEach(function (g) { if (out.length < 6 && groups[g][r]) out.push(groups[g][r]); });
    return out;
  }

  /* a soft plucked strum, so the new grip can be heard at once */
  var AC = null;
  function strum(f) {
    try {
      AC = AC || new (window.AudioContext || window.webkitAudioContext)();
      if (AC.state === "suspended") AC.resume();
      var t0 = AC.currentTime + 0.02;
      notes(f).forEach(function (m, i) {
        if (m === null) return;
        var hz = 440 * Math.pow(2, (m - 69) / 12), sr = AC.sampleRate, len = Math.floor(sr * 2.2);
        var buf = AC.createBuffer(1, len, sr), d = buf.getChannelData(0), P = Math.round(sr / hz), ring = new Float32Array(P);
        for (var j = 0; j < P; j++) ring[j] = Math.random() * 2 - 1;
        var idx = 0, prev = 0;
        for (var n = 0; n < len; n++) {
          var cur = ring[idx], nx = ring[(idx + 1) % P];
          var v = 0.4985 * (cur + nx); ring[idx] = v; idx = (idx + 1) % P;
          prev = prev * 0.25 + v * 0.75; d[n] = prev;
        }
        var src = AC.createBufferSource(), g = AC.createGain();
        src.buffer = buf; g.gain.value = 0.22;
        src.connect(g); g.connect(AC.destination);
        src.start(t0 + i * 0.035);
      });
    } catch (e) { /* no sound here */ }
  }

  function load() { try { return JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch (e) { return {}; } }
  function save(o) { try { localStorage.setItem(KEY, JSON.stringify(o)); } catch (e) { /* storage unavailable */ } }

  function setup() {
    var steps = Array.prototype.slice.call(document.querySelectorAll(".step")).filter(function (s) {
      return !s.classList.contains("is-run") && s.querySelector(":scope > svg.dg") && parse(s.querySelector(":scope > svg.dg"));
    });
    if (!steps.length) return false;
    var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);
    var saved = load();
    // which chord of its bar each diagram is: the n-th chord diagram among the bar's steps
    var perBar = {};
    steps.forEach(function (s) {
      var m = /^fs-(.+)-(\d+)-(\d+)$/.exec(s.getAttribute("data-mark") || "");
      var key = m ? m[1] + "-" + m[2] : null;
      s.__ffBar = key; s.__ffK = key ? (perBar[key] = (perBar[key] || 0) + 1) - 1 : 0;
    });
    steps.forEach(function (step, si) {
      var svg0 = step.querySelector(":scope > svg.dg"), g0 = parse(svg0);
      var sn = step.querySelector(".sn"), sub = step.querySelector(".sub");
      var name0 = sn ? sn.textContent : g0.name, sub0 = sub ? sub.textContent : "";
      // the chord tone each pitch is in the page's own drawing
      var degs = {};
      Array.prototype.forEach.call(svg0.querySelectorAll("text.deg"), function (t) {
        var i = Math.round((parseFloat(t.getAttribute("x")) - 12) / 14);
        if (i >= 0 && i < 6 && g0.f[i] >= 0) degs[(OPEN[i] + g0.f[i]) % 12] = t.textContent;
      });
      var list = null, idx = 0, mark = step.getAttribute("data-mark") || String(si);
      function build() {
        if (list) return list;
        var near = [];
        var pv = steps[si - 1] && parse(steps[si - 1].querySelector(":scope > svg.dg"));
        var nx = steps[si + 1] && parse(steps[si + 1].querySelector(":scope > svg.dg"));
        if (pv) near.push([pos(pv.f), 1]);
        if (nx) near.push([pos(nx.f), 0.6]);
        near.push([pos(g0.f), 0.25]);
        var nChords = step.__ffBar ? perBar[step.__ffBar] : 1;
        list = [{ name: null, f: g0.f, why: "" }].concat(sameChord(g0.f, near), pageOptions(step, step.__ffK, nChords));
        return list;
      }
      var box = document.createElement("div");
      box.className = "ffg";
      box.innerHTML = '<button type="button" aria-label="Another way to play it, back">‹</button><span class="ffg-n"></span><button type="button" aria-label="Another way to play it">›</button>';
      var why = document.createElement("span"); why.className = "ffg-why";
      (sub || svg0).insertAdjacentElement("afterend", box);
      box.insertAdjacentElement("afterend", why);
      var num = box.querySelector(".ffg-n");
      num.textContent = "1";
      function show(i, sound) {
        build();
        idx = (i + list.length) % list.length;
        var o = list[idx], cur = step.querySelector(":scope > svg.dg");
        var el = idx === 0 ? svg0 : chordSVG(o.f, o.name || plain(g0.name), o.name ? null : degs);
        if (cur !== el) cur.replaceWith(el);
        if (sn) sn.textContent = o.name ? disp(o.name) : name0;
        if (sub) sub.textContent = idx === 0 ? sub0 : fstr(o.f);
        step.classList.toggle("ff-alt", idx > 0);
        if (idx > 0) step.setAttribute("data-ff-alt", "1"); else step.removeAttribute("data-ff-alt");
        num.textContent = (idx + 1) + "/" + list.length;
        why.textContent = idx === 0 ? "" : (o.name ? "Another chord: " + o.why : o.why);
        if (sound) strum(o.f);
      }
      box.querySelectorAll("button")[0].addEventListener("click", function (e) { e.stopPropagation(); show(idx - 1, true); remember(); });
      box.querySelectorAll("button")[1].addEventListener("click", function (e) { e.stopPropagation(); show(idx + 1, true); remember(); });
      function remember() { var o = load(); if (idx) o[mark] = fstr(list[idx].f) + "|" + (list[idx].name || ""); else delete o[mark]; save(o); }
      if (saved[mark]) {
        build();
        var want = saved[mark];
        for (var j = 1; j < list.length; j++) if (fstr(list[j].f) + "|" + (list[j].name || "") === want) { show(j, false); break; }
      } else {
        // the count shows once the list is known, without slowing the page down
        (window.requestIdleCallback || function (fn) { return setTimeout(fn, 200); })(function () { build(); num.textContent = "1/" + list.length; });
      }
    });
    return true;
  }
  // the page draws its diagrams itself, sometimes a moment after loading: wait for them
  var tries = 0;
  function go() { if (!setup() && ++tries < 20) setTimeout(go, 250); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", function () { setTimeout(go, 0); });
  else setTimeout(go, 0);
})();

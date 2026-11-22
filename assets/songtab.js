/* Fret Finder: a song read as tab, note by note (like Liebestraum and Lágrima).
   A checkbox in the arrangement's head, "Tab, note by note", swaps the bars of diagrams for the whole song in tab:
   every note on its string and fret with its length under it, a small diagram wherever the hand takes a new grip
   (its fret number large), the notes still ringing shaded, Back / Next / Play at 50, 75 or 100% on the record's own
   timing, and the grip's dots lighting as their notes sound. The choice and the place in the song are kept on this
   device. It reads the page's own bars (DATA.tracks[0]), so it works on the open page and on a locked copy alike.
   Sound: the guitar recordings in assets/guitar. */
(function () {
  "use strict";
  if (window.__ffSongTab) return; window.__ffSongTab = true;
  var esc = function (s) { return String(s == null ? "" : s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); };
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var OPEN = { 1: 64, 2: 59, 3: 55, 4: 50, 5: 45, 6: 40 }, HARM = { 12: 12, 7: 19, 19: 19, 5: 24, 24: 24, 4: 28, 9: 28, 16: 28, 3: 31 };
  var SNAME = ["", "high E", "B", "G", "D", "A", "low E"];
  function get(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }
  function put(k, v) { try { localStorage.setItem(k, v); } catch (e) { /* storage unavailable */ } }
  function disp(n) { return String(n || "").replace(/b(?=\d|$|\/|m|°|ø|\(|maj|sus|add|6|7|9)/g, "♭").replace(/#/g, "♯"); }

  function start() {
    var DATA_; try { DATA_ = DATA; } catch (e) { return; }                      // the page's own data (a top-level const)
    var T = DATA_ && DATA_.tracks && DATA_.tracks[0]; if (!T || !T.bars || !T.bars.length) return;
    var tb = document.getElementById("tb-" + T.key); if (!tb) return;
    var sec = tb.parentElement, head = sec.querySelector(".block-head"); if (!head) return;
    var player = sec.querySelector(".player-row"), pattern = sec.querySelector(".pattern");
    var audioEl = player ? player.querySelector("audio") : null;
    var path = location.pathname, KMODE = "ff.songtab:" + path, KPOS = "ff.songtabpos:" + path, KRATE = "ff.songtabrate:" + path;

    /* ---------- the song as notes: the page's items, read the way the page plays them ---------- */
    var NB = 6, bars = T.bars, EV = [], GR = [], STOPS = [];
    function pick(f, m) {
      var idx = []; for (var j = 0; j < f.length; j++) if (f[j] >= 0) idx.push(f.length - j);   // strings in the grip, low first
      if (Array.isArray(m)) return m.slice();
      return { a: idx, b: idx.slice(0, 1), t: idx.slice(1), h: idx.slice(-3) }[m] || [];
    }
    function barBeats(items) {
      var x = 0;
      items.forEach(function (it) {
        var k = it[0];
        if (k === "W") x += it[1]; else if (k === "K") x += it[3].reduce(function (a, h) { return a + h[0]; }, 0);
        else if (k === "C" || k === "T") x += it[3]; else if (k === "R" || k === "P") x += it[2].reduce(function (a, d) { return a + d; }, 0);
        else if (k === "Y") x += it[3].reduce(function (a, d) { return a + d; }, 0);
      });
      return x;
    }
    var FR = [];          // one per bar: {bar, i, tot, t0, t1}
    bars.forEach(function (b, bi) {
      var tot = barBeats(b.items) || 4, st = +b.start, nx = bi + 1 < bars.length ? +bars[bi + 1].start : st + 4.5, bt = b.bt;
      function tm(x) {
        if (bt && bt.length === Math.round(tot) + 1) { var k = Math.min(Math.floor(x), bt.length - 2); return bt[k] + (bt[k + 1] - bt[k]) * (x - k); }
        return st + (nx - st) * x / tot;
      }
      FR.push({ bar: b, i: bi, tot: tot, tm: tm, t0: tm(0), t1: tm(tot) });
      var x = 0, pend = null;
      function note(s, f, at, o) { EV.push({ bi: bi, x: at, t: tm(at), s: s, f: f, h: o && o.h || 0, k: o && o.k || "", c: o && o.c || "" }); }
      b.items.forEach(function (it) {
        var k = it[0], o = it[it.length - 1] && typeof it[it.length - 1] === "object" && !Array.isArray(it[it.length - 1]) ? it[it.length - 1] : {};
        if (k === "X") { pend = it[1]; return; }
        function bass() { if (pend) { pend.forEach(function (sf) { note(sf[0], sf[1], x, { k: "x" }); }); pend = null; } }
        if (k === "W") {
          if (o.damp) STOPS.push({ t: tm(x + (o.at || 0)) - 0.01, ss: o.damp });
          bass(); x += it[1]; return;
        }
        if (k === "K") {
          var f = it[2]; GR.push({ bi: bi, x: x, t: tm(x), f: f, c: it[1], keep: o.keep || [] }); bass();
          it[3].forEach(function (h) {
            var d = h[0], m = h[1];
            if (m === "-") { STOPS.push({ t: tm(x) - 0.01, ss: [1, 2, 3, 4, 5, 6] }); x += d; return; }
            pick(f, m).forEach(function (s) { var fr = f[f.length - s]; if (fr >= 0) note(s, fr, x, { c: it[1] }); });
            x += d;
          });
          return;
        }
        if (k === "C") {
          var g = it[2], sk = o.skip || []; GR.push({ bi: bi, x: x, t: tm(x), f: g, c: it[1], keep: [] }); bass();
          pick(g, "a").forEach(function (s) { if (sk.indexOf(s) < 0) note(s, g[g.length - s], x, { c: it[1] }); });
          x += it[3]; return;
        }
        if (k === "T") {
          var gt = it[2], ot = it[4] || {}, n8 = Math.round(it[3] * 2), mel = [];
          GR.push({ bi: bi, x: x, t: tm(x), f: gt, c: it[1], keep: [] }); bass();
          (ot.mel || []).forEach(function (q) { for (var z = 0; z < q[1]; z++) mel.push(q[0]); });
          for (var q8 = 0; q8 < n8; q8++) {
            var th = ot.thumb && ot.thumb[q8], mm = mel[q8] || mel[mel.length - 1];
            if (th) note(th[0], th[1], x + q8 / 2, { c: it[1] });
            if (mm) note(mm[0], mm[1], x + q8 / 2, { c: it[1], k: "trem" });
          }
          x += it[3]; return;
        }
        if (k === "R") { bass(); it[1].forEach(function (sf, j) { note(sf[0], sf[1], x, { k: "run" }); x += it[2][j]; }); return; }
        if (k === "P") {
          var strs = []; it[1].forEach(function (pr) { pr.forEach(function (sf) { strs.push(sf[0]); }); });
          var keep = o.keep || [6, 5, 4], ss = []; for (var s0 = 1; s0 <= NB; s0++) if (strs.indexOf(s0) < 0 && keep.indexOf(s0) < 0) ss.push(s0);
          STOPS.push({ t: tm(x) - 0.01, ss: ss }); bass();
          it[1].forEach(function (pr, j) { pr.forEach(function (sf) { note(sf[0], sf[1], x, { k: "run" }); }); x += it[2][j]; });
          return;
        }
        if (k === "Y") { bass(); it[2].forEach(function (tri, j) { [3, 2, 1].forEach(function (s, q) { if (tri[q] >= 0) note(s, tri[q], x, { c: it[1] }); }); x += it[3][j]; }); return; }
        if (k === "H") { it[1].forEach(function (sf) { EV.push({ bi: bi, x: x, t: tm(x), s: sf[0], f: 0, h: sf[1], k: "harm" }); }); return; }
        if (k === "D") { STOPS.push({ t: tm(x) - 0.01, ss: [1, 2, 3, 4, 5, 6] }); }
      });
    });
    if (!EV.length) return;
    EV.sort(function (a, b) { return a.t - b.t || b.s - a.s; });
    var END = FR[FR.length - 1].t1 + 1.5;
    EV.forEach(function (e, i) {
      e.i = i; e.m = OPEN[e.s] + (e.h ? (HARM[e.h] || e.h) : e.f);
      var end = END;
      for (var j = i + 1; j < EV.length; j++) if (EV[j].s === e.s && EV[j].t > e.t + 1e-4) { end = EV[j].t; break; }
      GR.forEach(function (g) { if (g.t > e.t + 1e-4 && g.t < end) { var fr = g.f[g.f.length - e.s]; if (fr !== e.f && g.keep.indexOf(e.s) < 0 && !(fr < 0 && e.f === 0)) end = g.t; } });
      STOPS.forEach(function (z) { if (z.t > e.t + 1e-4 && z.t < end && z.ss.indexOf(e.s) >= 0) end = z.t; });
      e.t1 = Math.max(e.t + 0.12, Math.min(end, e.t + 6));
    });

    /* steps: the notes that start together */
    var S = [];
    EV.forEach(function (e) {
      var last = S[S.length - 1];
      if (last && last.bi === e.bi && Math.abs(last.x - e.x) < 1e-3) { last.notes.push(e); return; }
      S.push({ bi: e.bi, x: e.x, t: e.t, notes: [e] });
    });
    S.forEach(function (sp, i) {
      sp.i = i; var nx = S[i + 1];
      sp.len = nx && nx.bi === sp.bi ? nx.x - sp.x : FR[sp.bi].tot - sp.x;
      sp.notes.sort(function (a, b) { return b.s - a.s; });
      sp.notes.forEach(function (n) { n.si = i; });
      /* who is who: the top of a chord (or a run on the high strings) is the tune, the low string under it the bass */
      var many = sp.notes.length > 1;
      sp.notes.forEach(function (n, q) {
        if (n.k === "harm") n.r = "t";
        else if (many) n.r = q === sp.notes.length - 1 ? "t" : (q === 0 && n.s >= 4 ? "b" : "i");
        else n.r = n.s <= 3 ? "t" : "b";
      });
    });

    /* ---------- where the hand takes a new grip ---------- */
    var DG = [], cur = null;
    function fretted(f) { var m = {}; for (var j = 0; j < f.length; j++) if (f[j] > 0) m[(f.length - j) + ":" + f[j]] = { s: f.length - j, f: f[j] }; return m; }
    GR.forEach(function (g) {
      var m = fretted(g.f), keys = Object.keys(m);
      if (!keys.length && cur) { g.dg = cur; return; }
      var sub = cur && keys.every(function (k) { return cur.dots[k]; });
      var fits = cur && !sub && g.c === cur.c && keys.every(function (k) { var v = m[k]; return !Object.keys(cur.dots).some(function (w) { var d = cur.dots[w]; return d.s === v.s && d.f !== v.f; }); }) &&
        Math.max.apply(null, keys.map(function (k) { return m[k].f; }).concat([cur.hi])) - Math.min.apply(null, keys.map(function (k) { return m[k].f; }).concat([cur.lo])) <= 3;
      if (cur && (sub || fits)) { keys.forEach(function (k) { cur.dots[k] = m[k]; cur.lo = Math.min(cur.lo, m[k].f); cur.hi = Math.max(cur.hi, m[k].f); }); g.dg = cur; return; }
      cur = { n: DG.length, c: g.c, dots: m, open: {}, lo: 99, hi: 0, bi: g.bi, x: g.x, t: g.t };
      keys.forEach(function (k) { cur.lo = Math.min(cur.lo, m[k].f); cur.hi = Math.max(cur.hi, m[k].f); });
      for (var j = 0; j < g.f.length; j++) if (g.f[j] === 0) cur.open[g.f.length - j] = 1;
      if (cur.lo === 99) { cur.lo = 1; cur.hi = 1; }
      DG.push(cur); g.dg = cur; g.isNew = true;
    });
    function gripAt(sp) { var g = null; for (var j = 0; j < GR.length; j++) { if (GR[j].t <= sp.t + 1e-4) g = GR[j]; else break; } return g; }
    S.forEach(function (sp) { var g = gripAt(sp); sp.dg = g ? g.dg : null; sp.c = g ? g.c : ""; });
    function diagram(dg) {
      var base = dg.hi <= 4 ? 1 : dg.lo, rows = Math.max(4, dg.hi - base + 1);
      var L = base > 1 ? 34 : 12, Tp = 12, SX = 11, FY = 12, W = L + 5 * SX + 8, H = Tp + rows * FY + 3;
      var X = function (s) { return L + (6 - s) * SX; }, Y = function (f) { return Tp + (f - base + 0.5) * FY; };
      var said = [], s = "";
      for (var i = 0; i < 6; i++) s += '<line class="st-gs" x1="' + (L + i * SX) + '" y1="' + Tp + '" x2="' + (L + i * SX) + '" y2="' + (Tp + rows * FY) + '"/>';
      for (var j = 0; j <= rows; j++) s += '<line class="' + (j === 0 && base === 1 ? "st-gn" : "st-gf") + '" x1="' + L + '" y1="' + (Tp + j * FY) + '" x2="' + (L + 5 * SX) + '" y2="' + (Tp + j * FY) + '"/>';
      if (base > 1) s += '<text class="st-gno" x="' + (L - 5) + '" y="' + (Tp + FY + 1) + '">' + base + "</text>";
      Object.keys(dg.open).forEach(function (st) { s += '<circle class="st-go" data-k="' + st + ':0" cx="' + X(+st) + '" cy="' + (Tp - 6.5) + '" r="3.6"/>'; said.push("open " + SNAME[+st]); });
      Object.keys(dg.dots).forEach(function (k) { var d = dg.dots[k]; s += '<circle class="st-gd" data-k="' + k + '" cx="' + X(d.s) + '" cy="' + Y(d.f) + '" r="4.7"/>'; said.push(SNAME[d.s] + " string fret " + d.f); });
      return '<svg class="st-dg" data-d="' + dg.n + '" viewBox="0 0 ' + W + " " + H + '" width="' + W + '" height="' + H + '" role="img" aria-label="' + esc((dg.c ? disp(dg.c) + ": " : "") + said.join(", ")) + '">' + s + "</svg>";
    }

    /* ---------- the tab: each bar cut where a new grip starts, and into rows of at most 12 notes ---------- */
    var CW = 26, LH = 12, TT = 9, TB = TT + 5 * LH, RY = TB + 14, H = RY + 8;
    function lineY(s) { return TT + (s - 1) * LH; }
    var FRAC = [[1 / 4, "¼"], [1 / 3, "⅓"], [1 / 2, "½"], [2 / 3, "⅔"], [3 / 4, "¾"], [1 / 6, "⅙"], [1 / 8, "⅛"], [3 / 8, "⅜"], [5 / 8, "⅝"], [7 / 8, "⅞"]];
    function dur(d) { var w = Math.floor(d + 1e-6), r = d - w; if (r < 0.02) return String(w); var fr = FRAC.find(function (x) { return Math.abs(x[0] - r) < 0.02; }); return (w ? w : "") + (fr ? fr[1] : (+r.toFixed(2)).toString().replace(/^0/, "")); }
    var CH = [];          // chunks: {bi, s0, s1, dg (new diagram or null), first}
    (function () {
      var bi = -1, c = null;
      S.forEach(function (sp, i) {
        var newDg = sp.dg && sp.notes.some(function (n) { return n.k !== "run" && n.k !== "harm"; }) && GR.some(function (g) { return g.isNew && g.dg === sp.dg && g.bi === sp.bi && Math.abs(g.x - sp.x) < 1e-3; });
        if (sp.bi !== bi || newDg || (c && i - c.s0 >= 12)) {
          if (c) c.s1 = i;
          c = { bi: sp.bi, s0: i, dg: newDg ? sp.dg : null, first: sp.bi !== bi }; CH.push(c); bi = sp.bi;
        }
      });
      if (c) c.s1 = S.length;
    })();
    function chunkSvg(ch, last) {
      var n = ch.s1 - ch.s0, W = n * CW + (last ? 8 : 2), s = "";
      for (var st = 1; st <= 6; st++) s += '<line class="st-l" x1="0" y1="' + lineY(st) + '" x2="' + W + '" y2="' + lineY(st) + '"/>';
      if (ch.first) s += '<line class="st-bl" x1="0.75" y1="' + lineY(1) + '" x2="0.75" y2="' + lineY(6) + '"/>';
      if (last) s += '<line class="st-bl" x1="' + (W - 4) + '" y1="' + lineY(1) + '" x2="' + (W - 4) + '" y2="' + lineY(6) + '"/><line class="st-bl2" x1="' + (W - 1.5) + '" y1="' + lineY(1) + '" x2="' + (W - 1.5) + '" y2="' + lineY(6) + '"/>';
      for (var i = ch.s0; i < ch.s1; i++) {
        var sp = S[i], x = (i - ch.s0 + 0.5) * CW, g = '<g class="st-c" data-i="' + i + '"><rect class="st-hit" x="' + (x - CW / 2) + '" y="0" width="' + CW + '" height="' + H + '"/>';
        sp.notes.forEach(function (nt) {
          var y = lineY(nt.s), tx = nt.h ? String(nt.h) : String(nt.f), w = tx.length * 7.6 + 5;
          if (nt.h) g += '<path class="st-k st-hm" id="st-n' + nt.i + '" d="M' + x + " " + (y - 7.5) + "L" + (x + 10) + " " + y + "L" + x + " " + (y + 7.5) + "L" + (x - 10) + " " + y + 'Z"/><text class="st-t st-h ' + nt.r + '" x="' + x + '" y="' + y + '">' + tx + "</text>";
          else g += '<rect class="st-k" id="st-n' + nt.i + '" x="' + (x - w / 2) + '" y="' + (y - 6.5) + '" width="' + w + '" height="13" rx="3"/><text class="st-t ' + nt.r + '" x="' + x + '" y="' + y + '">' + tx + "</text>";
        });
        var trem = sp.notes.some(function (nt) { return nt.k === "trem"; });
        g += '<text class="st-d" x="' + x + '" y="' + RY + '">' + (trem ? "~" : "") + dur(sp.len) + "</text>";
        s += g + "</g>";
      }
      return '<svg class="st-tab" viewBox="0 0 ' + W + " " + H + '" width="' + W + '" height="' + H + '" aria-hidden="true">' + s + "</svg>";
    }
    var SN = '<div class="st-sn" aria-hidden="true"><span>e</span><span>B</span><span>G</span><span>D</span><span>A</span><span>E</span></div>';
    var partOf = {};       // bar index -> the part's name, from the page's own part heads
    tb.querySelectorAll(".part").forEach(function (p) {
      var h3 = p.querySelector(".part-head h3"), fb = p.querySelector(".fbar");
      if (h3 && fb) { var m = /-(\d+)$/.exec(fb.id); if (m) partOf[+m[1]] = h3.textContent; }
    });
    function build() {
      var h = "", prevC = null;
      CH.forEach(function (ch, ci) {
        var b = FR[ch.bi].bar;
        if (ch.first) {
          if (ci) h += "</div>";
          if (partOf[ch.bi] !== undefined) h += '<div class="st-sec"><h3>' + esc(partOf[ch.bi]) + "</h3></div>";
          h += '<div class="st-bar">';
        }
        var c = S[ch.s0].c, lab = (ch.first ? '<b class="st-bn">' + esc(b.label) + "</b>" : "") + (c && (ch.first || c !== prevC) ? '<span class="st-ch">' + esc(disp(c)) + "</span>" : "");
        prevC = c;
        h += '<div class="st-fr" id="st-f' + ci + '">' + (ch.dg ? '<div class="st-dgw">' + diagram(ch.dg) + "</div>" : "") +
          '<div class="st-lab">' + lab + '</div><div class="st-tw">' + SN + chunkSvg(ch, ci === CH.length - 1) + "</div></div>";
      });
      return h + "</div>";
    }

    /* ---------- the page around it ---------- */
    var css = document.createElement("style");
    css.textContent = [
      ".st-sw{display:inline-flex;align-items:center;gap:8px;font-weight:600;cursor:pointer;margin-top:6px;user-select:none}",
      ".st-sw input{width:1.15em;height:1.15em;margin:0;accent-color:var(--voice,var(--accent));cursor:pointer}",
      ".st-wrap{display:grid;gap:14px}",
      ".st-ctl{position:sticky;top:0;z-index:6;display:flex;flex-wrap:wrap;align-items:center;gap:8px 10px;padding:10px 12px;background:var(--paper,var(--surface));border:1px solid var(--rule,var(--line));border-radius:10px;box-shadow:0 2px 10px rgba(0,0,0,.06)}",
      ".st-ctl button{font:inherit;font-weight:600;font-size:15px;padding:8px 14px;border-radius:8px;border:1px solid var(--rule-strong,var(--line));background:var(--sunk);color:var(--ink);cursor:pointer;min-height:40px}",
      ".st-ctl button.st-play{background:var(--voice,var(--accent));border-color:var(--voice,var(--accent));color:var(--paper,#fff);min-width:92px}",
      ".st-ctl .st-rate{display:inline-flex;border:1px solid var(--rule-strong,var(--line));border-radius:8px;overflow:hidden}",
      ".st-ctl .st-rate button{border:0;border-radius:0;background:transparent;padding:8px 10px;font-size:14px}",
      ".st-ctl .st-rate button[aria-pressed=true]{background:var(--voice-soft,var(--accent-soft));color:var(--voice,var(--accent))}",
      ".st-at{font-size:14px;color:var(--muted);flex:1 1 140px}.st-at b{color:var(--ink)}",
      ".st-key{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:13px;color:var(--muted)}.st-key b{font-family:var(--mono);font-weight:600}",
      ".st-key .t{color:var(--voice,var(--accent))}.st-key .b{color:var(--bass)}.st-key .hd{background:var(--sunk);outline:1px solid var(--rule-strong,var(--line));border-radius:3px;padding:0 4px}",
      ".st-body,.st-bar{display:flex;flex-wrap:wrap;align-items:flex-end;column-gap:0;row-gap:22px}.st-body{padding-left:16px}.st-bar{max-width:100%}",
      ".st-sec{flex:0 0 100%;display:flex;align-items:baseline;gap:12px;margin:18px 0 -6px -16px;border-top:1px solid var(--rule,var(--line));padding-top:14px}",
      ".st-sec:first-child{margin-top:0}.st-sec h3{font-family:var(--display);font-weight:400;font-size:1.45rem;margin:0}",
      ".st-fr{display:flex;flex-direction:column;align-items:flex-start;max-width:100%}",
      ".st-dgw{padding:0 0 2px 2px}",
      ".st-lab{height:20px;display:flex;align-items:baseline;gap:8px;padding-left:2px;white-space:nowrap}",
      ".st-bn{font-family:var(--mono);font-size:12px;color:var(--muted);font-weight:600}.st-ch{font-weight:700;font-size:14px}",
      ".st-tw{position:relative}.st-sn{display:none;position:absolute;left:-15px;top:" + (TT - 6) + "px;font-family:var(--mono);font-size:10px;line-height:" + LH + "px;color:var(--faint)}.st-sn span{display:block}",
      ".st-fr.st-rs .st-sn{display:block}",
      ".st-tab{display:block;overflow:visible;cursor:pointer}",
      ".st-tab .st-l{stroke:var(--rule-strong,var(--line));stroke-width:1}.st-tab .st-bl{stroke:var(--ink);stroke-width:1.5}.st-tab .st-bl2{stroke:var(--ink);stroke-width:3}",
      ".st-tab .st-hit{fill:transparent}.st-tab .st-k{fill:var(--paper,var(--surface))}",
      ".st-tab .st-t{font-family:var(--mono);font-size:13px;font-weight:600;fill:var(--ink);text-anchor:middle;dominant-baseline:central}",
      ".st-tab .st-t.t{fill:var(--voice,var(--accent));font-weight:700}.st-tab .st-t.b{fill:var(--bass)}.st-tab .st-t.st-h{font-size:10.5px}",
      ".st-tab .st-hm{stroke:var(--rule-strong,var(--line));stroke-width:1}",
      ".st-tab .st-d{font-family:var(--mono);font-size:11px;fill:var(--muted);text-anchor:middle;dominant-baseline:central}",
      ".st-tab .st-k.st-hold{fill:var(--sunk);stroke:var(--rule-strong,var(--line));stroke-width:1}",
      ".st-tab .st-c.now .st-k{fill:var(--now);stroke:var(--ink);stroke-width:1.2}.st-tab .st-c.now .st-d{fill:var(--ink);font-weight:700}",
      ".st-tab .st-c:hover .st-hit{fill:var(--sunk)}.st-tab .st-c.now .st-hit{fill:var(--now);opacity:.55}",
      ".st-dg{display:block;overflow:visible}.st-dg .st-gs,.st-dg .st-gf{stroke:var(--rule-strong,var(--line));stroke-width:1}.st-dg .st-gn{stroke:var(--ink);stroke-width:3}",
      ".st-dg .st-gno{font-family:var(--body,serif);font-weight:800;font-size:24px;fill:var(--ink);text-anchor:end;dominant-baseline:central}",
      ".st-dg .st-gd{fill:var(--ink)}.st-dg .st-go{fill:none;stroke:var(--ink);stroke-width:1.3}",
      ".st-dg circle{transform-box:fill-box;transform-origin:center}.st-dg .on{fill:var(--voice,var(--accent));transform:scale(1.4)}.st-dg .st-go.on{fill:var(--now)}",
      "@media (prefers-reduced-motion:no-preference){.st-dg circle{transition:transform .12s}}"
    ].join("\n");
    document.head.appendChild(css);

    var sw = document.createElement("label"); sw.className = "st-sw";
    sw.innerHTML = '<input type="checkbox"> Tab, note by note';
    head.appendChild(sw);
    var box = sw.querySelector("input");
    var wrap = document.createElement("div"); wrap.className = "st-wrap"; wrap.hidden = true;
    wrap.innerHTML = '<div class="st-ctl" role="group" aria-label="Step through the tab">' +
      '<button type="button" data-a="back" aria-label="Back one note" aria-keyshortcuts="ArrowLeft">&#8249; Back</button>' +
      '<button type="button" class="st-play" data-a="play">&#9654; Play</button>' +
      '<button type="button" data-a="next" aria-label="Next note" aria-keyshortcuts="ArrowRight">Next &#8250;</button>' +
      '<span class="st-rate" role="group" aria-label="Speed"><button type="button" data-r="0.5">50%</button><button type="button" data-r="0.75">75%</button><button type="button" data-r="1">100%</button></span>' +
      '<span class="st-at" aria-live="polite"></span></div>' +
      '<div class="st-key"><span><b class="t">2</b> the tune</span><span><b class="b">3</b> bass</span><span><b>0</b> the other notes</span>' +
      '<span><b>½</b> how long, in beats</span><span><b class="hd">1</b> still ringing: keep it held</span></div>' +
      '<div class="st-body"></div>';
    tb.parentNode.insertBefore(wrap, tb.nextSibling);
    var body = wrap.querySelector(".st-body"), at = wrap.querySelector(".st-at"), playB = wrap.querySelector(".st-play"), headP = head.querySelector("p"), headH = head.querySelector("h2");
    var headTxt = headP ? headP.textContent : "", headHTxt = headH ? headH.textContent : "";
    var built = false, colEls = [], frEls = [], dgEls = [];
    function rows() {
      var last = null;
      frEls.forEach(function (e) { var y = e.offsetTop + e.offsetHeight; e.classList.toggle("st-rs", last === null || Math.abs(y - last) > 4); last = y; });
    }
    function ensure() {
      if (built) return; built = true;
      body.innerHTML = build();
      colEls = new Array(S.length); body.querySelectorAll(".st-c").forEach(function (g) { colEls[+g.getAttribute("data-i")] = g; });
      frEls = Array.prototype.slice.call(body.querySelectorAll(".st-fr"));
      dgEls = []; body.querySelectorAll(".st-dg").forEach(function (e) { dgEls[+e.getAttribute("data-d")] = e; });
      rows(); var rt; window.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(rows, 120); });
      body.addEventListener("click", function (e) { var g = e.target.closest(".st-c"); if (!g) return; stop(); go(+g.getAttribute("data-i"), true, false); });
    }
    function setMode(on) {
      box.checked = on; put(KMODE, on ? "1" : "0");
      tb.hidden = on; if (pattern) pattern.hidden = on; if (player) player.hidden = on; wrap.hidden = !on;
      if (headH) headH.textContent = on ? "The whole song, note by note" : headHTxt;
      if (headP) headP.textContent = on ? "Every note in tab, on its string and fret, with how long it lasts in beats under it and a diagram wherever the hand takes a new grip. Back and Next play one note at a time; tap a note to start there." : headTxt;
      if (on) { if (audioEl && !audioEl.paused) audioEl.pause(); ensure(); requestAnimationFrame(rows); go(pos, false, false); }
      else stop();
    }

    /* ---------- sound: the guitar recordings ---------- */
    var ctx = null, live = [];
    function ac() {
      if (!ctx) { var AC = window.AudioContext || window.webkitAudioContext; if (!AC) return null; try { if (navigator.audioSession) navigator.audioSession.type = "playback"; } catch (e) { /* older browsers */ } ctx = new AC({ latencyHint: "playback" }); }
      if (ctx.state === "suspended") ctx.resume();
      return ctx;
    }
    var Guitar = (function () {
      var base = "../../assets/guitar/", man = null, manP = null, bufs = {}, loading = {};
      function manifest() {
        if (!manP) manP = fetch(base + "manifest.json").then(function (r) { return r.ok ? r.json() : null; }).then(function (j) { man = j; return j; }).catch(function () { manP = null; return null; });
        return manP;
      }
      function pk(s, m) {
        var st = man && man.strings[s]; if (st && st[m]) return { s: s, m: m };
        var best = null;
        Object.keys(man ? man.strings : {}).forEach(function (k) { Object.keys(man.strings[k]).forEach(function (n) { n = +n; var d = Math.abs(n - m) + (String(k) === String(s) ? 0 : 0.5); if (!best || d < best.d) best = { s: k, m: n, d: d }; }); });
        return best && Math.abs(best.m - m) <= 4 ? { s: best.s, m: best.m } : null;
      }
      function decode(c, ab) { return new Promise(function (res, rej) { var p = c.decodeAudioData(ab, res, rej); if (p && p.then) p.then(res, rej); }); }
      function load(c, s, m) {
        var key = s + "/" + m; if (bufs[key]) return Promise.resolve(bufs[key]);
        if (!loading[key]) loading[key] = fetch(base + "s" + s + "/" + m + ".mp3").then(function (r) { if (!r.ok) throw new Error("missing"); return r.arrayBuffer(); })
          .then(function (ab) { return decode(c, ab); })
          .then(function (buf) { var d = buf.getChannelData(0), mx = 0, i, n = Math.min(d.length, buf.sampleRate / 2); for (i = 0; i < n; i++) { var v = Math.abs(d[i]); if (v > mx) mx = v; } for (i = 0; i < n && Math.abs(d[i]) < mx * 0.05; i++); return (bufs[key] = { buf: buf, onset: Math.max(0, i / buf.sampleRate - 0.003), tune: (man.strings[s][m] || {}).tune || 0 }); })
          .catch(function () { delete loading[key]; return null; });
        return loading[key];
      }
      function want(c, list) { return manifest().then(function () { if (!man) return; return Promise.all(list.map(function (x) { var p = pk(x.s, x.m); return p ? load(c, p.s, p.m) : null; })); }); }
      function get(s, m) { if (!man) return null; var p = pk(s, m); var b = p && bufs[p.s + "/" + p.m]; return b ? { b: b, cents: (m - p.m) * 100 + b.tune } : null; }
      return { want: want, get: get };
    })();
    function bus(c) {
      if (c.__stBus) return c.__stBus;
      var input = c.createGain(), comp = c.createDynamicsCompressor(), wet = c.createGain(), conv = c.createConvolver();
      comp.threshold.value = -14; comp.knee.value = 10; comp.ratio.value = 3; comp.attack.value = 0.003; comp.release.value = 0.25;
      var len = Math.floor(c.sampleRate * 1.6), ir = c.createBuffer(2, len, c.sampleRate);
      for (var ch = 0; ch < 2; ch++) { var d = ir.getChannelData(ch), lp = 0, seed = 4321 + ch * 999; for (var i = 0; i < len; i++) { seed = (seed * 16807) % 2147483647; var t = i / c.sampleRate, nz = (seed / 2147483647) * 2 - 1, k = 0.22 + 0.6 * Math.exp(-t * 2.8); lp += k * (nz - lp); d[i] = t < 0.01 ? 0 : lp * Math.exp(-t * 3.9); } }
      conv.buffer = ir; wet.gain.value = 0.17; input.connect(comp); input.connect(conv); conv.connect(wet); wet.connect(comp); comp.connect(c.destination);
      return (c.__stBus = input);
    }
    var LVL = { t: 1, b: 0.82, i: 0.55 };
    function pluck(c, n, when, ring) {
      var smp = Guitar.get(n.s, n.m), g = c.createGain(), lvl = 0.72 * (LVL[n.r] || 0.6) * (n.h ? 0.8 : 1), src;
      g.gain.setValueAtTime(lvl, when); g.gain.setValueAtTime(lvl, when + ring); g.gain.setTargetAtTime(0, when + ring, 0.07); g.connect(bus(c));
      if (smp) { src = c.createBufferSource(); src.buffer = smp.b.buf; if (src.detune) src.detune.value = smp.cents; else src.playbackRate.value = Math.pow(2, smp.cents / 1200); src.connect(g); src.start(when, smp.b.onset); }
      else { src = c.createOscillator(); src.type = "triangle"; src.frequency.value = 440 * Math.pow(2, (n.m - 69) / 12); var e = c.createGain(); e.gain.setValueAtTime(0.0001, when); e.gain.exponentialRampToValueAtTime(0.3, when + 0.005); e.gain.exponentialRampToValueAtTime(0.02, when + 1.4); src.connect(e); e.connect(g); src.start(when); }
      src.stop(when + ring + 0.6); live.push(src);
      src.onended = function () { var i = live.indexOf(src); if (i >= 0) live.splice(i, 1); };
    }
    function hush() { var c = ctx; if (!c) return; var t = c.currentTime; live.forEach(function (x) { try { x.stop(t + 0.08); } catch (e) { /* already stopped */ } }); live = []; }

    /* ---------- stepping and playing ---------- */
    var pos = Math.min(S.length - 1, Math.max(0, parseInt(get(KPOS) || "0", 10) || 0));
    var rate = parseFloat(get(KRATE) || "1"); if ([0.5, 0.75, 1].indexOf(rate) < 0) rate = 1;
    var playing = false, t0 = 0, c0 = 0, next = 0, timer = 0, raf = 0, litCol = null, litHold = [], litDots = [];
    function rateUi() { wrap.querySelectorAll(".st-rate button").forEach(function (b) { b.setAttribute("aria-pressed", +b.getAttribute("data-r") === rate ? "true" : "false"); }); }
    rateUi();
    function chunkOf(i) { for (var j = 0; j < CH.length; j++) if (i >= CH[j].s0 && i < CH[j].s1) return j; return 0; }
    function show(i, scroll) {
      var sp = S[i]; if (!sp) return;
      if (litCol) litCol.classList.remove("now");
      litCol = colEls[i]; if (litCol) litCol.classList.add("now");
      litHold.forEach(function (e) { e.classList.remove("st-hold"); }); litHold = [];
      for (var j = sp.notes[0].i - 1; j >= 0 && EV[j].t > sp.t - 30; j--) {
        var n = EV[j]; if (n.t < sp.t - 1e-4 && n.t1 > sp.t + 0.03) { var e = document.getElementById("st-n" + n.i); if (e) { e.classList.add("st-hold"); litHold.push(e); } }
      }
      litDots.forEach(function (e) { e.classList.remove("on"); }); litDots = [];
      var svg = sp.dg && dgEls[sp.dg.n];
      if (svg) sp.notes.forEach(function (n) { if (n.h) return; var d = svg.querySelector('[data-k="' + n.s + ":" + n.f + '"]'); if (d) { d.classList.add("on"); litDots.push(d); } });
      var b = FR[sp.bi].bar, beat = Math.floor(sp.x + 1e-6) + 1;
      at.innerHTML = "<b>Bar " + esc(b.label) + "</b>, beat " + beat + (sp.c ? " · " + esc(disp(sp.c)) : "");
      if (scroll) {
        var el = frEls[chunkOf(i)]; if (el) { var r = el.getBoundingClientRect(), top = wrap.querySelector(".st-ctl").getBoundingClientRect().bottom + 8;
          if (r.top < top || r.bottom > window.innerHeight - 12) window.scrollTo({ top: window.scrollY + r.top - top - Math.max(0, (window.innerHeight - top - r.height) / 3), behavior: reduce ? "auto" : "smooth" }); }
      }
    }
    function go(i, sound, scroll) {
      pos = Math.max(0, Math.min(S.length - 1, i)); put(KPOS, String(pos));
      show(pos, scroll !== false);
      if (sound) { var c = ac(); if (!c) return; hush(); var sp = S[pos];
        Guitar.want(c, sp.notes).then(function () { var w = c.currentTime + 0.02; sp.notes.forEach(function (n) { pluck(c, n, w, Math.min(2.4, Math.max(0.5, (n.t1 - n.t) / rate))); }); }); }
    }
    function tick() {
      if (!playing) return;
      var c = ctx, ahead = c.currentTime + 0.35;
      while (next < S.length && c0 + (S[next].t - t0) / rate <= ahead) {
        var sp = S[next], when = c0 + (sp.t - t0) / rate;
        sp.notes.forEach(function (n) { pluck(c, n, Math.max(c.currentTime, when), Math.max(0.12, (n.t1 - n.t) / rate)); });
        next++;
      }
      if (next >= S.length && c.currentTime > c0 + (END - t0) / rate) { stop(); return; }
      timer = setTimeout(tick, 60);
    }
    function follow() {
      if (!playing) return;
      var t = t0 + (ctx.currentTime - c0) * rate, lo = 0, hi = S.length - 1;
      while (lo < hi) { var m = (lo + hi + 1) >> 1; if (S[m].t <= t + 0.01) lo = m; else hi = m - 1; }
      if (S[lo].t <= t + 0.01 && lo !== pos) { pos = lo; show(pos, true); }
      raf = requestAnimationFrame(follow);
    }
    function play() {
      var c = ac(); if (!c) return;
      if (pos >= S.length - 1) pos = 0;
      playing = true; playB.innerHTML = "&#10074;&#10074; Pause"; playB.setAttribute("aria-label", "Pause");
      var from = pos, soon = [];
      for (var j = from; j < Math.min(S.length, from + 48); j++) soon = soon.concat(S[j].notes);
      Guitar.want(c, soon).then(function () {
        if (!playing) return;
        t0 = S[from].t; c0 = c.currentTime + 0.08; next = from; show(from, true); tick(); follow();
        var rest = []; for (var j = from + 48; j < S.length; j++) rest = rest.concat(S[j].notes); Guitar.want(c, rest);
      });
    }
    function stop() {
      if (!playing) return; playing = false; clearTimeout(timer); cancelAnimationFrame(raf); hush();
      playB.innerHTML = "&#9654; Play"; playB.removeAttribute("aria-label"); put(KPOS, String(pos));
    }
    wrap.querySelector(".st-ctl").addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b) return;
      var a = b.getAttribute("data-a"), r = b.getAttribute("data-r");
      if (r) { var was = playing; stop(); rate = +r; put(KRATE, r); rateUi(); if (was) play(); return; }
      if (a === "play") { if (playing) stop(); else play(); }
      else if (a === "next") { stop(); go(pos + 1, true); }
      else if (a === "back") { stop(); go(pos - 1, true); }
    });
    document.addEventListener("keydown", function (e) {
      if (wrap.hidden || e.altKey || e.ctrlKey || e.metaKey) return;
      var tg = e.target && e.target.tagName; if (tg === "INPUT" || tg === "TEXTAREA" || tg === "SELECT") return;
      if (e.key === "ArrowRight") { e.preventDefault(); stop(); go(pos + 1, true); }
      else if (e.key === "ArrowLeft") { e.preventDefault(); stop(); go(pos - 1, true); }
    });
    if (audioEl) audioEl.addEventListener("play", function () { if (!wrap.hidden) audioEl.pause(); });
    box.addEventListener("change", function () { setMode(box.checked); });
    window.__ffSongTabData = { steps: S.length, notes: EV.length, grips: DG.length, chunks: CH.length };
    setMode(get(KMODE) === "1");
  }
  /* the page draws its bars first */
  function when() { if (document.querySelector('[id^="tb-"] .fbar')) start(); else setTimeout(when, 120); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", when); else when();
})();

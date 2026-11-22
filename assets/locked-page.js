/* Fret Finder: a song page with a locked copy.
   Where the faithful version of a page holds music still under copyright (a tune's own phrase, say), that version
   sits beside the open page as a ".locked" file, encrypted to the singer key like the singer tracks.
   - On the open page, <meta name="ff-locked-copy" content="real.html"> names the copy's address. A device that holds
     the singer key goes there; everyone else stays on the open page.
   - On the copy's address (a small stub page), <meta name="ff-locked-file" content="real.html.locked"> names the file.
     This script opens it with the key and writes it in as the page. If it can't, it goes back to the open page and
     stays there for the rest of the visit.
   - The stub may also name scripts from assets/ with <meta name="ff-also" content="NAME.js">; they are added to the copy.
   - A page of the Classical section is locked whole: its stub also names <meta name="ff-locked-back" content="../../">,
     where a device without the key goes instead. */
(function () {
  "use strict";
  var KEY = "ff.voicekey", S = window.crypto && window.crypto.subtle;
  function key() { try { return localStorage.getItem(KEY) || ""; } catch (e) { return ""; } }
  function plainKey() { return "ff.plain:" + location.pathname.replace(/[^/]*$/, ""); }
  function plain(v) { try { if (v === undefined) return sessionStorage.getItem(plainKey()) === "1"; sessionStorage.setItem(plainKey(), "1"); } catch (e) { return false; } }
  var root = document.documentElement;
  var copy = document.querySelector('meta[name="ff-locked-copy"]');
  if (copy && window.FF_LEAVING) return;          /* assets/eight.js is taking this visit to the 8-string page */
  if (copy) {
    if (key() && S && !plain()) { root.style.visibility = "hidden"; location.replace(copy.getAttribute("content") + location.hash); }
    return;
  }
  var file = document.querySelector('meta[name="ff-locked-file"]');
  if (!file) return;
  /* A page of the locked Classical section has no open page: without the key it goes back to the library. */
  var away = document.querySelector('meta[name="ff-locked-back"]');
  function back() { if (away) return location.replace(away.getAttribute("content")); plain(true); location.replace("./" + location.hash); }
  if (!key() || !S) return back();
  var base; try { base = new URL("../../assets/", location.href).href; } catch (e) { base = "../../assets/"; }
  var INFO = new TextEncoder().encode("fret-finder voice");
  function toD(w) {
    w = String(w || "").replace(/\s+/g, "");
    if (/^[A-Za-z0-9_-]{43}$/.test(w)) return Promise.resolve(w);
    var te = new TextEncoder();
    return S.importKey("raw", te.encode(w.toLowerCase()), "PBKDF2", false, ["deriveBits"])
      .then(function (k) { return S.deriveBits({ name: "PBKDF2", hash: "SHA-256", salt: te.encode("fret-finder voice key"), iterations: 100000 }, k, 256); })
      .then(function (b) { var s = ""; new Uint8Array(b).forEach(function (c) { s += String.fromCharCode(c); }); return btoa(s).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, ""); });
  }
  function open(buf, d) {
    var u = new Uint8Array(buf);
    if (u.length < 82 || String.fromCharCode(u[0], u[1], u[2], u[3]) !== "FFV1") return Promise.reject(new Error("not a locked file"));
    var epk = u.slice(4, 69), iv = u.slice(69, 81), ct = u.slice(81);
    return Promise.all([fetch(base + "voice-key.json").then(function (r) { return r.json(); }), toD(d)]).then(function (pd) {
      return Promise.all([
        S.importKey("jwk", { kty: "EC", crv: "P-256", x: pd[0].x, y: pd[0].y, d: pd[1], ext: true }, { name: "ECDH", namedCurve: "P-256" }, false, ["deriveBits"]),
        S.importKey("raw", epk, { name: "ECDH", namedCurve: "P-256" }, false, [])
      ]);
    }).then(function (k) { return S.deriveBits({ name: "ECDH", public: k[1] }, k[0], 256); })
      .then(function (bits) { return S.importKey("raw", bits, "HKDF", false, ["deriveKey"]); })
      .then(function (hk) { return S.deriveKey({ name: "HKDF", hash: "SHA-256", salt: epk, info: INFO }, hk, { name: "AES-GCM", length: 256 }, false, ["decrypt"]); })
      .then(function (k) { return S.decrypt({ name: "AES-GCM", iv: iv }, k, ct); });
  }
  fetch(file.getAttribute("content"), { cache: "no-cache" })
    .then(function (r) { if (!r.ok) throw new Error("missing"); return r.arrayBuffer(); })
    .then(function (b) { return open(b, key()); })
    .then(function (pt) {
      var html = new TextDecoder().decode(pt);
      /* the stub can name more of the site's scripts for the copy (<meta name="ff-also" content="songtab.js">):
         they join the page after its own, so a copy gains a feature without being locked again */
      Array.prototype.forEach.call(document.querySelectorAll('meta[name="ff-also"]'), function (m) {
        var f = m.getAttribute("content"); if (/^[a-z0-9-]+\.js$/.test(f)) html += '\n<script src="' + base + f + '" defer></script>';
      });
      document.open(); document.write(html); document.close();
    })
    .catch(back);
})();

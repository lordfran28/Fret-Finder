/* Fret Finder: the 8-string version of a song.
   Every song page carries a checkbox, "8 strings". Ticked, the choice holds for every song on this device
   (localStorage ff.eight), and a song that has an 8-string version opens it: the page names it with
   <meta name="ff-eight" content="eight.html">, and the 8-string page names its way back with <meta name="ff-six">.
   A song without one yet stays on six strings and says so beside the box.
   Load this right after those metas and before assets/locked-page.js, which it can stop from leaving. */
(function () {
  "use strict";
  var KEY = "ff.eight";
  function on(v) {
    try { if (v === undefined) return localStorage.getItem(KEY) === "1"; localStorage.setItem(KEY, v ? "1" : "0"); } catch (e) { return false; }
  }
  var eightTo = document.querySelector('meta[name="ff-eight"]'), sixTo = document.querySelector('meta[name="ff-six"]');
  var root = document.documentElement;
  function go(url) { window.FF_LEAVING = true; root.style.visibility = "hidden"; location.replace(url + location.hash); }
  if (on() && eightTo) return go(eightTo.getAttribute("content"));
  if (!on() && sixTo) return go(sixTo.getAttribute("content"));

  var PIC = "../../assets/eight-headstock.jpg";   /* a real photo of an 8-string classical headstock, turned on its side */
  var css = ".ff-eight{display:inline-flex;align-items:center;gap:7px;margin-left:auto;font:inherit;font-size:.95em;cursor:pointer;" +
    "white-space:nowrap;user-select:none}.ff-eight input{width:1.05em;height:1.05em;margin:0;accent-color:currentColor;cursor:pointer}" +
    ".ff-eight img{height:2.2em;width:auto;display:block;border-radius:3px}.ff-eight small{opacity:.7;font-style:italic;white-space:normal}" +
    ".ff-shelf{display:flex;align-items:center;flex-wrap:wrap;gap:6px 14px}";
  function build() {
    var hd = document.querySelector("header.ff-shelf");
    if (!hd || hd.querySelector(".ff-eight")) return;
    var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);
    var lab = document.createElement("label"); lab.className = "ff-eight";
    var box = document.createElement("input"); box.type = "checkbox"; box.checked = on();
    box.setAttribute("aria-describedby", "ff-eight-note");
    var img = null; if (PIC) { img = new Image(); img.alt = ""; img.src = PIC; img.onerror = function () { img.remove(); }; }
    var txt = document.createElement("span"); txt.textContent = "8 strings";
    var note = document.createElement("small"); note.id = "ff-eight-note";
    function say() { note.textContent = (box.checked && !eightTo && !sixTo) ? "no 8-string version of this song yet" : ""; }
    lab.appendChild(box); if (img) lab.appendChild(img); lab.appendChild(txt); lab.appendChild(note); say();
    box.addEventListener("change", function () {
      on(box.checked); say();
      if (box.checked && eightTo) go(eightTo.getAttribute("content"));
      else if (!box.checked && sixTo) go(sixTo.getAttribute("content"));
    });
    hd.appendChild(lab);
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", build); else build();
})();

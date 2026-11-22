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

  /* An 8-string classical headstock, from his photo (the full-size one), engraved: lines along the neck whose weight follows the shade, cut out of
     the photo's background. The file is the lines alone; the page's ink colours them, so it prints in either theme. */
  var PIC = "../../assets/eight-headstock-engraved.png";
  var css = ".ff-eight{display:inline-flex;align-items:center;gap:7px;margin-left:auto;font:inherit;font-size:.95em;cursor:pointer;" +
    "white-space:nowrap;user-select:none}" +
    ".ff-eight input{-webkit-appearance:none;appearance:none;width:.95em;height:.95em;margin:0;cursor:pointer;flex:none;" +
    "border:1.5px solid var(--muted,#6A5546);border-radius:2px;background:transparent;transition:background-color .25s ease,border-color .25s ease}" +
    ".ff-eight input:checked{border-color:var(--accent,#8A2E1E);background:var(--accent,#8A2E1E) url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 10 10'%3E%3Cpath d='M2 5.2l2 2 4-4.4' fill='none' stroke='%23FFF6EE' stroke-width='1.6' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E\") center/100% no-repeat}" +
    ".ff-eight input:focus-visible{outline:2px solid var(--accent,#8A2E1E);outline-offset:2px}" +
    ".ff-eight .ff-plate{display:block;height:2.7em;aspect-ratio:420/203;background:var(--muted,#6A5546);" +
    "-webkit-mask:url(" + PIC + ") center/contain no-repeat;mask:url(" + PIC + ") center/contain no-repeat;transition:background-color .35s ease}" +
    ".ff-eight input:checked~.ff-plate{background:var(--accent,#8A2E1E)}" +
    ".ff-eight span.ff-eight-name{font:italic 400 1.05rem var(--display,serif);color:var(--muted)}" +
    ".ff-eight input:checked~.ff-eight-name{color:var(--accent)}" +
    ".ff-eight small{opacity:.7;font-style:italic;white-space:normal}" +
    ".ff-shelf{display:flex;align-items:center;flex-wrap:wrap;gap:6px 14px}";
  function build() {
    var hd = document.querySelector("header.ff-shelf");
    if (!hd || hd.querySelector(".ff-eight")) return;
    var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);
    var lab = document.createElement("label"); lab.className = "ff-eight";
    var box = document.createElement("input"); box.type = "checkbox"; box.checked = on();
    box.setAttribute("aria-describedby", "ff-eight-note");
    var img = null; if (PIC) { img = document.createElement("span"); img.className = "ff-plate"; img.setAttribute("aria-hidden", "true"); }
    var txt = document.createElement("span"); txt.className = "ff-eight-name"; txt.textContent = "8 strings";
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

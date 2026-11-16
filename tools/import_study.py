#!/usr/bin/env python3
"""Put an Exercises entry made in conversation onto Fret Finder.

    python3 tools/import_study.py PAGE.html SLUG "Title" --style "Wyble" [--file NAME=PATH ...] [--added ISO-DATE]

Writes studies/SLUG/index.html (the page with Fret Finder's look and a way back to the library), copies the media
files it uses next to it, and writes studies/SLUG/entry.json for the list of exercises.
"""
import argparse, datetime, json, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page")
    ap.add_argument("slug")
    ap.add_argument("title")
    ap.add_argument("--style", required=True, help="the group it is listed under, e.g. Wyble, Tango, Flamenco")
    ap.add_argument("--file", action="append", default=[], help="NAME=PATH of a file the page uses")
    ap.add_argument("--added", default="")
    a = ap.parse_args()
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,79}", a.slug):
        sys.exit("The slug must be lower-case letters, digits and dashes.")
    out = os.path.join(ROOT, "studies", a.slug)
    os.makedirs(out, exist_ok=True)

    html = open(a.page, encoding="utf-8").read()
    shelf = '<link rel="stylesheet" href="../../assets/shelf.css">'
    bar = ('<header class="ff-shelf"><a href="../../">&larr; Fret Finder</a>'
           '<span class="ff-mark">Exercises</span></header>')
    html = html.replace(shelf, "")
    html = re.sub(r'<header class="ff-shelf">.*?</header>', "", html, flags=re.S)
    html = html.replace("</head>", shelf + "</head>", 1) if "</head>" in html else shelf + html
    m = re.search(r"<body[^>]*>", html)
    html = html[:m.end()] + bar + html[m.end():] if m else bar + html
    # the dots light up as their notes sound; slower speeds under the player
    for src in ("ring.js", "speed.js"):
        tag = '<script src="../../assets/%s" defer></script>' % src
        html = html.replace(tag, "")
        html = html.replace("</body>", tag + "</body>", 1) if "</body>" in html else html + tag
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

    used = []
    for spec in a.file:
        name, _, path = spec.partition("=")
        if not name or not path or "/" in name or name.startswith("."):
            sys.exit("Bad --file %r" % spec)
        shutil.copyfile(path, os.path.join(out, name))
        used.append(name)

    meta_path = os.path.join(out, "entry.json")
    meta = {}
    if os.path.exists(meta_path):
        try:
            meta = json.load(open(meta_path, encoding="utf-8"))
        except ValueError:
            meta = {}
    files = ["index.html"] + used
    if not used:      # a page-only update keeps the media already there
        files = [f for f in (meta.get("files") or ["index.html"]) if f == "index.html" or os.path.exists(os.path.join(out, f))]
    meta.update({"title": a.title, "kind": "exercises", "style": a.style, "files": files})
    meta.setdefault("addedAt", a.added or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("studies/%s: %s (%s), %d media file(s)." % (a.slug, a.title, a.style, len(used)))


if __name__ == "__main__":
    main()

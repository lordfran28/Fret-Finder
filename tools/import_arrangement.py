#!/usr/bin/env python3
"""Put an arrangement page made in conversation onto the Fret Finder shelf.

    python3 tools/import_arrangement.py PAGE.html SLUG "Title" [--file NAME=PATH ...] [--drop-alt]
        [--locked NAME.mp3.locked=PATH ...] [--instrument guitar] [--source URL] [--added ISO-DATE]

Writes songs/SLUG/index.html (the page with Fret Finder's look and a way back to the songs),
copies the media files it uses next to it, and writes songs/SLUG/song.json for the song list.

--drop-alt removes the page's second audio track (audio_alt), for example a mix with a record's
own vocal, which mustn't go on a public site.

--locked puts a track with a record's own singer on the page locked (see assets/voice.js): PATH is the
mp3, NAME is what the page's data calls it and must end in ".mp3.locked". It plays only on devices
where the owner entered the singer key; everywhere else its button is hidden.
"""
import argparse, datetime, json, os, re, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shelf_voice

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("page")
    ap.add_argument("slug")
    ap.add_argument("title")
    ap.add_argument("--file", action="append", default=[], help="NAME=PATH of a file the page uses")
    ap.add_argument("--drop-alt", action="store_true")
    ap.add_argument("--locked", action="append", default=[], help="NAME.mp3.locked=PATH of a singer's track")
    ap.add_argument("--instrument", default="guitar")
    ap.add_argument("--source", default="")
    ap.add_argument("--added", default="")
    a = ap.parse_args()

    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,79}", a.slug):
        sys.exit("The slug must be lower-case letters, digits and dashes.")
    out = os.path.join(ROOT, "songs", a.slug)
    os.makedirs(out, exist_ok=True)

    html = open(a.page, encoding="utf-8").read()
    if a.drop_alt:
        html, n = re.subn(r'"audio_alt"\s*:\s*"[^"]*"', '"audio_alt":""', html)
        print("Second audio track removed from %d place(s)." % n)

    # Fret Finder's look goes in the head; a way back to the songs goes at the top of the body.
    shelf = '<link rel="stylesheet" href="../../assets/shelf.css">'
    bar = ('<header class="ff-shelf"><a href="../../">&larr; Fret Finder</a>'
           '<span class="ff-mark">%s</span></header>' % a.instrument.capitalize())
    html = re.sub(r'<link rel="stylesheet" href="\.\./\.\./assets/shelf\.css">', "", html)
    html = re.sub(r'<header class="ff-shelf">.*?</header>', "", html, flags=re.S)
    if "</head>" in html:
        html = html.replace("</head>", shelf + "</head>", 1)
    else:
        html = shelf + html
    m = re.search(r"<body[^>]*>", html)
    if m:
        html = html[:m.end()] + bar + html[m.end():]
    else:
        html = bar + html
    # The dots light up as their notes sound, and the fret number beside each diagram is huge.
    ring = '<script src="../../assets/ring.js" defer></script>'
    html = html.replace(ring, "")
    # The singer's track, locked: playable only on the owner's devices.
    html = shelf_voice.mark_locked(shelf_voice.add_voice_script(html))
    html = html.replace("</body>", ring + "</body>", 1) if "</body>" in html else html + ring
    # Slower tracks for practising along: a row of speeds under every player, the pitch unchanged.
    speed = '<script src="../../assets/speed.js" defer></script>'
    html = html.replace(speed, "")
    html = html.replace("</body>", speed + "</body>", 1) if "</body>" in html else html + speed
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

    used = []
    for spec in a.file:
        name, _, path = spec.partition("=")
        if not name or not path or "/" in name or name.startswith("."):
            sys.exit("Bad --file %r" % spec)
        if a.drop_alt and name not in html:
            print("Skipped %s: the page no longer uses it." % name)
            continue
        shutil.copyfile(path, os.path.join(out, name))
        used.append(name)

    for spec in a.locked:
        name, _, path = spec.partition("=")
        if not name.endswith(".mp3.locked") or not path or "/" in name:
            sys.exit("Bad --locked %r" % spec)
        if name not in html:
            sys.exit("The page doesn't use %s; add it to the page's track list first." % name)
        shelf_voice.lock(path, os.path.join(out, name))
        used.append(name)

    meta_path = os.path.join(out, "song.json")
    meta = {}
    if os.path.exists(meta_path):
        try:
            meta = json.load(open(meta_path, encoding="utf-8"))
        except ValueError:
            meta = {}
    meta.update({
        "title": a.title,
        "kind": "arrangement",
        "instrument": a.instrument,
        "files": ["index.html"] + used,
    })
    if a.source:
        meta["source"] = a.source
    meta.setdefault("addedAt", a.added or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("songs/%s: %s, %d media file(s)." % (a.slug, a.title, len(used)))


if __name__ == "__main__":
    main()

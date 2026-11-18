#!/usr/bin/env python3
"""The Classical section of the library: pieces locked whole, so only the owner's devices see them.

    python3 tools/classical.py add PAGE.html SLUG "Composer – Title" --composer NAME [--what "Solo guitar"]
        [--arranger NAME] [--file NAME=PATH ...] [--source URL] [--added ISO-DATE]
    python3 tools/classical.py move SLUG [--composer NAME] [--what ...] [--arranger NAME]
    python3 tools/classical.py index

Each piece is a folder classical/<id>/, where <id> is a fixed hash of its slug (piece_id below), so the folder
names say nothing about the pieces:

    index.html         a small stub page: on a device with the singer key, assets/locked-page.js opens
                       page.html.locked and writes it in; anywhere else it goes back to the library
    page.html.locked   the whole page (Fret Finder's look added as for the songs), locked with tools/lock_voice.mjs
    piece.locked       its title, composer, arranger and date, locked the same way, for the library's list
    *.mp3.locked       every track, locked

classical/index.json lists the folders and nothing else. The library shows the section only where the singer
key is on the device, reading each piece.locked there.

add    takes a page made in conversation, gives it Fret Finder's look and locks it with the files it uses.
move   takes a page already on the shelf (songs/SLUG/) into the section and takes it off the song list.
index  writes classical/index.json from the folders.
"""
import argparse, datetime, hashlib, json, os, re, shutil, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import shelf_voice
from import_arrangement import shelf_look

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, ".."))
DIR = os.path.join(ROOT, "classical")

STUB = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex">'
        '<meta name="ff-locked-file" content="page.html.locked"><meta name="ff-locked-back" content="../../">'
        '<title>Fret Finder</title><style>body{margin:0;background:#F1F2F4}'
        '@media (prefers-color-scheme:dark){body{background:#15171B}}</style>'
        '<script src="../../assets/locked-page.js"></script></head><body></body></html>\n')


def piece_id(slug):
    return hashlib.sha256(("fret-finder classical " + slug).encode()).hexdigest()[:12]


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def lock_bytes(data, dst):
    with tempfile.NamedTemporaryFile(delete=False) as t:
        t.write(data)
    try:
        shelf_voice.lock(t.name, dst)
    finally:
        os.unlink(t.name)


def lock_tracks(html, names):
    """Every track the page names, plain mp3 in the page, becomes NAME.locked."""
    for n in names:
        html = re.sub(r'(?<![\w.-])' + re.escape(n) + r'(?![\w.-])', n + ".locked", html)
    return shelf_voice.mark_locked(html)


def write_piece(slug, html, media, meta):
    """media: {name: path}; plain mp3s are locked, files already locked are copied as they are."""
    out = os.path.join(DIR, piece_id(slug))
    if os.path.isdir(out):
        shutil.rmtree(out)
    os.makedirs(out)
    plain = [n for n in media if not n.endswith(".locked")]
    # every track is locked, so every page needs assets/voice.js to play them (some older pages had no locked track)
    html = lock_tracks(shelf_voice.add_voice_script(html), [n for n in plain if n.lower().endswith((".mp3", ".m4a"))])
    files = []
    for n, p in media.items():
        if n.endswith(".locked"):
            with open(p, "rb") as f:
                if f.read(4) != b"FFV1":
                    sys.exit("%s is named .locked but isn't locked" % p)
            shutil.copyfile(p, os.path.join(out, n)); files.append(n)
        elif n.lower().endswith((".mp3", ".m4a")):
            shelf_voice.lock(p, os.path.join(out, n + ".locked")); files.append(n + ".locked")
        else:
            sys.exit("Only audio goes next to a locked page; %s would be open to anyone." % n)
    lock_bytes(html.encode("utf-8"), os.path.join(out, "page.html.locked"))
    meta = dict(meta, slug=slug, files=["page.html.locked"] + files)
    lock_bytes(json.dumps(meta, ensure_ascii=False).encode("utf-8"), os.path.join(out, "piece.locked"))
    with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:
        f.write(STUB)
    print("classical/%s: %s, %d track(s), all locked." % (piece_id(slug), meta["title"], len(files)))
    return out


def write_index():
    pieces = []
    for d in sorted(os.listdir(DIR)) if os.path.isdir(DIR) else []:
        f = os.path.join(DIR, d)
        if os.path.isdir(f) and all(os.path.exists(os.path.join(f, x)) for x in ("index.html", "page.html.locked", "piece.locked")):
            pieces.append({"id": d})
    with open(os.path.join(DIR, "index.json"), "w", encoding="utf-8") as fh:
        json.dump({"pieces": pieces}, fh, indent=1)
        fh.write("\n")
    print("classical/index.json: %d piece(s)." % len(pieces))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a1 = sub.add_parser("add")
    a1.add_argument("page"); a1.add_argument("slug"); a1.add_argument("title")
    a2 = sub.add_parser("move")
    a2.add_argument("slug")
    for p in (a1, a2):
        p.add_argument("--composer", default="")
        p.add_argument("--what", default="", help='what the page is for, e.g. "Solo guitar" or "Voice and guitar"')
        p.add_argument("--arranger", default="")
    a1.add_argument("--file", action="append", default=[], help="NAME=PATH of a track the page uses")
    a1.add_argument("--source", default="")
    a1.add_argument("--added", default="")
    sub.add_parser("index")
    a = ap.parse_args()

    if a.cmd == "index":
        return write_index()
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,79}", a.slug):
        sys.exit("The slug must be lower-case letters, digits and dashes.")
    os.makedirs(DIR, exist_ok=True)

    if a.cmd == "add":
        html = shelf_look(open(a.page, encoding="utf-8").read(), "guitar")
        media = {}
        for spec in a.file:
            n, _, p = spec.partition("=")
            if not n or not p or "/" in n:
                sys.exit("Bad --file %r" % spec)
            media[n] = p
        meta = {"title": a.title, "composer": a.composer, "what": a.what or "Solo guitar", "arranger": a.arranger,
                "source": a.source, "addedAt": a.added or now()}
        write_piece(a.slug, html, media, meta)
    else:
        src = os.path.join(ROOT, "songs", a.slug)
        song = json.load(open(os.path.join(src, "song.json"), encoding="utf-8"))
        html = open(os.path.join(src, "index.html"), encoding="utf-8").read()
        media = {n: os.path.join(src, n) for n in sorted(os.listdir(src))
                 if n.lower().endswith((".mp3", ".m4a", ".mp3.locked", ".m4a.locked"))}
        extra = [n for n in os.listdir(src) if n not in media and n not in ("index.html", "song.json")]
        if extra:
            sys.exit("songs/%s holds files the move doesn't handle: %s" % (a.slug, ", ".join(extra)))
        meta = {"title": song.get("title", a.slug), "composer": a.composer, "what": a.what or "Voice and guitar",
                "arranger": a.arranger, "source": song.get("source", ""), "addedAt": song.get("addedAt") or now()}
        write_piece(a.slug, html, media, meta)
        subprocess.run(["git", "-C", ROOT, "rm", "-r", "-q", "--", os.path.join("songs", a.slug)], check=True)
        print("songs/%s taken off the song list." % a.slug)
    write_index()


if __name__ == "__main__":
    main()

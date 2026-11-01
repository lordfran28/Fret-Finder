#!/usr/bin/env python3
"""Writes songs/index.json: the list of songs the site shows.

A folder under songs/ with a song.json in it is an arrangement made in conversation: its page is
the folder's index.html. Any MusicXML, MIDI or Guitar Pro file elsewhere under songs/ is listed too.
A file may have a companion "<file>.ff.json", written by the site, holding its title and settings.
"""
import datetime, hashlib, json, os, re, subprocess, unicodedata

ROOT = "songs"
KINDS = {".mid": "MIDI", ".midi": "MIDI", ".musicxml": "MusicXML", ".xml": "MusicXML", ".mxl": "MusicXML", ".gp": "Guitar Pro", ".gp5": "Guitar Pro", ".gp4": "Guitar Pro", ".gp3": "Guitar Pro"}
OUT = os.path.join(ROOT, "index.json")


def first_added(path):
    try:
        out = subprocess.run(["git", "log", "--diff-filter=A", "--follow", "--format=%aI", "--", path],
                             capture_output=True, text=True, check=True).stdout.split()
        if out:
            return out[-1]
    except Exception:
        pass
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def utc(stamp):
    try:
        d = datetime.datetime.fromisoformat(str(stamp).replace("Z", "+00:00"))
        if d.tzinfo is None:
            d = d.replace(tzinfo=datetime.timezone.utc)
        return d.astimezone(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    except ValueError:
        return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def sha1(path):
    with open(path, "rb") as f:
        return hashlib.sha1(f.read()).hexdigest()


def slug(text):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "song"


def main():
    songs, used = [], set()
    for folder, dirs, files in os.walk(ROOT):
        dirs[:] = sorted(d for d in dirs if not d.startswith("."))
        if folder != ROOT and "song.json" in files and "index.html" in files:
            try:
                with open(os.path.join(folder, "song.json"), encoding="utf-8") as f:
                    meta = json.load(f) or {}
            except (OSError, ValueError):
                meta = {}
            rel = folder.replace(os.sep, "/")
            sid = slug(rel[len(ROOT) + 1:])
            while sid in used:
                sid += "-2"
            used.add(sid)
            songs.append({
                "id": sid,
                "file": rel + "/",
                "page": rel + "/",
                "title": str(meta.get("title") or os.path.basename(folder)),
                "kind": "arrangement",
                "instrument": str(meta.get("instrument") or "guitar"),
                "addedAt": utc(meta.get("addedAt") or first_added(os.path.join(folder, "song.json"))),
            })
            dirs[:] = []
            continue
        for name in sorted(files):
            stem, ext = os.path.splitext(name)
            if ext.lower() not in KINDS or name.startswith("."):
                continue
            path = os.path.join(folder, name).replace(os.sep, "/")
            side = {}
            try:
                with open(path + ".ff.json", encoding="utf-8") as f:
                    side = json.load(f) or {}
            except (OSError, ValueError):
                side = {}
            sid = str(side.get("id") or "")
            if not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", sid) or sid in used:
                base = slug(os.path.splitext(path[len(ROOT) + 1:])[0])
                sid, n = base, 2
                while sid in used:
                    sid, n = "%s-%d" % (base, n), n + 1
            used.add(sid)
            entry = {
                "id": sid,
                "file": path,
                "title": str(side.get("title") or stem.replace("_", " ").strip() or "Untitled song"),
                "kind": KINDS[ext.lower()],
                "sha1": sha1(path),
                "addedAt": utc(side.get("addedAt") or first_added(path)),
            }
            units = side.get("units")
            if isinstance(units, dict) and isinstance(units.get("count"), int):
                entry["units"] = {"count": units["count"], "unit": str(units.get("unit") or "Bar")}
            songs.append(entry)
    songs.sort(key=lambda s: (str(s["addedAt"]), s["file"]))

    try:
        with open(OUT, encoding="utf-8") as f:
            if json.load(f).get("songs") == songs:
                print("Song list unchanged (%d songs)." % len(songs))
                return
    except (OSError, ValueError, AttributeError):
        pass
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"app": "Fret Finder", "generatedAt": now, "songs": songs}, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("Wrote %d songs." % len(songs))


if __name__ == "__main__":
    main()

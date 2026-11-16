#!/usr/bin/env python3
"""Writes studies/index.json: the Exercises entries the library lists, each folder under studies/ with an entry.json."""
import datetime, json, os

ROOT = "studies"
OUT = os.path.join(ROOT, "index.json")


def main():
    out = []
    if os.path.isdir(ROOT):
        for name in sorted(os.listdir(ROOT)):
            folder = os.path.join(ROOT, name)
            meta_path = os.path.join(folder, "entry.json")
            if not (os.path.isdir(folder) and os.path.exists(meta_path) and os.path.exists(os.path.join(folder, "index.html"))):
                continue
            try:
                meta = json.load(open(meta_path, encoding="utf-8")) or {}
            except (OSError, ValueError):
                meta = {}
            out.append({
                "id": name,
                "page": ROOT + "/" + name + "/",
                "title": str(meta.get("title") or name),
                "style": str(meta.get("style") or "Other"),
                "addedAt": str(meta.get("addedAt") or datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")),
            })
    os.makedirs(ROOT, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump({"studies": out}, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("%d exercise entries" % len(out))


if __name__ == "__main__":
    main()

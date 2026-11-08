#!/usr/bin/env python3
"""Bakes landmarks.json into the photo editor -> tools/new-yorker-photo-editor.html"""
import json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); GAME = os.path.dirname(HERE)
L = json.load(open(os.path.join(GAME, "landmarks.json")))
keep = [{k: l[k] for k in ("id", "name", "boro", "lat", "lon", "gone") if k in l} for l in L]
idx = open(os.path.join(GAME, "index.html")).read()
z = re.search(r"apertureZooms:\s*(\[[^\]]*\])", idx).group(1)
t = open(os.path.join(HERE, "photo-editor.template.html")).read()
t = t.replace("/*LANDMARKS*/[]", json.dumps(keep, ensure_ascii=False)).replace("/*ZOOMS*/[3.4, 2.5, 1.8, 1.25]", z)
open(os.path.join(HERE, "new-yorker-photo-editor.html"), "w").write(t)
print("editor built:", len(keep), "places, zooms", z)

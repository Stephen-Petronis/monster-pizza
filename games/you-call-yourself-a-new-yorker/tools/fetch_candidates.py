#!/usr/bin/env python3
"""Gathers several photo options per landmark for art direction.

Writes:
  build/new-yorker-photos.zip   <id>__<nn>.jpg photos (long side <= 2400) + manifest.json + README.txt
  ../tools/photo-candidates.json  the same manifest, kept in the repo so returned edits can be matched up

Option 01 is always the photo the game uses right now.
Run by .github/workflows/new-yorker-candidates.yml.
"""
import io, json, os, re, sys, time, zipfile
from PIL import Image, ImageOps
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fetch_photos import api, get, file_info, article_photos, commons_search, API, CAPI  # noqa

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.dirname(HERE)
PER = 6
SIDE = 2400
SKIP = re.compile(r"(logo|icon|map|seal|flag|symbol|plaque|diagram|location|svg|chart|graph|coat.of.arms|signature|portrait|tallest)", re.I)

def main():
    L = json.load(open(os.path.join(GAME, "landmarks.json")))
    cur = json.load(open(os.path.join(GAME, "photos.json")))
    os.makedirs("build", exist_ok=True)
    zpath = "build/new-yorker-photos.zip"
    man = []
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_STORED) as z:
        for lm in L:
            lid = lm["id"]; print("•", lid, flush=True)
            names = []
            if cur.get(lid, {}).get("file"): names.append(cur[lid]["file"])
            try: names += article_photos(lm["wiki"], 80)
            except Exception as e: print("  article fail", e)
            try: names += commons_search('"%s"' % lm["name"].replace("The ", ""), 40)
            except Exception as e: print("  search fail", e)
            seen, picked = set(), 0
            for n in names:
                if picked >= PER: break
                if n in seen or SKIP.search(n): continue
                seen.add(n)
                try:
                    fi = file_info(n, SIDE)
                    if not fi or not re.search(r"(jpeg|png|tiff|webp)", fi["mime"]): continue
                    minside = 900 if lm.get("gone") else 1600
                    if max(fi["w"], fi["h"]) < minside: continue
                    im = Image.open(io.BytesIO(get(fi["url"])))
                    im = ImageOps.exif_transpose(im).convert("RGB")
                    if max(im.size) > SIDE: im.thumbnail((SIDE, SIDE), Image.LANCZOS)
                    picked += 1
                    fname = "%s__%02d.jpg" % (lid, picked)
                    buf = io.BytesIO(); im.save(buf, "JPEG", quality=86, optimize=True)
                    z.writestr("photos/" + fname, buf.getvalue())
                    man.append({"file": fname, "id": lid, "name": lm["name"], "boro": lm["boro"], "lat": lm["lat"], "lon": lm["lon"],
                                "gone": lm.get("gone"), "current": picked == 1 and n == cur.get(lid, {}).get("file"),
                                "commons": fi["title"], "page": fi["page"], "author": fi["author"], "license": fi["license"],
                                "srcW": fi["w"], "srcH": fi["h"]})
                    time.sleep(0.2)
                except Exception as e:
                    print("  skip", n, e)
            print("  ", picked, "options", flush=True)
        z.writestr("manifest.json", json.dumps(man, indent=1, ensure_ascii=False))
        z.writestr("README.txt", README % (len(man), len(L)))
    json.dump(man, open(os.path.join(HERE, "photo-candidates.json"), "w"), indent=1, ensure_ascii=False)
    print("total photos:", len(man), "zip MB:", round(os.path.getsize(zpath) / 1e6, 1))

README = """You Call Yourself a New Yorker? — photo options for art direction
%d photos for %d locations, from Wikimedia Commons (free licenses; author + license for each one is in manifest.json).

File names are <location-id>__<option>.jpg — option 01 is the photo the game uses now.
Keep the file names as they are: that's how each photo stays tied to its place (and its latitude/longitude).

Open the photo editor (new-yorker-photo-editor.html), drop in the photos you like, art-direct them,
then hit Export and send the zip it makes back to Claude.
"""

if __name__ == "__main__":
    main()

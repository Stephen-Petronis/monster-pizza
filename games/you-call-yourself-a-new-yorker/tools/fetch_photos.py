#!/usr/bin/env python3
"""Downloads + optimizes the landmark photos for "You Call Yourself a New Yorker?".

Run by .github/workflows/new-yorker-photos.yml (needs Pillow).
Reads  ../landmarks.json
Writes ../photos/<id>.webp     crisp, phone-friendly copies (long side <= MAX_SIDE)
       ../photos.json          credits (author, license, Commons link), sizes, Wikipedia coordinates
       ../photos/_contact.jpg  contact sheet for reviewing every photo at a glance
       ../photos/_candidates-<id>.jpg + ../photos/_candidates.json
                               other photo options, for landmarks marked "review": true

A landmark can pin a specific Commons file with "file": "File:Something.jpg".
"""
import io, json, os, re, sys, time, urllib.parse, urllib.request
from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.dirname(HERE)
PHOTOS = os.path.join(GAME, "photos")
MAX_SIDE = 3200       # keeps zoomed-in crops sharp on retina phones
QUALITY = 80
UA = {"User-Agent": "monster-pizza-games/1.0 (https://github.com/Stephen-Petronis/monster-pizza; monster.pizza.games@gmail.com)"}
API = "https://en.wikipedia.org/w/api.php"
CAPI = "https://commons.wikimedia.org/w/api.php"

def get(url, tries=4):
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
                return r.read()
        except Exception as e:
            print("   retry", k, e, file=sys.stderr); time.sleep(4 * (k + 1))
    raise RuntimeError("failed " + url)

def api(base, **params):
    params.update(format="json", formatversion="2")
    return json.loads(get(base + "?" + urllib.parse.urlencode(params)))

def strip_html(s):
    s = re.sub(r"<[^>]+>", "", s or "")
    return re.sub(r"\s+", " ", s).strip()

def file_info(title, width=MAX_SIDE):
    j = api(CAPI, action="query", titles=title, prop="imageinfo",
            iiprop="url|size|mime|extmetadata", iiurlwidth=width)
    p = j["query"]["pages"][0]
    if "imageinfo" not in p: return None
    ii = p["imageinfo"][0]; md = ii.get("extmetadata", {})
    v = lambda k: strip_html(md.get(k, {}).get("value", ""))
    return {"title": p["title"], "url": ii.get("thumburl") or ii["url"], "orig": ii["url"],
            "w": ii["width"], "h": ii["height"], "mime": ii["mime"],
            "author": v("Artist")[:120], "license": v("LicenseShortName"), "licenseUrl": v("LicenseUrl"),
            "page": "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(p["title"].replace(" ", "_"))}

def lead_file(wiki):
    j = api(API, action="query", titles=wiki, redirects=1, prop="pageimages|coordinates", piprop="name", pilicense="free")
    p = j["query"]["pages"][0]
    c = (p.get("coordinates") or [None])[0]
    return ("File:" + p["pageimage"]) if p.get("pageimage") else None, (c["lat"], c["lon"]) if c else None

def article_photos(wiki, limit=40):
    j = api(API, action="query", titles=wiki, redirects=1, prop="images", imlimit=limit)
    names = [i["title"] for i in j["query"]["pages"][0].get("images", [])]
    return [n for n in names if re.search(r"\.(jpe?g|png|webp|tiff?)$", n, re.I) and not re.search(r"(logo|icon|map|seal|flag|symbol|commons-|wikimedia|location|diagram)", n, re.I)]

def load_image(url):
    im = Image.open(io.BytesIO(get(url)))
    im = ImageOps.exif_transpose(im)
    if im.mode not in ("RGB",): im = im.convert("RGB")
    return im

def save_webp(im, path):
    if max(im.size) > MAX_SIDE:
        im.thumbnail((MAX_SIDE, MAX_SIDE), Image.LANCZOS)
    im.save(path, "WEBP", quality=QUALITY, method=6)
    return im.size

def font(sz):
    for f in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"]:
        if os.path.exists(f): return ImageFont.truetype(f, sz)
    return ImageFont.load_default()

def sheet(items, path, cols=6, cell=(420, 300)):
    """items: list of (PIL image, caption)"""
    rows = (len(items) + cols - 1) // cols
    W, H = cols * cell[0], rows * (cell[1] + 44)
    out = Image.new("RGB", (W, H), (24, 24, 26)); d = ImageDraw.Draw(out); f = font(17)
    for k, (im, cap) in enumerate(items):
        x, y = (k % cols) * cell[0], (k // cols) * (cell[1] + 44)
        t = im.copy(); t.thumbnail((cell[0] - 8, cell[1] - 8))
        out.paste(t, (x + (cell[0] - t.width) // 2, y + 4 + (cell[1] - 8 - t.height) // 2))
        for i, line in enumerate(cap.split("\n")[:2]):
            d.text((x + 6, y + cell[1] + 2 + i * 20), line[:44], fill=(240, 220, 120) if i == 0 else (200, 200, 200), font=f)
    out.save(path, "JPEG", quality=82)

def main():
    os.makedirs(PHOTOS, exist_ok=True)
    L = json.load(open(os.path.join(GAME, "landmarks.json")))
    manifest, contact, cands = {}, [], {}
    for lm in L:
        lid = lm["id"]; print("•", lid)
        try:
            title, coords = lead_file(lm["wiki"])
            if lm.get("file"): title = lm["file"]
            if not title: print("   no photo"); continue
            info = file_info(title)
            if not info: print("   no info"); continue
            im = load_image(info["url"])
            w, h = save_webp(im, os.path.join(PHOTOS, lid + ".webp"))
            manifest[lid] = {"src": "photos/%s.webp" % lid, "w": w, "h": h, "srcW": info["w"], "srcH": info["h"],
                             "file": info["title"], "page": info["page"], "author": info["author"],
                             "license": info["license"], "licenseUrl": info["licenseUrl"],
                             "lat": coords[0] if coords else None, "lon": coords[1] if coords else None}
            flag = " LOW-RES" if info["w"] < 2000 and info["h"] < 2000 else ""
            contact.append((im, "%s%s\n%dx%d %s" % (lm["name"], flag, info["w"], info["h"], info["title"][5:40])))
            if lm.get("review"):
                opts = []
                for n in article_photos(lm["wiki"])[:18]:
                    try:
                        fi = file_info(n, 640)
                        if not fi or fi["w"] < 1200: continue
                        opts.append((load_image(fi["url"]), "%s\n%dx%d" % (fi["title"][5:44], fi["w"], fi["h"])))
                        cands.setdefault(lid, []).append({"file": fi["title"], "w": fi["w"], "h": fi["h"]})
                    except Exception as e: print("   cand fail", n, e)
                if opts: sheet(opts, os.path.join(PHOTOS, "_candidates-%s.jpg" % lid), cols=4)
            time.sleep(0.5)
        except Exception as e:
            print("   FAILED", e, file=sys.stderr)
    json.dump(manifest, open(os.path.join(GAME, "photos.json"), "w"), indent=1, ensure_ascii=False)
    if contact: sheet(contact, os.path.join(PHOTOS, "_contact.jpg"))
    json.dump(cands, open(os.path.join(PHOTOS, "_candidates.json"), "w"), indent=1)
    print("photos:", len(manifest), "of", len(L))

if __name__ == "__main__":
    main()

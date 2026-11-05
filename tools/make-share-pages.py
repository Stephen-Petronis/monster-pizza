#!/usr/bin/env python3
"""Build link-preview pictures and share pages for every game in games.js.

For each game it writes:
  share/<id>.jpg            1200x630 preview picture (the cabinet on the arcade wall)
  play/<id>/index.html      a tiny page with that picture as its link preview,
                            which sends visitors straight to the game in the arcade
Plus share/monster-pizza.jpg, the preview for the main arcade link.

Run it from the repo folder after adding a game or a new cabinet:
  python3 tools/make-share-pages.py
Needs Python 3 with Pillow (pip install pillow) and Node (to read games.js).
"""
import html, json, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

SITE = "https://stephen-petronis.github.io/monster-pizza/"
W, H = 1200, 630
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

cfg = json.loads(subprocess.check_output(
    ["node", "-e", "global.window={};require('./games.js');console.log(JSON.stringify(window.MONSTER_PIZZA))"]))
games = cfg["games"]


def font(size):
    for f in ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/Library/Fonts/Arial Bold.ttf"]:
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


def wall():
    """The arcade wall: the plain wall tile repeated, with the floor strip along the bottom."""
    bg = Image.new("RGB", (W, H))
    tile = Image.open("walls/wall-plain.jpg").convert("RGB")
    tw = round(tile.width * H / tile.height)
    tile = tile.resize((tw, H), Image.LANCZOS)
    for x in range(0, W, tw):
        bg.paste(tile, (x, 0))
    if cfg.get("floor") and os.path.exists(cfg["floor"]):
        top = round(H * cfg.get("floorTop", 84) / 100)
        fl = Image.open(cfg["floor"]).convert("RGB")
        fw = round(fl.width * (H - top) / fl.height)
        fl = fl.resize((fw, H - top), Image.LANCZOS)
        for x in range(0, W, fw):
            bg.paste(fl, (x, top))
    return bg


def shadow(img, cx, bottom, width):
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse([cx - width // 2, bottom - 18, cx + width // 2, bottom + 14], fill=(20, 8, 4, 120))
    img.alpha_composite(sh)


def paste_cabinet(img, path, cx, bottom, height):
    cab = Image.open(path).convert("RGBA")
    w = round(cab.width * height / cab.height)
    cab = cab.resize((w, height), Image.LANCZOS)
    shadow(img, cx, bottom, int(w * 1.1))
    img.alpha_composite(cab, (cx - w // 2, bottom - height))
    return w


def built_in_cabinet(img, g, cx, bottom, height):
    """A simple drawn cabinet for games that don't have cabinet art yet, with their GIF on the screen."""
    d = ImageDraw.Draw(img)
    w = round(height * .56)
    x0, y0 = cx - w // 2, bottom - height
    ink, col = (31, 21, 18), g.get("color", "#2f7fd0")
    shadow(img, cx, bottom, int(w * 1.1))
    d.rounded_rectangle([x0, y0, x0 + w, bottom], 18, fill=col, outline=ink, width=8)
    # marquee with the title
    m = [x0 + 22, y0 + 20, x0 + w - 22, y0 + 20 + height * .15]
    d.rounded_rectangle(m, 10, fill=(244, 182, 62), outline=ink, width=6)
    size = 44
    while size > 14 and d.textlength(g["title"], font=font(size)) > (m[2] - m[0] - 20):
        size -= 2
    d.text(((m[0] + m[2]) / 2, (m[1] + m[3]) / 2), g["title"], fill=ink, font=font(size), anchor="mm")
    # screen
    sx0, sy0 = x0 + 34, int(m[3] + 26)
    sw, sh = w - 68, int((w - 68) * .75)
    d.rounded_rectangle([sx0 - 10, sy0 - 10, sx0 + sw + 10, sy0 + sh + 10], 14, fill=(18, 12, 10), outline=ink, width=6)
    if g.get("screen") and os.path.exists(g["screen"]):
        fr = Image.open(g["screen"])
        try:
            fr.seek(min(10, getattr(fr, "n_frames", 1) - 1))
        except EOFError:
            pass
        fr = fr.convert("RGB")
        r = max(sw / fr.width, sh / fr.height)
        fr = fr.resize((round(fr.width * r), round(fr.height * r)), Image.LANCZOS)
        fr = fr.crop(((fr.width - sw) // 2, (fr.height - sh) // 2, (fr.width - sw) // 2 + sw, (fr.height - sh) // 2 + sh))
        img.paste(fr, (sx0, sy0))
    # control panel and coin door
    py = sy0 + sh + 30
    d.rounded_rectangle([x0 + 14, py, x0 + w - 14, py + 46], 8, fill=(42, 32, 35), outline=ink, width=6)
    for k, c in enumerate([(214, 69, 45), (244, 182, 62), (89, 195, 255)]):
        bx = x0 + w * (.3 + k * .2)
        d.ellipse([bx - 12, py + 11, bx + 12, py + 35], fill=c, outline=ink, width=4)
    d.rounded_rectangle([cx - 46, py + 76, cx + 46, py + 150], 8, fill=(58, 48, 54), outline=ink, width=5)
    d.rectangle([cx - 5, py + 92, cx + 5, py + 120], fill=(210, 74, 47))


def add_logo(img, width=250):
    if os.path.exists("art/logo-small.webp"):
        lg = Image.open("art/logo-small.webp").convert("RGBA")
        lg = lg.resize((width, round(lg.height * width / lg.width)), Image.LANCZOS)
        img.alpha_composite(lg, (26, 22))


def save(img, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.convert("RGB").save(path, quality=86, optimize=True, progressive=True)


def share_page(g):
    gid, title = g["id"], g["title"]
    url = SITE + "play/" + gid + "/"
    img = SITE + "share/" + gid + ".jpg"
    dest = "../../#" + gid
    t, desc = html.escape(title + " · Monster Pizza Arcade"), html.escape(g.get("blurb", "Play it at the Monster Pizza Arcade."))
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{t}</title>
<meta name="description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Monster Pizza Arcade">
<meta property="og:title" content="{t}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta property="og:image:width" content="{W}">
<meta property="og:image:height" content="{H}">
<meta property="og:image:alt" content="{html.escape(title)} arcade cabinet at Monster Pizza">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="{img}">
<link rel="canonical" href="{url}">
<meta http-equiv="refresh" content="0; url={dest}">
<style>body{{margin:0;min-height:100vh;display:grid;place-items:center;background:#2a2147;color:#fbf0d6;font:18px system-ui,sans-serif}}a{{color:#f4b63e}}</style>
</head>
<body>
<p>Heading to <a href="{dest}">{html.escape(title)}</a> at the Monster Pizza Arcade&hellip;</p>
<script>location.replace({json.dumps(dest)});</script>
</body>
</html>
"""


# per-game pictures and pages
for g in games:
    img = wall().convert("RGBA")
    add_logo(img)
    if g.get("cabinet") and os.path.exists(g["cabinet"]):
        paste_cabinet(img, g["cabinet"], W // 2, H - 14, H - 36)
    else:
        built_in_cabinet(img, g, W // 2, H - 14, H - 36)
    save(img, f"share/{g['id']}.jpg")
    os.makedirs(f"play/{g['id']}", exist_ok=True)
    with open(f"play/{g['id']}/index.html", "w") as f:
        f.write(share_page(g))
    print("made", g["id"])

# the main arcade preview: big logo over a row of cabinets
img = wall().convert("RGBA")
cabs = [g for g in games if g.get("cabinet") and os.path.exists(g["cabinet"])][:6]
n = len(cabs)
for k, g in enumerate(cabs):
    cx = round(W * (k + .5) / n)
    paste_cabinet(img, g["cabinet"], cx, H - 12, 300)
if os.path.exists("art/logo.webp"):
    lg = Image.open("art/logo.webp").convert("RGBA")
    lw = 620
    lg = lg.resize((lw, round(lg.height * lw / lg.width)), Image.LANCZOS)
    img.alpha_composite(lg, ((W - lw) // 2, 8))
save(img, "share/monster-pizza.jpg")
print("made monster-pizza preview")

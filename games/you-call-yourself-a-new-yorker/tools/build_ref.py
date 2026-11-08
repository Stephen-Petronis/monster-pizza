#!/usr/bin/env python3
"""Builds the map reference files for "You Call Yourself a New Yorker?".

Run by the GitHub Action in .github/workflows/new-yorker-map-data.yml (or by hand).
Writes, next to index.html:
  nyc-ref.json        unlabeled reference lines: highways, big streets, waterways (OpenStreetMap)
  nyc-boroughs.json   the five-borough land shapes (NYC Dept. of City Planning, via Code for America)
"""
import json, os, sys, time, urllib.parse, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
BBOX = "40.485,-74.285,40.930,-73.680"  # south,west,north,east

NAMED = ["Broadway","Atlantic Avenue","Flatbush Avenue","Queens Boulevard","Grand Concourse","Northern Boulevard",
 "Ocean Parkway","Eastern Parkway","Fordham Road","East Fordham Road","West Fordham Road","Canal Street","Houston Street",
 "East Houston Street","West Houston Street","West 42nd Street","East 42nd Street","West 125th Street","East 125th Street",
 "Fifth Avenue","Park Avenue","Delancey Street","Hylan Boulevard","Richmond Avenue","Victory Boulevard","Linden Boulevard",
 "Kings Highway","Bedford Avenue","Fourth Avenue","4th Avenue","Roosevelt Avenue","Woodhaven Boulevard","Cross Bay Boulevard",
 "Pelham Parkway","Bruckner Boulevard","Southern Boulevard","Jamaica Avenue","Hillside Avenue","Myrtle Avenue",
 "Coney Island Avenue","Nostrand Avenue","Utica Avenue","Church Avenue","Lexington Avenue","Amsterdam Avenue",
 "Seventh Avenue","Eighth Avenue","7th Avenue","8th Avenue","5th Avenue"]

QUERY = f"""[out:json][timeout:180];
(
  way["highway"~"^(motorway|trunk)$"]({BBOX});
  way["highway"~"^(primary|secondary|tertiary)$"]["name"~"^({'|'.join(NAMED)})$"]({BBOX});
  way["waterway"~"^(river|canal|tidal_channel)$"]({BBOX});
);
out geom qt;"""

MIRRORS = ["https://overpass-api.de/api/interpreter",
           "https://overpass.private.coffee/api/interpreter",
           "https://maps.mail.ru/osm/tools/overpass/api/interpreter"]

BOROUGH_URLS = ["https://raw.githubusercontent.com/codeforamerica/click_that_hood/main/public/data/new-york-city-boroughs.geojson",
                "https://raw.githubusercontent.com/codeforamerica/click_that_hood/master/public/data/new-york-city-boroughs.geojson"]

UA = {"User-Agent": "monster-pizza-games/1.0 (github.com/Stephen-Petronis/monster-pizza)"}

def get(url, data=None, tries=2):
    last = None
    for _ in range(tries):
        try:
            req = urllib.request.Request(url, data=data, headers=UA)
            with urllib.request.urlopen(req, timeout=240) as r:
                return r.read()
        except Exception as e:  # noqa
            last = e; print("  failed:", url, e, file=sys.stderr); time.sleep(10)
    raise last

def overpass():
    body = urllib.parse.urlencode({"data": QUERY}).encode()
    for m in MIRRORS:
        try:
            return json.loads(get(m, body))
        except Exception:
            continue
    raise SystemExit("all Overpass mirrors failed")

def simplify(flat, tol=0.00002):
    """Douglas-Peucker on a flat [lon,lat,lon,lat...] list (tol in degrees, ~2 m)."""
    n = len(flat)//2
    if n < 3: return flat
    keep = [False]*n; keep[0] = keep[-1] = True
    stack = [(0, n-1)]
    while stack:
        a, b = stack.pop()
        ax, ay, bx, by = flat[2*a], flat[2*a+1], flat[2*b], flat[2*b+1]
        dx, dy = bx-ax, by-ay; L = (dx*dx+dy*dy) or 1e-18
        best, bi = -1, -1
        for k in range(a+1, b):
            px, py = flat[2*k], flat[2*k+1]
            t = max(0, min(1, ((px-ax)*dx+(py-ay)*dy)/L))
            d = (ax+t*dx-px)**2 + (ay+t*dy-py)**2
            if d > best: best, bi = d, k
        if bi >= 0 and best > tol*tol:
            keep[bi] = True; stack += [(a, bi), (bi, b)]
    out = []
    for k in range(n):
        if keep[k]: out += [flat[2*k], flat[2*k+1]]
    return out

def flat_of(geom):
    flat, last = [], None
    for p in geom:
        if not p: continue
        pt = (round(p["lon"], 5), round(p["lat"], 5))
        if pt != last: flat += pt; last = pt
    return flat

def overpass_q(q):
    body = urllib.parse.urlencode({"data": q}).encode()
    for m in MIRRORS:
        try: return json.loads(get(m, body))
        except Exception: continue
    raise SystemExit("all Overpass mirrors failed")

def join_rings(ways):
    """Join open way pieces (lists of (lon,lat)) into closed rings."""
    rings, pieces = [], [list(w) for w in ways if len(w) >= 2]
    while pieces:
        cur = pieces.pop()
        changed = True
        while cur[0] != cur[-1] and changed:
            changed = False
            for i, w in enumerate(pieces):
                if w[0] == cur[-1]: cur += w[1:]
                elif w[-1] == cur[-1]: cur += w[::-1][1:]
                elif w[-1] == cur[0]: cur = w + cur[1:]
                elif w[0] == cur[0]: cur = w[::-1] + cur[1:]
                else: continue
                pieces.pop(i); changed = True; break
        if len(cur) >= 4: rings.append(cur)
    return rings

def write(name, obj):
    with open(os.path.join(OUT, name), "w") as f:
        json.dump(obj, f, separators=(",", ":"))
    print("wrote", name, os.path.getsize(os.path.join(OUT, name)), "bytes")

def build_extras():
    # ---- parks (always shown) ----
    j = overpass_q(f"""[out:json][timeout:180];
(way["leisure"~"^(park|nature_reserve|garden|golf_course)$"]({BBOX});
 relation["leisure"~"^(park|nature_reserve|golf_course)$"]({BBOX}););
out geom qt;""")
    parks = []
    for el in j.get("elements", []):
        if el["type"] == "way" and el.get("geometry"):
            g = el["geometry"]
            if g[0] == g[-1] and len(g) >= 4:
                f = simplify(flat_of(g), 0.00001)
                if len(f) >= 8: parks.append(f)
        elif el["type"] == "relation":
            outers = [[(round(p["lon"],5), round(p["lat"],5)) for p in m.get("geometry") or [] if p]
                      for m in el.get("members", []) if m.get("type") == "way" and m.get("role") in ("outer", "")]
            for r in join_rings(outers):
                f = simplify([c for pt in r for c in pt], 0.00001)
                if len(f) >= 8: parks.append(f)
    print("parks:", len(parks))
    if parks: write("nyc-parks.json", {"parks": parks, "credit": "© OpenStreetMap contributors (ODbL)"})
    time.sleep(5)

    # ---- more roads (helper) ----
    j = overpass_q(f"""[out:json][timeout:180];
way["highway"~"^(secondary|tertiary)$"]({BBOX});
out geom qt;""")
    more = []
    for el in j.get("elements", []):
        if el.get("geometry"):
            f = simplify(flat_of(el["geometry"]))
            if len(f) >= 4: more.append(f)
    print("more roads:", len(more))
    if more: write("nyc-roads2.json", {"road2": more, "credit": "© OpenStreetMap contributors (ODbL)"})

    # ---- subway lines (helper) — NYC DoITT subway line shapes ----
    for u in SUBWAY_URLS:
        try:
            g = json.loads(get(u))
            lines = {}
            for f in g.get("features", []):
                props = {k.lower(): v for k, v in (f.get("properties") or {}).items()}
                sym = str(props.get("rt_symbol") or props.get("name") or "S").strip()[:1].upper()
                geom = f.get("geometry") or {}
                parts = [geom["coordinates"]] if geom.get("type") == "LineString" else geom.get("coordinates", []) if geom.get("type") == "MultiLineString" else []
                for part in parts:
                    flat = []
                    for x, y in (pt[:2] for pt in part): flat += [round(x, 5), round(y, 5)]
                    flat = simplify(flat)
                    if len(flat) >= 4: lines.setdefault(sym, []).append(flat)
            if lines:
                print("subway trunks:", {k: len(v) for k, v in lines.items()})
                write("nyc-subway.json", {"lines": lines, "credit": "NYC DoITT subway lines"})
                break
        except Exception as e:
            print("  subway source failed:", e, file=sys.stderr)

SUBWAY_URLS = [
    "https://services6.arcgis.com/IX0rbbPRMd0YfCJN/ArcGIS/rest/services/NYC_DoITT_Subway_Line/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=geojson",
    "https://services3.arcgis.com/GVgbJbqm8hXASVYi/ArcGIS/rest/services/Subway_Lines_NYC/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=geojson",
    "https://services5.arcgis.com/cuQhNeNcUrgLmYGD/ArcGIS/rest/services/NYC_Subway_Lines/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=geojson",
]

def main():
    j = overpass()
    ref = {"hwy": [], "road": [], "water": []}
    for el in j.get("elements", []):
        g = el.get("geometry")
        if el.get("type") != "way" or not g or len(g) < 2:
            continue
        flat, last = [], None
        for p in g:
            pt = (round(p["lon"], 5), round(p["lat"], 5))
            if pt != last:
                flat += pt; last = pt
        flat = simplify(flat)
        if len(flat) < 4:
            continue
        t = el.get("tags", {})
        if "waterway" in t: ref["water"].append(flat)
        elif t.get("highway") in ("motorway", "trunk"): ref["hwy"].append(flat)
        else: ref["road"].append(flat)
    print("lines:", {k: len(v) for k, v in ref.items()})
    if not ref["hwy"] or not ref["road"]:
        raise SystemExit("suspiciously empty result, not writing")
    ref["credit"] = "© OpenStreetMap contributors (ODbL)"
    with open(os.path.join(OUT, "nyc-ref.json"), "w") as f:
        json.dump(ref, f, separators=(",", ":"))

    for u in BOROUGH_URLS:
        try:
            b = json.loads(get(u))
            if b.get("features"):
                with open(os.path.join(OUT, "nyc-boroughs.json"), "w") as f:
                    json.dump(b, f, separators=(",", ":"))
                print("boroughs:", len(b["features"]))
                break
        except Exception:
            continue

if __name__ == "__main__":
    main()
    time.sleep(5)
    build_extras()

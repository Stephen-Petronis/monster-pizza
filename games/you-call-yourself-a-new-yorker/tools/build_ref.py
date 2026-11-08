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

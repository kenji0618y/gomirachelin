# -*- coding: utf-8 -*-
"""data/map-facilities.json を静的地図へ反映し、基本整合性を検査する。"""

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "map-facilities.json"
MAP_PATH = ROOT / "map" / "index.html"
PATTERN = re.compile(r"ALL=uniqueFacilities\((\[.*?\])\);", re.S)
GEO_PATTERN = re.compile(r"var PREF_GEO = (\{.*?\});\s*\n", re.S)


def valid_position(item):
    lat, lng = item.get("lat"), item.get("lng")
    return (
        isinstance(lat, (int, float))
        and isinstance(lng, (int, float))
        and 20 <= lat <= 46
        and 122 <= lng <= 154
    )


def ring_contains(lng, lat, ring):
    inside = False
    previous = len(ring) - 1
    for current, (x_current, y_current) in enumerate(ring):
        x_previous, y_previous = ring[previous]
        crosses = (y_current > lat) != (y_previous > lat)
        if crosses and lng < (x_previous - x_current) * (lat - y_current) / (y_previous - y_current) + x_current:
            inside = not inside
        previous = current
    return inside


def geometry_contains(lng, lat, geometry):
    polygons = geometry["coordinates"] if geometry["type"] == "MultiPolygon" else [geometry["coordinates"]]
    for polygon in polygons:
        outer = ring_contains(lng, lat, polygon[0])
        holes = any(ring_contains(lng, lat, hole) for hole in polygon[1:])
        if outer and not holes:
            return True
    return False


def validate(rows, prefecture_geo):
    errors = []
    features = {feature["properties"]["P"]: feature for feature in prefecture_geo["features"]}
    source_rows = [item.get("sourceRow") for item in rows]
    if len(source_rows) != len(set(source_rows)):
        errors.append("sourceRow が重複しています")
    for item in rows:
        for key in ("name", "pref", "sourceRow", "lat", "lng"):
            if key not in item:
                errors.append(f"必須項目がありません: {item.get('name', '?')} / {key}")
        has_lat = item.get("lat") not in (None, 0)
        has_lng = item.get("lng") not in (None, 0)
        if has_lat != has_lng:
            errors.append(f"緯度・経度の片方だけがあります: {item.get('name')}")
        if has_lat and not valid_position(item):
            errors.append(f"日本域外の座標です: {item.get('name')} / {item.get('lat')},{item.get('lng')}")
        if has_lat and valid_position(item):
            feature = features.get(item.get("pref"))
            if not feature or not geometry_contains(item["lng"], item["lat"], feature["geometry"]):
                errors.append(f"座標が登録都道府県の外です: {item.get('name')} / {item.get('pref')}")
    if errors:
        raise RuntimeError("\n".join(errors))


def render(source, rows):
    compact = json.dumps(rows, ensure_ascii=False, separators=(",", ":"))
    replacement = f"ALL=uniqueFacilities({compact});"
    # callable replacement avoids re.sub interpreting JSON escapes such as \n
    result, count = PATTERN.subn(lambda _match: replacement, source, count=1)
    if count != 1:
        raise RuntimeError("map/index.html の施設データを検出できません")
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="HTMLが正本と同期しているかだけ確認")
    args = parser.parse_args()

    old = MAP_PATH.read_text(encoding="utf-8")
    geo_match = GEO_PATTERN.search(old)
    if not geo_match:
        raise RuntimeError("map/index.html の都道府県境界を検出できません")
    prefecture_geo = json.loads(geo_match.group(1))
    rows = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    validate(rows, prefecture_geo)
    new = render(old, rows)
    coordinates = sum(valid_position(item) for item in rows)

    if args.check:
        if new != old:
            raise SystemExit("NG: map/index.html が data/map-facilities.json と同期していません")
        print(f"OK: facilities={len(rows)}, coordinates={coordinates}, missing={len(rows)-coordinates}")
        return

    MAP_PATH.write_text(new, encoding="utf-8")
    print(f"UPDATED: facilities={len(rows)}, coordinates={coordinates}, missing={len(rows)-coordinates}")


if __name__ == "__main__":
    main()

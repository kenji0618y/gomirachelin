# -*- coding: utf-8 -*-
"""現在URLと旧URL履歴の重複・転送先を検査する。"""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ACTIVE_PATH = ROOT / "data" / "urls.json"
HISTORY_PATH = ROOT / "data" / "url-history.json"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def duplicates(values):
    seen = set()
    return sorted({value for value in values if value in seen or seen.add(value)})


active = load_json(ACTIVE_PATH)
history = load_json(HISTORY_PATH)["entries"]
active_slugs = [item["slug"] for item in active]
history_slugs = [item["slug"] for item in history]

errors = []
for label, values in (("現在URL", active_slugs), ("履歴URL", history_slugs)):
    found = duplicates(values)
    if found:
        errors.append(f"{label}内の重複: {', '.join(found)}")

overlap = sorted(set(active_slugs) & set(history_slugs))
if overlap:
    errors.append(f"現在URLと履歴URLの重複: {', '.join(overlap)}")

active_set = set(active_slugs)
for item in history:
    slug = item["slug"]
    canonical = item.get("canonicalSlug")
    if canonical not in active_set:
        errors.append(f"履歴 {slug} の転送先が現在URLにない: {canonical}")
    if not (ROOT / slug / "index.html").is_file():
        errors.append(f"履歴URLの転送ページがない: {slug}/index.html")
    if canonical and not (ROOT / canonical / "index.html").is_file():
        errors.append(f"正式ページがない: {canonical}/index.html")

if errors:
    raise SystemExit("\n".join(errors))

print(f"OK: active={len(active)}, history={len(history)}, overlap=0")

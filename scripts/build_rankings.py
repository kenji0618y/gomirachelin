#!/usr/bin/env python3
"""Build the two static ranking pages from data/rankings.json."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "rankings.json"
RANKING_PATH = ROOT / "ランキング" / "index.html"
AXES_PATH = ROOT / "10項目別ランキング" / "index.html"

AXES = [
    {"key": "a1", "id": "s1", "en": "SAUNA", "jp": "①サウナ", "description": "温度・湿度・広さ・熱の質。"},
    {"key": "a2", "id": "s2", "en": "COLD BATH", "jp": "②水風呂", "description": "水温・深さ・広さ。冷たさの質。"},
    {"key": "a3", "id": "s3", "en": "REST", "jp": "③休憩", "description": "外気浴・内気浴の快適さ。"},
    {"key": "a4", "id": "s4", "en": "FLOW", "jp": "④動線", "description": "サウナ→水→休憩の流れ。"},
    {"key": "a5", "id": "s5", "en": "LOYLY", "jp": "⑤ロウリュ", "description": "ロウリュ・アウフグースの提供内容と質。"},
    {"key": "a6", "id": "s6", "en": "BATH", "jp": "⑥スパ内施設", "description": "浴室内の湯・設備の充実。"},
    {"key": "a7", "id": "s7", "en": "LOUNGE", "jp": "⑦スパ外施設", "description": "浴室外の館内休憩・食事施設の充実。"},
    {"key": "a8", "id": "s8", "en": "CLEANLINESS", "jp": "⑧清潔さ", "description": "築年数と切り離した清掃・衛生。"},
    {"key": "a9", "id": "s9", "en": "UNIQUENESS", "jp": "⑨独自性", "description": "他にない体験と個性。"},
    {"key": "a10", "id": "s10", "en": "HOSPITALITY", "jp": "⑩ホスピタリティ", "description": "接客と、また来たくなる温かさ。"},
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def bootstrap() -> None:
    """Create the first master file from the currently published static pages."""
    ranking = read_text(RANKING_PATH)
    match = re.search(r"var FACILITIES = (\[.*?\]);\s*\n", ranking, re.S)
    if not match:
        raise RuntimeError("ランキングページのFACILITIESを検出できません")
    facilities = json.loads(match.group(1))
    by_name = {item["name"]: item for item in facilities}

    axes_html = read_text(AXES_PATH)
    for number, axis in enumerate(AXES, start=1):
        block_match = re.search(
            rf'<div class="axis-block" id="axis-s{number}">(.*?)<p class="more-note num">',
            axes_html,
            re.S,
        )
        if not block_match:
            raise RuntimeError(f"axis-s{number}を検出できません")
        rows = [line.strip() for line in block_match.group(1).splitlines() if 'class="rank-row' in line]
        if not rows:
            raise RuntimeError(f"axis-s{number}に順位がありません")
        for row in rows:
            name_match = re.search(r'class="name-link"[^>]*>(.*?) <span class="go-arrow"', row)
            if not name_match:
                name_match = re.search(r'class="plain-name">(.*?)</span>', row)
            score_match = re.search(r'class="score num">([0-9.]+)', row)
            if not name_match or not score_match:
                raise RuntimeError(f"axis-s{number}の行を解析できません: {row[:120]}")
            name = html.unescape(re.sub(r"<[^>]+>", "", name_match.group(1)))
            if name not in by_name:
                raise RuntimeError(f"通常ランキングにない施設です: {name}")
            by_name[name].setdefault("axes", {})[axis["key"]] = float(score_match.group(1))

    counts = {axis["key"]: sum(axis["key"] in item.get("axes", {}) for item in facilities) for axis in AXES}
    if len(set(counts.values())) != 1:
        raise RuntimeError(f"10項目の施設数が一致しません: {counts}")

    payload = {"schemaVersion": 1, "axes": AXES, "facilities": facilities}
    DATA_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"created {DATA_PATH.relative_to(ROOT)}: facilities={len(facilities)}, scored={next(iter(counts.values()))}")


def load_data() -> dict:
    payload = json.loads(read_text(DATA_PATH))
    if payload.get("schemaVersion") != 1:
        raise RuntimeError("未対応のrankings.jsonスキーマです")
    facilities = payload.get("facilities")
    if not isinstance(facilities, list) or not facilities:
        raise RuntimeError("rankings.jsonに施設データがありません")
    return payload


def facility_href(item: dict) -> str | None:
    slug = item.get("slug")
    return f"/{quote(str(slug), safe='')}/" if slug else None


def render_row(item: dict, score: float, position: int) -> str:
    first = " rank-first" if position == 1 else ""
    href = facility_href(item)
    linked = " has-link" if href else ""
    crown = '<span class="pos-crown">★</span>' if position == 1 else ""
    name = html.escape(str(item["name"]))
    place = html.escape(str(item.get("pref") or ""))
    if href:
        label = f'<a class="name-link" href="{href}">{name} <span class="go-arrow">›</span></a>'
    else:
        label = f'<span class="plain-name">{name}</span>'
    closed = '<span class="closed-tag">閉店</span>' if item.get("closed") else ""
    return (
        f'      <div class="rank-row{first}{linked}"><div class="pos num">{position}{crown}</div>'
        f'<div class="info"><div class="nm">{label}{closed}</div><div class="pl">{place}</div></div>'
        f'<div class="score num">{float(score):.1f}<span class="s">/10</span></div></div>'
    )


def build_ranking_page(source: str, facilities: list[dict]) -> str:
    public_items = [{key: value for key, value in item.items() if key != "axes"} for item in facilities]
    compact = json.dumps(public_items, ensure_ascii=False, separators=(",", ":"))
    result, count = re.subn(
        r"var FACILITIES = \[.*?\];\s*\n",
        f"var FACILITIES = {compact};\n",
        source,
        count=1,
        flags=re.S,
    )
    if count != 1:
        raise RuntimeError("ランキングページのFACILITIESを更新できません")
    return result


def build_axes_page(source: str, axes: list[dict], facilities: list[dict]) -> str:
    result = source
    for number, axis in enumerate(axes, start=1):
        key = axis["key"]
        axis_id = html.escape(str(axis["id"]))
        axis_en = html.escape(str(axis["en"]))
        axis_jp = html.escape(str(axis["jp"]))
        axis_description = html.escape(str(axis["description"]))

        card_pattern = rf'<a class="score-card" href="#axis-{re.escape(axis_id)}">.*?</a>'
        card = (
            f'<a class="score-card" href="#axis-{axis_id}"><div class="no">{number:02d}</div>'
            f'<div class="en">{axis_en}</div><div class="jp">{axis_jp}</div></a>'
        )
        result, card_count = re.subn(card_pattern, card, result, count=1)
        if card_count != 1:
            raise RuntimeError(f"axis-s{number}の項目カードを更新できません")

        header_pattern = (
            rf'(<div class="axis-block" id="axis-{re.escape(axis_id)}">\s*'
            rf'<div class="axis-head">\s*)'
            rf'<div class="en num">.*?</div>\s*<div class="jp">.*?</div>\s*'
            rf'<div class="desc">.*?</div>'
        )
        def replace_header(match: re.Match[str]) -> str:
            return (
                f'{match.group(1)}<div class="en num">{axis_en}</div>\n'
                f'      <div class="jp">{axis_jp}</div>\n'
                f'      <div class="desc">{axis_description}</div>'
            )

        result, header_count = re.subn(header_pattern, replace_header, result, count=1, flags=re.S)
        if header_count != 1:
            raise RuntimeError(f"axis-s{number}の見出しを更新できません")

        scored = [(index, item) for index, item in enumerate(facilities) if key in item.get("axes", {})]
        scored.sort(key=lambda pair: (-float(pair[1]["axes"][key]), pair[0]))
        rows = "\n".join(render_row(item, item["axes"][key], position) for position, (_, item) in enumerate(scored, 1))
        pattern = (
            rf'(<div class="axis-block" id="axis-s{number}">.*?'
            rf'<div class="rank-list" data-metric="axis">).*?'
            rf'(</div>\s*<p class="more-note num">全 \d+ 施設</p>)'
        )
        def replace_block(match: re.Match[str]) -> str:
            return f'{match.group(1)}\n{rows}\n    </div>\n    <p class="more-note num">全 {len(scored)} 施設</p>'

        result, count = re.subn(pattern, replace_block, result, count=1, flags=re.S)
        if count != 1:
            raise RuntimeError(f"axis-s{number}の順位一覧を更新できません")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bootstrap", action="store_true", help="現在のHTMLから初回マスターデータを作る")
    parser.add_argument("--check", action="store_true", help="生成結果との差がないか確認する")
    args = parser.parse_args()

    if args.bootstrap:
        if DATA_PATH.exists():
            raise RuntimeError("rankings.jsonは既にあります。上書きしません")
        bootstrap()

    payload = load_data()
    facilities = payload["facilities"]
    axes = payload.get("axes") or AXES
    ranking_old = read_text(RANKING_PATH)
    axes_old = read_text(AXES_PATH)
    ranking_new = build_ranking_page(ranking_old, facilities)
    axes_new = build_axes_page(axes_old, axes, facilities)

    if args.check:
        changed = []
        if ranking_new != ranking_old:
            changed.append(str(RANKING_PATH.relative_to(ROOT)))
        if axes_new != axes_old:
            changed.append(str(AXES_PATH.relative_to(ROOT)))
        if changed:
            print("更新が必要: " + ", ".join(changed), file=sys.stderr)
            return 1
        print(f"OK: facilities={len(facilities)}, scored={sum(bool(item.get('axes')) for item in facilities)}")
        return 0

    RANKING_PATH.write_text(ranking_new, encoding="utf-8")
    AXES_PATH.write_text(axes_new, encoding="utf-8")
    print(f"updated ranking pages: facilities={len(facilities)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)

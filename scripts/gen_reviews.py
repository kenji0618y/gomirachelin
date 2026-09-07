# -*- coding: utf-8 -*-
"""レビュー一覧ページ（reviews/index.html）を作り直すスクリプト。

使い方（サイトのフォルダで）:
    python3 scripts/gen_reviews.py

データの元:
  - ランキング/index.html の中の FACILITIES（施設名・スコア・料金・slug）
  - data/urls.json（記事の公開日とタイトル）
記事フォルダ（<slug>/index.html）が実際にあるものだけを一覧に載せます。
"""
import re, json, os, html

# このスクリプトは <サイトのフォルダ>/scripts/ に置く想定。ひとつ上がサイトのルート。
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

src = open(os.path.join(ROOT, "ランキング/index.html"), encoding="utf-8").read()
FAC = json.loads(re.search(r"var FACILITIES = (\[.*?\]);", src, re.S).group(1))
URLS = json.load(open(os.path.join(ROOT, "data/urls.json"), encoding="utf-8"))

date_by_slug = {x["slug"]: x["date"][:10] for x in URLS}
title_by_slug = {x["slug"]: x["title"] for x in URLS}

# 記事ページが実在する施設だけを対象にする
items = []
for f in FAC:
    slug = f.get("slug")
    if not slug:
        continue
    if not os.path.exists(os.path.join(ROOT, slug, "index.html")):
        continue
    items.append({
        "name": f.get("name") or title_by_slug.get(slug, slug),
        "slug": slug,
        "pref": f.get("pref") or "",
        "price": f.get("price"),
        "yen_h": f.get("yen_h"),
        "min": f.get("min"),
        "total": f.get("total"),
        "cospa": f.get("cospa"),
        "taipa": f.get("taipa"),
        "closed": bool(f.get("closed")),
        "official": f.get("official") or "",
        "date": date_by_slug.get(slug, ""),
    })

# 新着順（同日は総合スコアの高い順）
items.sort(key=lambda x: (x["date"], x["total"] if x["total"] is not None else -1), reverse=True)

COLUMN_SLUG = "サウナのふるさと納税｜実質2000円でととのう、コ"

def e(s):
    return html.escape(str(s if s is not None else ""), quote=True)

def fmt(v):
    if v is None or v == "":
        return "—"
    try:
        return "%.1f" % float(v)
    except (TypeError, ValueError):
        return "—"

def place(x):
    parts = []
    if x["pref"]:
        parts.append(e(x["pref"]))
    if x["min"] not in (None, ""):
        parts.append("主要都市から%s分" % x["min"])
    if x["price"] not in (None, ""):
        yh = ""
        if x["yen_h"] not in (None, ""):
            yh = "（¥%d/h）" % round(float(x["yen_h"]))
        parts.append("平日%s円%s" % (x["price"], yh))
    return " ／ ".join(parts)

rows = []
for x in items:
    href = "/" + x["slug"] + "/"
    tag = '<span class="closed-tag">閉店</span>' if x["closed"] else ""
    chips = ""
    q = x["name"] + ((" " + x["pref"]) if x["pref"] else "")
    from urllib.parse import quote
    chips += ('<a class="chip" href="https://www.google.com/maps/search/?api=1&amp;query=%s"'
              ' target="_blank" rel="noopener">MAP</a>' % quote(q, safe=""))
    if x["official"]:
        chips += ('<a class="chip" href="%s" target="_blank" rel="noopener">公式</a>' % e(x["official"]))
    subs = ('<span class="c-total">総合<b>{t}</b></span>'
            '<span class="c-cospa">コスパ<b>{c}</b></span>'
            '<span class="c-taipa">タイパ<b>{p}</b></span>').format(
                t=fmt(x["total"]), c=fmt(x["cospa"]), p=fmt(x["taipa"]))
    rows.append(
        '      <div class="rank-row has-link">'
        '<div class="pos num">{date}</div>'
        '<div class="info">'
        '<div class="nm"><a class="name-link" href="{href}">{name} <span class="go-arrow">›</span></a>{tag}</div>'
        '<div class="pl">{place} <span style="white-space:nowrap;margin-left:6px;">{chips}</span></div>'
        '<div class="subs-sp">{subs}</div>'
        '</div>'
        '<div class="subs">{subs}</div>'
        '<div class="score num">{total}<span class="s">OVERALL</span></div>'
        '</div>'.format(
            date=e(x["date"][5:].replace("-", ".")), href=quote(href, safe="/"), name=e(x["name"]),
            tag=tag, place=place(x), chips=chips, subs=subs, total=fmt(x["total"])))

column_row = ""
if os.path.exists(os.path.join(ROOT, COLUMN_SLUG, "index.html")):
    from urllib.parse import quote
    column_row = (
        '      <div class="rank-row has-link">'
        '<div class="pos num">{date}</div>'
        '<div class="info">'
        '<div class="nm"><a class="name-link" href="{href}">{title} <span class="go-arrow">›</span></a></div>'
        '<div class="pl">コラム ／ 返礼品でととのう、コスパのはなし</div>'
        '</div>'
        '</div>'.format(
            date=e(date_by_slug.get(COLUMN_SLUG, "")[5:].replace("-", ".")),
            href=quote("/" + COLUMN_SLUG + "/", safe="/"),
            title=e(title_by_slug.get(COLUMN_SLUG, "サウナのふるさと納税"))))

DESC = "GOMIRACHELINが実際に訪問して10項目で採点した、全国%d軒のサウナ正直レビュー一覧。新着順に、総合・コスパ・タイパのスコアつきで掲載しています。" % len(items)

page = """<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>レビュー一覧 | GOMIRACHELIN</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="https://sauna-cospa.com/reviews/">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Oswald:wght@300;400;500;600;700&family=Shippori+Mincho:wght@500;700;800&family=Zen+Kaku+Gothic+New:wght@400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/site.css">
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-GTF2GM6DNJ"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-GTF2GM6DNJ');
  </script>
  <style>
    /* 順位ではなく公開日を出すので、左カラムは小さめ・グレーで統一する */
    .ranking-static .rank-list[data-metric="total"] .rank-row .pos,
    .ranking-static .rank-list[data-metric="total"] .rank-row:nth-child(-n+3) .pos{{
      font-size:12px;min-width:46px;color:#7a756a;padding-top:6px;letter-spacing:1px;
    }}
  </style>
</head>
<body>
<input type="checkbox" id="nav-check">
<header class="site-header">
  <div class="wrap nav">
    <a class="brand" href="/">
      <span class="mark">G</span>
      <span>
        <b>GOMIRACHELIN</b>
        <span class="tag">Sauna Guide</span>
      </span>
    </a>
    <button class="nav-toggle" type="button" onclick="document.getElementById('nav-check').click()" aria-label="メニュー">MENU</button>
    <nav class="nav-links" aria-label="メインメニュー">
        <a href="/">トップ</a>
        <a href="/why/">WHY</a>
        <a href="/ランキング/">ランキング</a>
        <a href="/sauna-university/">サウナ大学</a>
        <a href="/map/">サウナ地図</a>
        <a href="/お問い合わせ/">お問い合わせ</a>
    </nav>
  </div>
</header>
<main class="page-main"><article class="entry">
  <header class="entry-head">
    <p class="kicker">GOMIRACHELIN</p>
    <h1>レビュー一覧</h1>
  </header>
  <div class="entry-body">
<h2 style="color:#d4a017;font-size:1.3em;">一軒ずつ、正直に。</h2>
<p>GOMIRACHELINが実際に足を運んで、①サウナ室②水風呂③休憩④動線⑤ロウリュ⑥スパ内施設⑦スパ外施設⑧清潔さ⑨唯一無二性⑩ホスピタリティの10項目で採点した、全{n}軒の正直レビューです。新しく書いたものから順に並べています。</p>
<p>スコアの高い順に見たいときは<a href="/%E3%83%A9%E3%83%B3%E3%82%AD%E3%83%B3%E3%82%B0/">ランキング</a>を、10項目それぞれの採点を見比べたいときは<a href="/10%E9%A0%85%E7%9B%AE%E5%88%A5%E3%83%A9%E3%83%B3%E3%82%AD%E3%83%B3%E3%82%B0/">EVALUATION</a>をご覧ください。</p>
</div>
<section class="ranking-static" id="reviews" aria-label="サウナレビュー一覧">
  <div class="section-head">
    <div class="label">ALL REVIEWS</div>
    <h2 class="mincho">サウナ正直レビュー</h2>
    <p>新着順 ／ 総合・コスパ・タイパのスコアつき</p>
  </div>
  <div class="rank-list" data-metric="total">
{rows}
  </div>
  <p class="more-note num">全 {n} 施設</p>
{columnblock}
  <div class="more-link">
    <a href="/%E3%83%A9%E3%83%B3%E3%82%AD%E3%83%B3%E3%82%B0/">RANKING ›</a>
  </div>
  <p class="foot-note">点数は管理人の主観による評価です ／ 掲載スコアは訪問時点のもの ／ ※当サイトはアフィリエイトプログラムを利用しています</p>
</section>
</article></main>
<footer class="site-footer">
  <div class="wrap">
    <div class="footer-brand">
      <div class="gold-rule"></div>
      <div class="name">GOMIRACHELIN</div>
      <div class="sub">Cospa Sauna Guide</div>
    </div>
    <ul class="footer-links">
          <li><a href="/why/">WHY</a></li>
          <li><a href="/%E3%83%A9%E3%83%B3%E3%82%AD%E3%83%B3%E3%82%B0/">ランキング</a></li>
          <li><a href="/10%E9%A0%85%E7%9B%AE%E5%88%A5%E3%83%A9%E3%83%B3%E3%82%AD%E3%83%B3%E3%82%B0/">EVALUATION</a></li>
          <li><a href="/sauna-university/">サウナ大学</a></li>
          <li><a href="/%E3%81%8A%E5%95%8F%E3%81%84%E5%90%88%E3%82%8F%E3%81%9B/">お問い合わせ</a></li>
          <li><a href="/%E9%81%8B%E5%96%B6%E8%80%85%E6%83%85%E5%A0%B1/">運営者情報</a></li>
          <li><a href="/%E3%83%97%E3%83%A9%E3%82%A4%E3%83%90%E3%82%B7%E3%83%BC%E3%83%9D%E3%83%AA%E3%82%B7%E3%83%BC/">プライバシーポリシー</a></li>
          <li><a href="/%E5%85%8D%E8%B2%AC%E4%BA%8B%E9%A0%85/">免責事項</a></li>
    </ul>
    <p class="footer-copy">© 2026 GOMIRACHELIN　コスパで選ぶ、全国サウナ正直ガイド</p>
  </div>
</footer>
</body>
</html>
"""

columnblock = ""
if column_row:
    columnblock = ('  <div class="section-head" style="margin-top:56px;">\n'
                   '    <div class="label">COLUMN</div>\n'
                   '    <h2 class="mincho">コラム</h2>\n'
                   '  </div>\n'
                   '  <div class="rank-list" data-metric="total">\n'
                   + column_row + '\n  </div>\n')

out = page.format(desc=e(DESC), rows="\n".join(rows), n=len(items), columnblock=columnblock)
os.makedirs(os.path.join(ROOT, "reviews"), exist_ok=True)
open(os.path.join(ROOT, "reviews/index.html"), "w", encoding="utf-8").write(out)
print("生成しました: reviews/index.html  施設 %d 件 / コラム %d 件" % (len(items), 1 if column_row else 0))

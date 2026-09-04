# -*- coding: utf-8 -*-
"""サイトマップページ（サイトマップ/index.html）を作り直すスクリプト。

「サイトマップ」ページは、検索エンジン向けの sitemap.xml とは別に、
人（サイトを見に来た人）向けに全ページの一覧を見せるためのページです。

使い方（サイトのフォルダで）:
    python3 scripts/gen_sitemapp.py

データの元:
  - ランキング/index.html の中の FACILITIES（施設名・slug）
  - data/urls.json（記事・固定ページの一覧とタイトル）
記事フォルダ（<slug>/index.html）が実際にあるものだけを載せます。
"""
import re, json, os, html
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

src = open(os.path.join(ROOT, "ランキング/index.html"), encoding="utf-8").read()
FAC = json.loads(re.search(r"var FACILITIES = (\[.*?\]);", src, re.S).group(1))
URLS = json.load(open(os.path.join(ROOT, "data/urls.json"), encoding="utf-8"))

def e(s):
    return html.escape(str(s), quote=True)

def link(slug, title):
    href = "/" + quote(slug, safe="") + "/"
    return '<li><a href="%s">%s</a></li>' % (href, e(title))

# --- 施設レビュー一覧（記事フォルダが実在するものだけ、五十音・英数字順） ---
slug_has_page = lambda s: bool(s) and os.path.exists(os.path.join(ROOT, s, "index.html"))
title_by_slug = {x["slug"]: x["title"] for x in URLS}

posts = [x for x in URLS if x["type"] == "post" and slug_has_page(x["slug"])]
posts.sort(key=lambda x: x["title"])
review_items = "\n".join("      " + link(x["slug"], x["title"]) for x in posts)

MAIN_PAGES = [
    ("top", "トップ"),
    ("why", "WHY"),
    ("ランキング", "ランキング"),
    ("10項目別ランキング", "10項目別ランキング（EVALUATION）"),
    ("reviews", "レビュー一覧"),
    ("sauna-university", "サウナ大学"),
]
def main_link(slug, title):
    href = "/" if slug == "top" else "/" + quote(slug, safe="") + "/"
    return '<li><a href="%s">%s</a></li>' % (href, e(title))
main_items = "\n".join("      " + main_link(s, t) for s, t in MAIN_PAGES)

INFO_PAGES = [
    ("お問い合わせ", "お問い合わせ"),
    ("運営者情報", "運営者情報"),
    ("プライバシーポリシー", "プライバシーポリシー"),
    ("免責事項", "免責事項"),
]
info_items = "\n".join("      " + link(s, t) for s, t in INFO_PAGES)

DESC = "GOMIRACHELINの全ページ一覧です。メインページ、施設レビュー全%d件、サイト情報ページへのリンクをまとめています。" % len(posts)

page = """<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>サイトマップ | GOMIRACHELIN</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="https://sauna-cospa.com/%E3%82%B5%E3%82%A4%E3%83%88%E3%83%9E%E3%83%83%E3%83%97/">
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
        <a href="/お問い合わせ/">お問い合わせ</a>
        <a href="/サイトマップ/" class="is-active">サイトマップ</a>
    </nav>
  </div>
</header>
<main class="page-main"><article class="entry">
  <header class="entry-head">
    <p class="kicker">GOMIRACHELIN</p>
    <h1>サイトマップ</h1>
  </header>
  <div class="entry-body">
<p>GOMIRACHELINの全ページの一覧です。お探しのページが見つからないときにご利用ください。</p>

<h2>メインページ</h2>
<ul>
{main_items}
</ul>

<h2>サウナ施設レビュー（全{n}件・五十音順）</h2>
<ul>
{review_items}
</ul>

<h2>サイト情報</h2>
<ul>
{info_items}
</ul>

<p style="margin-top:2em;font-size:13px;color:#7a756a;">検索エンジン向けの一覧（XMLサイトマップ）は <a href="/sitemap.xml">sitemap.xml</a> をご覧ください。</p>
</div>
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
          <li><a href="/ランキング/">ランキング</a></li>
          <li><a href="/10項目別ランキング/">EVALUATION</a></li>
          <li><a href="/sauna-university/">サウナ大学</a></li>
          <li><a href="/お問い合わせ/">お問い合わせ</a></li>
          <li><a href="/運営者情報/">運営者情報</a></li>
          <li><a href="/プライバシーポリシー/">プライバシーポリシー</a></li>
          <li><a href="/免責事項/">免責事項</a></li>
          <li><a href="/サイトマップ/" class="is-active">サイトマップ</a></li>
    </ul>
    <p class="footer-copy">© 2026 GOMIRACHELIN　コスパで選ぶ、全国サウナ正直ガイド</p>
  </div>
</footer>
</body>
</html>
"""

out = page.format(desc=e(DESC), main_items=main_items, review_items=review_items,
                   info_items=info_items, n=len(posts))
os.makedirs(os.path.join(ROOT, "サイトマップ"), exist_ok=True)
open(os.path.join(ROOT, "サイトマップ/index.html"), "w", encoding="utf-8").write(out)
print("生成しました: サイトマップ/index.html  施設 %d 件" % len(posts))

# 公開サイトとGitHubの差分

最終更新：2026-09-05 23:24 JST前後

確認方法：公開HTTPのGETとGitHub mainの読み取りのみ。ConoHa管理画面は未ログイン。

## 要約

- 生産 `https://sauna-cospa.com` は稼働している。トップはWordPress形式のまま。
- GitHubの `sitemap.xml` と生産の `/sitemap.xml` のURL一覧は一致して見える。
- ただし生産の `/reviews/` は404。GitHub側にだけある自作ページ。
- 生産に `robots.txt` はない（404）。GitHubにも無い。
- GitHubに `gas/` ディレクトリは無い。

## 生産で確認したHTTP

| URL | 結果 | 備考 |
|-----|--------|------|
| `https://sauna-cospa.com/` | 200 | WHYへのリンクが `/?page_id=37` のまま。「レビュー一覧を見る」は `/reviews/` 向き |
| `https://sauna-cospa.com/reviews/` | 404 | GitHubには `reviews/index.html` がある。本番未反映 |
| `https://sauna-cospa.com/robots.txt` | 404 | 未作成 |
| `https://sauna-cospa.com/sitemap.xml` | 200 | GitHubのサイトマップと同じURL群に見える |
| `https://sauna-cospa.com/category/review/` | 200 | WordPressカテゴリ。GitHub静的サイト側の対応ファイルは未確認 |

## GitHubにあり、生産にないもの（確認済）

- `/reviews/`
- トップメニューの「サウナ地図」（生産トップの抽出文に地図メニューは出てこない）
- `sauna-app.webmanifest` / `sauna-icon-180.png`（PR #3でGitHubに追加済。生産の有無はバックアップ時に再確認）

## 生産にあり、GitHubに不足している可能があるもの

- WordPress本体（`wp-admin` / `wp-content` / `wp-includes`）
- `wp-content/uploads` の画像
- WordPressカテゴリ `/category/review/`
- GAS本体ソース（`gas/` なし）
- Google Sheetsの全データ
- `robots.txt`

## 一致しているもの

- 主要固定ページと個別レビューのURL群（`data/urls.json` と生産sitemap）
- `sauna-daigaku.html`

## 判断と理由

- 今の段階で生産に `/reviews/` を上げない。バックアップ前に公開ディレクトリへ書き込むと、戻せない上書きのリスクがあるため。
- トップが既に `/reviews/` を指しているのは既知の切れ。切替後に直す。

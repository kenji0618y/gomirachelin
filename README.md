# GOMIRACHELIN 静的HTML（ConoHaアップロード用）

このフォルダは、公開中の WordPress サイト [https://sauna-cospa.com](https://sauna-cospa.com) を **読み取り専用（GET / REST）** で書き出した静的HTMLです。

## 大事なこと

- **本番の WordPress は一切変更していません。** ログイン、投稿、削除、設定変更はしていません。
- これらは、あとから ConoHa のドキュメントルートへアップロードするためのサイトファイルです。
- Git の正本は非公開リポジトリ https://github.com/kenji0618y/gomirachelin です。**Git コマンドは覚えなくて大丈夫です。** 変更は grok bot 1 に頼んでください。

## 中身

| パス | 内容 |
|------|------|
| `index.html` | トップ（WP ページ id 57 / slug `top`） |
| `{スラッグ}/index.html` | 各投稿・固定ページ（Unicode スラッグ、末尾スラッシュ相当） |
| `sauna-daigaku.html` | 公開中の静的ファイルをそのまま保存（Amazon タグ `gomirachelin-22` を維持） |
| `css/site.css` | 黒×金の共通ヘッダー / ナビ / フッター |
| `reviews/index.html` | レビュー一覧（自作ページ。`scripts/gen_reviews.py` で生成） |
| `scripts/gen_reviews.py` | レビュー一覧を作り直すスクリプト |
| `docs/新規レビュー記事の追加手順.md` | サウナを1軒追加するときの手順書 |
| `sitemap.xml` | 書き出した URL 一覧 |
| `data/urls.json` | id / slug / title / link / date / type |

ナビ: トップ / WHY / ランキング / サウナ大学 / お問い合わせ

トップページの「レビュー一覧を見る」から `/reviews/` に行けます。

デザインは `sauna-daigaku.html` の `:root`（黒地、金 `#d4a017`、Shippori Mincho / Oswald / Zen Kaku Gothic New）に合わせています。本文の点数・レビュー文・リンク（アフィリエイト含む）は WordPress の `content.rendered` をそのまま包んでいます。ランキング・TOP3・EVALUATION の GAS iframe と、お問い合わせの Google フォームもそのまま残しています。

## アップロードのとき

ConoHa の公開ディレクトリに、このフォルダの **中身**（`index.html` がルートに来るように）を置けば表示されます。本番 WordPress を止める・移す作業は、このファイル作成とは別の判断です。

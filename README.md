# GOMIRACHELIN 静的HTML

全国のサウナ施設を独自の10項目で評価するサイト「GOMIRACHELIN（ゴミラシュラン）」の静的HTMLファイル群です。
もとは公開中の WordPress サイト [https://sauna-cospa.com](https://sauna-cospa.com) を **読み取り専用（GET / REST）** で書き出したものですが、現在は **このリポジトリを唯一の正本として直接編集していく運用**（WordPressは近いうち廃止予定）に移行中です。詳しい経緯や進捗は `docs/STATE.md` を参照してください。

## 大事なこと

- **本番の WordPress は一切変更していません。** ログイン、投稿、削除、設定変更はしていません。
- Git の正本は非公開リポジトリ https://github.com/kenji0618y/gomirachelin です。**Git コマンドは覚えなくて大丈夫です。** 変更はClaude（AIアシスタント）に頼んでください。
- 公開方法は **ConoHaへの手動アップロード → GitHub Pages（自動公開）へ移行中**。今の状況は `docs/STATE.md` の「次にやること」を参照。

## 中身

| パス | 内容 |
|------|------|
| `index.html` | トップ（WP ページ id 57 / slug `top`） |
| `{スラッグ}/index.html` | 各投稿・固定ページ（Unicode スラッグ、末尾スラッシュ相当） |
| `sauna-daigaku.html` | 公開中の静的ファイルをそのまま保存（Amazon タグ `gomirachelin-22` を維持） |
| `css/site.css` | 黒×金の共通ヘッダー / ナビ / フッター |
| `reviews/index.html` | レビュー一覧（自作ページ。`scripts/gen_reviews.py` で生成） |
| `サイトマップ/index.html` | 全ページ一覧（自作ページ。`scripts/gen_sitemapp.py` で生成） |
| `scripts/gen_reviews.py` | レビュー一覧を作り直すスクリプト |
| `scripts/gen_sitemapp.py` | サイトマップページを作り直すスクリプト |
| `docs/新規レビュー記事の追加手順.md` | サウナを1軒追加するときの手順書 |
| `docs/STATE.md` | サイトの現状・次にやること・決定事項の記録（作業前に必読） |
| `sitemap.xml` | 検索エンジン向けのURL一覧（XMLサイトマップ） |
| `data/urls.json` | id / slug / title / link / date / type |
| `sauna-icon-180.png` / `sauna-app.webmanifest` | スマホのホーム画面アイコン用（自作） |
| `404.html` | ページが見つからないときの案内（GitHub Pages用） |
| `.nojekyll` / `CNAME` | GitHub Pages公開用の設定ファイル |

ナビ: トップ / WHY / ランキング / サウナ大学 / お問い合わせ / サイトマップ

トップページの「レビュー一覧を見る」から `/reviews/` に、メニューの「サイトマップ」から `/サイトマップ/` に行けます。

デザインは `sauna-daigaku.html` の `:root`（黒地、金 `#d4a017`、Shippori Mincho / Oswald / Zen Kaku Gothic New）に合わせています。本文の点数・レビュー文・リンク（アフィリエイト含む）は WordPress の `content.rendered` をそのまま包んでいます。ランキング・TOP3・EVALUATION は静的なリストに置き換え済みで、お問い合わせの Google フォームはそのまま残しています。

## 公開方法（移行中）

現在は次の2通りが併存しています。今後はGitHub Pagesに一本化する予定です。

- **今まで**：ConoHaの公開ディレクトリに、このフォルダの中身（`index.html` がルートに来るように）を手動アップロード。
- **これから**：`main` ブランチにpushすると、GitHub Pagesが自動で `https://sauna-cospa.com/` に公開する形にする予定（DNS設定など、外部サービス側の準備が別途必要）。

本番 WordPress を止める・移す作業は、このファイル作成とは別の判断です。進め方は `docs/STATE.md` を参照してください。

# GOMIRACHELIN 静的HTML

全国のサウナ施設を独自の10項目で評価し、料金（コスパ）で格付けするサイト
**GOMIRACHELIN（ゴミラシュラン）** の静的HTMLファイル群です。

- 公開URL：[https://sauna-cospa.com](https://sauna-cospa.com)
- 中身：**素の静的HTML**。ビルド不要、npm不要、フレームワーク不要
- 由来：もとはWordPressサイトをREST APIで **読み取り専用** に書き出したもの
- 現在：**このリポジトリを唯一の正本として直接編集する運用に移行中**（WordPressは近いうち廃止予定）

---

## 📖 まずここを読む

| 読む人 | 読むファイル |
|---|---|
| **AIエージェント**（Claude Code / Codex など） | **`AGENTS.md` → `docs/STATE.md`** の順に必ず読む |
| 人間（サイトの持ち主） | `docs/STATE.md` の「次にやること」 |

### ドキュメント一覧

| ファイル | 内容 |
|---|---|
| `AGENTS.md` | AIエージェント向け指示書。ルール・禁止事項・全体像・データ構造 |
| `docs/STATE.md` | 現状・次にやること・決定事項の記録（作業日誌） |
| `docs/サイト構成.md` | サイトの構造とデータの持ち方の詳細リファレンス |
| `docs/作業手順とチェック方法.md` | 動作確認の手順と、実際にハマった落とし穴 |
| `docs/新規レビュー記事の追加手順.md` | サウナを1軒追加する手順（8ステップ） |
| `docs/GitHub-Pages移行手順.md` | WordPress廃止・GitHub Pages移行の作業手順 |

---

## 大事なこと

- **本番のWordPressは一切変更していません。** ログイン・投稿・削除・設定変更はしていません
- **Gitコマンドは覚えなくて大丈夫です。** 変更はAIアシスタント（Claude Codeなど）に頼んでください
- 公開方法は **ConoHaへの手動アップロード → GitHub Pages（自動公開）へ移行中**
- `reviews/index.html` と `サイトマップ/index.html` は **自動生成ファイル**。手で編集しないこと
- `sauna-daigaku.html` は **独自構造の特殊ファイル**。一括処理の対象から必ず除外すること

---

## ファイル構成

| パス | 内容 |
|------|------|
| `index.html` | トップ（WP ページ id 57 / slug `top`） |
| `{スラッグ}/index.html` | 各投稿・固定ページ（日本語スラッグ、末尾スラッシュ相当） |
| `ランキング/index.html` | **施設データ `FACILITIES`（176件）の正本がここにある** |
| `10項目別ランキング/index.html` | 10項目それぞれの順位（全部手書き） |
| `reviews/index.html` | レビュー一覧（自動生成。`scripts/gen_reviews.py`） |
| `サイトマップ/index.html` | 全ページ一覧（自動生成。`scripts/gen_sitemapp.py`） |
| `sauna-daigaku.html` | ★特殊★ サウナ大学の単独アプリ版（Amazonタグ `gomirachelin-22` を維持） |
| `404.html` | ページが見つからないときの案内（GitHub Pages用） |
| `css/site.css` | 黒×金の共通ヘッダー / ナビ / フッター（322行） |
| `data/urls.json` | 全ページのメタ情報（id / slug / title / link / date / type） |
| `sitemap.xml` | 検索エンジン向けURL一覧（XMLサイトマップ） |
| `sauna-icon-180.png` / `sauna-app.webmanifest` | スマホのホーム画面アイコン用（自作） |
| `.nojekyll` / `CNAME` | GitHub Pages公開用の設定ファイル |
| `scripts/gen_reviews.py` | レビュー一覧を作り直すスクリプト |
| `scripts/gen_sitemapp.py` | サイトマップページを作り直すスクリプト |

**数のまとめ**：HTMLファイル63個／個別記事50本（施設47軒＋コラム1本＋重複2本）／ランキング掲載176施設

ナビ：トップ / WHY / ランキング / サウナ大学 / お問い合わせ / サイトマップ

---

## デザイン

黒地（`#0f0d0a`）×金（`#d4a017`）が基調。フォントは Shippori Mincho / Oswald / Zen Kaku Gothic New。
定義は `css/site.css` の `:root` にあります。

本文の点数・レビュー文・リンク（アフィリエイト含む）は、WordPress の `content.rendered` を
そのまま包んでいます。ランキング・トップ3・EVALUATION はGoogle Apps Scriptのiframeから
静的リストに置き換え済みです。

---

## ローカルで確認する

```bash
python3 -m http.server 8000
```

ブラウザで `http://127.0.0.1:8000/` を開きます（止めるときは `Ctrl` + `C`）。

変更後は **リンク切れチェック** を必ず実行してください
（コマンドは `docs/作業手順とチェック方法.md` に記載）。

---

## 公開方法（移行中）

- **今まで**：ConoHaの公開ディレクトリに、このフォルダの中身（`index.html` がルートに来るように）を手動アップロード
- **これから**：`main` ブランチにpushすると、GitHub Pagesが自動で `https://sauna-cospa.com/` に公開

移行の進捗と手順は `docs/GitHub-Pages移行手順.md` および `docs/STATE.md` を参照してください。

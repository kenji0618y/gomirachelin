# 公開サイトとGitHubの差分調査

作成日：2026-09-05
担当：Claude（読み取り専用調査）
調査基点：GitHub `main` = `c33ba41`

---

## ⚠️ 最初に：本調査の範囲と限界

**公開サイト `https://sauna-cospa.com` へは、今回の作業環境からアクセスできませんでした。**

| 試した方法 | 結果 |
|---|---|
| `curl https://sauna-cospa.com/` | `CONNECT tunnel failed, response 403` |
| `curl https://sauna-cospa.com/robots.txt` | 同上 |
| WebFetchツール | `EGRESS_BLOCKED`（ネットワーク制限） |

サイト側の問題ではなく、**作業環境のネットワーク制限**です。

したがって本文書は次の構成になっています。

| 区分 | 内容 | 信頼度 |
|---|---|---|
| **A. GitHub側から確定できた事実** | mainのファイルを実測した結果 | ✅ **確定** |
| **B. 本番側の確認が必要な項目** | 誰かが本番を見ないと埋まらない箇所 | ⏳ **未確認** |

**B の項目には、そのまま実行できる確認コマンド・手順を添えてあります。**
ConoHaにアクセスできるCodexまたはKenjiさんが実行すれば、この文書を完成させられます。

---

## 総括：最優先で対応すべきもの

| 順位 | 内容 | 影響 |
|---|---|---|
| 🔴 **1** | **サウナ大学の写真35枚がWordPressサーバー上にしかない** | ConoHa解約でサウナ大学の写真が全部消える |
| 🔴 **2** | **リポジトリ内の画像が1枚しかない** | 本番にある画像類が未把握。棚卸しが必要 |
| 🟡 **3** | `robots.txt` が無い | 検索エンジンへの指示が引き継がれない |
| 🟡 **4** | `.htaccess`（リダイレクト設定）が無い | 旧URLの転送設定が引き継がれない |
| 🟡 **5** | メニューが61ページ中1ページだけ違う | 「サウナ地図」がトップにしか無い |
| 🟢 **6** | WordPress固有URL `/?page_id=37` が1件残存 | 移行後リンク切れになる |
| 🟢 **7** | `sauna-daigaku.html` 内に `/category/review/` が1件残存 | 移行後リンク切れになる |

---

# A. GitHub側から確定できた事実

## A-1. 🔴 サウナ大学の写真35枚がWordPressサーバー依存

**最も重大な発見です。**

`sauna-daigaku.html`（サウナ大学）が、**WordPressのアップロードフォルダにある写真35枚を直接読み込んでいます。**

```
https://sauna-cospa.com/wp-content/uploads/2026/07/sauna-univ-01.jpg
　…（sauna-univ-01 〜 sauna-univ-45 のうち35枚）
```

| 項目 | 内容 |
|---|---|
| ユニークな画像URL数 | **35枚**（すべて `.jpg`） |
| 参照元ファイル | `sauna-daigaku.html` のみ |
| 使われ方 | 1枚は92行目のCSS背景（`url(...)`）、34枚はJavaScriptの `photo:` プロパティ |
| 表示箇所 | 3873行目 `` `<img src="${ch.photo}">` `` で各レッスンのカバー画像として描画 |

### なぜ危険か

これらの画像は **WordPressの `wp-content/uploads/` にしか存在しません。**
GitHubリポジトリには入っていません（リポジトリ内の画像は後述のとおり1枚だけ）。

- **ConoHaを解約した瞬間、サウナ大学の写真35枚がすべて表示されなくなります。**
- GitHub Pagesへ移行しても、画像は旧サーバーを見に行き続けます。
- 移行直後は「まだ動いている」ように見えるため、**解約まで気づきにくい**のが特に危険です。

### 確認方法

```bash
# GitHub側（実行済み）
grep -rhoE 'https?://sauna-cospa\.com/wp-content/uploads/[^"'"'"' )]+' --include="*.html" . | sort -u | wc -l
# → 35
```

### 移行時の対応案

1. **バックアップから35枚を回収する**（ConoHaバックアップの `wp-content/uploads/2026/07/` 配下）
2. リポジトリに `images/sauna-univ/` のようなフォルダを作り、35枚を置く
3. `sauna-daigaku.html` の35箇所のURLを `/images/sauna-univ/sauna-univ-01.jpg` の形に書き換える
4. 書き換え後、35枚すべてが表示されることを確認する

> **注意**：`sauna-daigaku.html` は約4,900行の特殊ファイルです。一括置換は
> 「`https://sauna-cospa.com/wp-content/uploads/2026/07/`」→「`/images/sauna-univ/`」
> の単純置換で足りますが、置換後に必ず画像の表示確認をしてください。

> **優先度：最高。** ConoHaバックアップを取る際、`wp-content/uploads/` は
> **必ず含めてください。** ここが欠けると復旧できません。

---

## A-2. 🔴 リポジトリ内の画像が1枚しかない

`git ls-files` で実測した結果です。

| 種別 | 件数 | 内訳 |
|---|---|---|
| 追跡ファイル総数 | 78 | |
| HTMLファイル | 62 | |
| **画像ファイル** | **1** | `sauna-icon-180.png` のみ（PR #3で追加した代替アイコン） |
| PDFファイル | **0** | |

### 意味すること

**本番サイトにある画像・PDF・アイコン類が、ほぼ何もGitHubに入っていません。**

ただし、HTMLが参照している画像を調べたところ、**サイト内の相対パスで画像を呼んでいる箇所はほぼありません**でした。画像は次のいずれかです。

| 参照先 | 件数 | 移行後どうなるか |
|---|---|---|
| WordPress（`sauna-cospa.com/wp-content/`） | 35 | 🔴 **消える**（A-1） |
| 楽天トラベル（`img.travel.rakuten.co.jp`） | 13 | ✅ 外部なので生き続ける |
| サイト内の画像 | ほぼ0 | — |

つまり **「GitHubに画像が無い」のは、記事本文がほとんど画像を使っていないため**であり、
実害があるのは A-1 の35枚です。

ただし **本番サーバー上に、HTMLから参照されていない画像・PDF・ファビコン等が
置かれている可能性は残ります**（→ B-1で要確認）。

---

## A-3. 🟡 robots.txt が無い

| ファイル | GitHub main |
|---|---|
| `robots.txt` | ❌ **無い** |
| `sitemap.xml` | ✅ ある（61件） |
| `favicon.ico` | ❌ 無い |
| `ads.txt` | ❌ 無い |

### 影響

検索エンジンへの指示（クロール可否、サイトマップの場所）が引き継がれません。
本番に `robots.txt` がある場合、移行後に消えると **SEOに影響する可能性**があります。

### 移行時の対応案

本番の `robots.txt` を確認して（→ B-2）、同じ内容をリポジトリに置きます。
無い場合も、最低限これを置くのが安全です。

```
User-agent: *
Allow: /

Sitemap: https://sauna-cospa.com/sitemap.xml
```

> `favicon.ico` と `ads.txt` も同様に、本番にあるか確認してください（→ B-2）。

---

## A-4. 🟡 .htaccess（リダイレクト設定）が無い

`.htaccess` は **Apacheサーバー（ConoHa）専用のリダイレクト・エラーページ設定ファイル**です。

| 項目 | 状況 |
|---|---|
| GitHub mainに `.htaccess` | ❌ **無い** |
| 本番の `.htaccess` | ⏳ 未確認（→ B-3） |

### なぜ重要か

WordPressは通常 `.htaccess` にパーマリンク用のルールを書きます。
さらに、**手動で追加した旧URLのリダイレクト**が入っている可能性があります。
これが引き継がれないと、**外部サイトからのリンクや検索結果からの流入が切れます。**

### 移行時の対応案

GitHub Pagesは `.htaccess` を**使えません**。リダイレクトが必要な場合は別の方法になります。

| 本番の `.htaccess` の中身 | GitHub Pagesでの代替 |
|---|---|
| WordPressの標準ルールのみ | 対応不要（静的サイトには不要） |
| 旧URL → 新URL のリダイレクト | 各旧URLの場所に、転送用のHTMLを置く |
| `ErrorDocument 404` | GitHub Pagesは `404.html` を自動で使うため対応不要 |

> **先に B-3 で中身を確認してから、対応要否を判断してください。**

---

## A-5. 🟡 メニューが1ページだけ違う

61ページのメニューを実測しました。

| メニュー構成 | ページ数 |
|---|---|
| トップ / WHY / ランキング / サウナ大学 / お問い合わせ | **59** |
| トップ / WHY / ランキング / サウナ大学 / **サウナ地図** / お問い合わせ | **1**（`index.html` のみ） |
| （独自メニュー） | 1（`sauna-daigaku.html`） |

### 影響

- **「サウナ地図」はトップページにしか無い**ため、他のページからは行けません
- 既知のとおり、**地図は未ログインの訪問者には開けません**（GASのアクセス設定が「自分のみ」）

### 移行時の対応案

地図の公開方法が決まってから、次のどちらかに揃えます。

| 案 | 内容 |
|---|---|
| A | 地図を一般公開できるようにしてから、59ページすべてにメニューを追加する |
| B | 公開方法が決まるまで、`index.html` からも地図リンクを外して59ページに揃える |

> **判断はKenjiさん・Codex側にお任せします。** 本調査では変更していません。

---

## A-6. 🟢 WordPress固有URLの残存（2件）

| # | URL | 場所 | 移行後 |
|---|---|---|---|
| 1 | `/?page_id=37` | `index.html` 115行目 | 🔴 リンク切れ |
| 2 | `https://sauna-cospa.com/category/review/` | `sauna-daigaku.html` 570行目 | 🔴 リンク切れ |

### 詳細

**1件目：`/?page_id=37`**
WordPressの固定ページID形式のURLです。ID=37は **WHYページ**（`/why/`）にあたります。
静的サイトにはこのURLが存在しないため、移行後は404になります。

- **対応案**：`/?page_id=37` → `/why/` に書き換える（1箇所）

**2件目：`/category/review/`**
WordPressのカテゴリー一覧ページです。静的サイトには存在しません。
`sauna-daigaku.html` の「正直レビュー一覧」ボタンのリンク先です。

- **対応案**：`/reviews/`（既存のレビュー一覧ページ）に書き換える（1箇所）

> なお `http://kamifurano-hokkaido.com/?page_id=2` も検出されましたが、
> これは**外部サイトのURL**なので対応不要です。

---

## A-7. ✅ 問題が無かった項目

念のため確認し、**問題なし**だった項目です。

| 項目 | 結果 |
|---|---|
| サイト内リンク切れ | **0件** |
| フォルダ / `data/urls.json` の整合 | ✅ 一致（`reviews` の登録漏れ1件のみ） |
| `sitemap.xml` の網羅性 | ✅ 全フォルダを収録（61件） |
| `FACILITIES` のslugと記事の対応 | ✅ 47件すべて記事が存在 |
| 問い合わせフォーム | ✅ Googleフォームへの**リンク**（iframeではない）ため移行の影響なし |
| WordPress管理系URL（`wp-admin` 等） | ✅ 0件 |

### 軽微な指摘

- `reviews` フォルダが `data/urls.json` に登録されていません（表示への影響なし）
- `sitemap.xml` に `sauna-daigaku.html` が含まれていますが、これは正常です（フォルダではなく単独ファイルのため）

---

## A-8. 外部サービス依存の一覧（移行後も生き続けるか）

| ホスト | 参照数 | 移行後 | 備考 |
|---|---|---|---|
| `fonts.googleapis.com` / `fonts.gstatic.com` | 123 / 61 | ✅ 継続 | Webフォント |
| **`sauna-cospa.com`** | **104** | ⚠️ **要確認** | うち35件がWordPress画像（A-1） |
| `www.googletagmanager.com` | 61 | ✅ 継続 | Google Analytics（G-GTF2GM6DNJ） |
| `www.google.com` | 98 | ✅ 継続 | Googleマップ検索リンク |
| `sauna-ikitai.com` | 59 | ✅ 継続 | 外部リンク |
| `img.travel.rakuten.co.jp` | 14 | ✅ 継続 | 楽天トラベルのホテル写真（外部ホットリンク） |
| `hb.afl.rakuten.co.jp` | 15 | ✅ 継続 | 楽天アフィリエイト |
| `www.amazon.co.jp` | 16 | ✅ 継続 | Amazonアソシエイト |
| `docs.google.com` / `forms.gle` | 3 | ✅ 継続 | 問い合わせフォーム |

> **`sauna-cospa.com` への104件の参照**のうち、大半は `canonical` タグ（正規URL指定）で、
> 移行後も同じドメインを使うため問題ありません。**実害があるのは画像35件のみ**です。

---

# B. 本番側の確認が必要な項目

**ConoHaにアクセスできる方（Codex／Kenjiさん）が実施してください。**
結果をこの文書の該当箇所に追記すれば、調査が完成します。

## B-1. 🔴 本番サーバーのファイル一覧を取得する

**最優先。** GitHubに無いファイルを特定するために必須です。

### 確認方法

ConoHaのファイルマネージャーで `public_html/sauna-cospa.com/` を開き、次を確認します。

- [ ] **`wp-content/uploads/` の中身**（← A-1の35枚がここにある。**最重要**）
- [ ] ルート直下のファイル一覧（`robots.txt`、`favicon.ico`、`.htaccess`、`ads.txt` の有無）
- [ ] HTMLから参照されていない画像・PDFが無いか
- [ ] 総容量（バックアップの計画に必要）

> LIMIT_CHECKPOINT.md の記録では「ルート表示は88項目、902 KB」とあります。
> **902 KBはルート直下のみの数字と思われます。** `wp-content/uploads/` を含めた
> 実際の総容量を確認してください（画像35枚があるため、数十MB以上になる可能性）。

### 記入欄

| 項目 | 結果 |
|---|---|
| `wp-content/uploads/` の画像枚数 | （未記入） |
| うち `2026/07/sauna-univ-*.jpg` | （未記入） |
| ルート直下の総ファイル数 | （未記入） |
| 全体の総容量 | （未記入） |

---

## B-2. 🟡 robots.txt / favicon.ico / ads.txt の有無と中身

### 確認方法

ブラウザで次のURLを開くだけです（ログイン不要）。

```
https://sauna-cospa.com/robots.txt
https://sauna-cospa.com/favicon.ico
https://sauna-cospa.com/ads.txt
```

- 中身が表示される → **その内容をこの文書に記録し、リポジトリに追加する**
- 404が出る → 対応不要（ただし `robots.txt` は新規作成を推奨）

### 記入欄

| ファイル | 本番での有無 | 中身 |
|---|---|---|
| `robots.txt` | （未記入） | （未記入） |
| `favicon.ico` | （未記入） | — |
| `ads.txt` | （未記入） | （未記入） |

---

## B-3. 🟡 .htaccess の中身

### 確認方法

ConoHaのファイルマネージャーで `public_html/sauna-cospa.com/.htaccess` を開きます。
（隠しファイルなので、「隠しファイルを表示」の設定が必要な場合があります）

**中身をそのままこの文書に貼り付けてください。**
`RewriteRule` や `Redirect` の行があれば、移行時に対応が必要です。

### 記入欄

```
（.htaccess の中身をここに貼り付け）
```

| 判定 | 対応 |
|---|---|
| WordPress標準のルールのみ | 対応不要 |
| 手動のリダイレクトがある | 各URLの転送方法を検討（A-4参照） |

---

## B-4. 🟢 公開URLの実地確認

### 確認方法

**GitHubのファイル構成から、本番にあるはずのURL一覧を作れます。**
次の61URLがすべて開けるか確認してください（1つずつでも、まとめてでも構いません）。

主要URLだけ抜粋します。

```
https://sauna-cospa.com/
https://sauna-cospa.com/why/
https://sauna-cospa.com/ランキング/
https://sauna-cospa.com/10項目別ランキング/
https://sauna-cospa.com/reviews/          ← GitHub側のみ。本番には無い可能性
https://sauna-cospa.com/sauna-university/
https://sauna-cospa.com/sauna-daigaku.html
https://sauna-cospa.com/お問い合わせ/
https://sauna-cospa.com/運営者情報/
https://sauna-cospa.com/プライバシーポリシー/
https://sauna-cospa.com/免責事項/
https://sauna-cospa.com/sitemap.xml
```

**特に確認したいこと**

- [ ] `/reviews/` は本番にあるか（GitHubで新設したページ。本番未反映の可能性が高い）
- [ ] `/sauna-app.webmanifest` と `/sauna-icon-180.png` は本番にあるか（PR #3で追加したがConoHa未反映）
- [ ] **GitHubに無いページが本番にあるか**（← これが「不足しているもの」の本体）

### 記入欄

| 確認項目 | 結果 |
|---|---|
| 本番にあってGitHubに無いページ | （未記入） |
| GitHubにあって本番に無いページ | （未記入） |

---

# 移行時の対応案まとめ

優先度順に、いつ何をするかを整理しました。

| 順位 | 対応 | いつ | 誰が |
|---|---|---|---|
| 1 | **ConoHaバックアップに `wp-content/uploads/` を必ず含める** | バックアップ時 | Codex／Kenjiさん |
| 2 | サウナ大学の写真35枚をリポジトリへ移し、URLを書き換える | 不足補完フェーズ | AI（要バックアップ） |
| 3 | 本番の `robots.txt` を確認し、リポジトリへ追加 | 不足補完フェーズ | 要B-2の結果 |
| 4 | 本番の `.htaccess` を確認し、リダイレクト要否を判断 | 不足補完フェーズ | 要B-3の結果 |
| 5 | `/?page_id=37` → `/why/` に書き換え（1箇所） | いつでも可 | AI |
| 6 | `/category/review/` → `/reviews/` に書き換え（1箇所） | いつでも可 | AI |
| 7 | メニューの不揃いを解消（地図の公開方法が決まってから） | 地図の判断後 | 要判断 |
| 8 | `reviews` を `data/urls.json` に登録 | いつでも可 | AI |

> **本調査ではリポジトリのコード・画像を一切変更していません。**
> 上記はすべて「提案」であり、実施は別途ご判断ください。

---

## 本調査で使用した確認コマンド

再現・再検証できるよう、実際に使ったコマンドを残します。

```bash
# WordPress画像への依存を数える
grep -rhoE 'https?://sauna-cospa\.com/wp-content/uploads/[^"'"'"' )]+' --include="*.html" . | sort -u | wc -l

# リポジトリ内の画像・PDFを数える
git ls-files '*.png' '*.jpg' '*.jpeg' '*.gif' '*.svg' '*.webp' '*.ico'
git ls-files '*.pdf'

# WordPress固有URLを探す
grep -rn '?page_id=\|/category/\|/wp-json\|/wp-admin' --include="*.html" .

# ルート直下の設定ファイルの有無
ls -a robots.txt .htaccess favicon.ico ads.txt 2>&1

# 外部ホスト依存の一覧
grep -rhoE 'https?://[a-zA-Z0-9.-]+' --include="*.html" . | sed 's|https\?://||' | sort | uniq -c | sort -rn
```

メニュー整合とリンク切れの確認スクリプトは、実行結果が長いため本文に結果のみ記載しています。
必要であれば同じ手順を再実行できます。

---

## 変更していないもの（確認）

本調査は**読み取り専用**で実施しました。

- ❌ ConoHa：一切アクセスしていません（そもそも到達不可）
- ❌ GAS：変更していません
- ❌ Google Sheets：変更していません
- ❌ 本番サイト：変更していません
- ❌ サイトのHTML・CSS・画像：**1ファイルも変更していません**
- ✅ 追加したのは、この調査文書と最小限のMarkdown更新のみ

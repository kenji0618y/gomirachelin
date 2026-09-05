# gas/ フォルダ

GAS（Google Apps Script）で使うコードを、バックアップと版管理のためにここに置いています。

**このフォルダのファイルはGitHub Pagesのサイト表示には一切関係ありません。**
GASのエディタにコピーして使うためのものです。

---

## ファイル一覧

| ファイル | 内容 | 状態 |
|---|---|---|
| `github_post.gs` | 記事をWordPressではなく**GitHubへ投稿する**モジュール | 🆕 未導入（これから入れる） |

---

## github_post.gs の位置づけ

### 何を置き換えるのか

スマホアプリ（GASの編集アプリ）の流れは、いま次のようになっています。

```
スマホアプリ → スプレッドシート更新 → 記事生成 → 【WordPressに投稿】
```

この **最後の【WordPressに投稿】だけ** をGitHubに差し替えます。

```
スマホアプリ → スプレッドシート更新 → 記事生成 → 【GitHubに投稿】 → 自動で公開
```

**アプリの使い勝手・スプレッドシート・記事生成・校閲は、すべてそのままです。**

### 対応表

| | 今 | これから |
|---|---|---|
| 投稿先 | WordPress REST API | GitHub API |
| 認証情報の置き場所 | スクリプトプロパティ `WP_APP_PASS` | スクリプトプロパティ `GITHUB_TOKEN` |
| 差し替える関数 | `postArticleToCospa(title, html)` | `postArticleToGitHub({slug, title, bodyHtml, ...})` |
| 公開までの手順 | WordPress管理画面で公開日を設定して公開 | **自動**（pushの1〜2分後に反映） |

---

## 導入手順

### ステップ1：GitHubトークンを作る

1. GitHub → 右上のアイコン → **Settings**
2. 左メニューの一番下 → **Developer settings**
3. **Personal access tokens** → **Fine-grained tokens** → **Generate new token**
4. 設定内容：
   - **Token name**：わかる名前（例：`gomirachelin-gas`）
   - **Expiration**：期限。切れると使えなくなるので長めが楽
   - **Repository access**：`Only select repositories` → **gomirachelin** を選ぶ
   - **Permissions** → Repository permissions → **Contents** を **Read and write** にする
     （※これ1つだけでOK。他は触らなくてよい）
5. **Generate token** を押して、表示されたトークンをコピー
   （**この画面を閉じると二度と見られません。すぐ次のステップへ**）

### ステップ2：GASに登録する

1. GASのエディタを開く
2. 左の歯車マーク **プロジェクトの設定**
3. 下の方の **スクリプト プロパティ** → **スクリプト プロパティを追加**
   - プロパティ：`GITHUB_TOKEN`
   - 値：さっきコピーしたトークン
4. **スクリプト プロパティを保存**

> `WP_APP_PASS` を登録したのと同じ場所・同じやり方です。

### ステップ3：コードを追加する

1. GASのエディタで **ファイル** → **＋** → **スクリプト**
2. ファイル名を `github_post` にする
3. `github_post.gs` の中身を全部コピーして貼り付け（Ctrl+A → Ctrl+V）
4. 保存

### ステップ4：接続テスト（何も変更されません）

1. GASのエディタ上部の関数選択で **`testGitHubConnection`** を選ぶ
2. **実行** を押す
3. 初回は権限の確認が出るので許可する
4. **実行ログ**に次のように出れば成功

```
接続OK ✅
リポジトリ : kenji0618y/gomirachelin
書き込み権限: あり ✅
data/urls.json の読み取り: OK ✅
```

うまくいかないときは、ログのエラー内容をそのままAIに見せてください。

### ステップ5：テスト投稿（本番に1本作られます）

1. 関数選択で **`testPostArticle`** を選んで **実行**
2. `https://sauna-cospa.com/test-page/` にテスト記事ができます
   （GitHub Pagesを有効にした後。まだなら、GitHub上にファイルができたことを確認）
3. 確認できたら、GitHubの画面で `test-page` フォルダを削除してください

### ステップ6：既存の投稿処理を差し替える

編集アプリの「投稿」ボタンが呼んでいる `postArticleToCospa(...)` を
`postArticleToGitHub({...})` に変えます。

**この作業はAIに頼んでください。** 既存コードを見ながらでないと正確に直せません。

---

## 主な関数

| 関数 | 何をするか |
|---|---|
| `testGitHubConnection()` | 接続確認。**読み取りだけで何も変更しない**。最初にこれを実行 |
| `testPostArticle()` | テスト記事を1本投稿してみる |
| `postArticleToGitHub(o)` | **記事を投稿する本体。** 記事ページ＋`data/urls.json`＋`sitemap.xml` を1回のコミットで更新 |
| `updateFacilitiesOnGitHub(list)` | ランキングの施設データ（`FACILITIES`）を差し替える |
| `ghPutFiles(files, msg)` | 複数ファイルをまとめて1コミットで書き込む（内部用） |

### postArticleToGitHub の呼び方

```javascript
postArticleToGitHub({
  slug: '神戸サウナ',              // フォルダ名。URLになる
  title: '神戸サウナ',             // 施設名
  bodyHtml: '<p>本文…</p>',        // GASが生成した本文HTML
  description: '神戸／平日¥3100…',  // 検索結果に出る説明（省略可）
  dateText: '2026-08-23'           // 記事に表示する日付（省略時は今日）
});
```

`bodyHtml` には、**今までWordPressに渡していたHTMLをそのまま**渡してください。
上下のヘッダー・フッターはこのモジュールが付けます。

---

## 設計上のポイント

### なぜ「1回のコミット」にまとめているか

記事・`urls.json`・`sitemap.xml` を1つずつ書き込むと、途中で失敗したときに
**中途半端な状態**（記事はあるのにサイトマップに無い等）になります。

`ghPutFiles()` はGitの仕組みを使って、**全部成功するか、何も変わらないか**の
どちらかになるようにしています。

### 検証済みの内容（2026-09-04）

- ✅ 構文エラーなし（`node --check`）
- ✅ 生成されるHTMLの骨格が既存記事と**完全一致**
- ✅ ナビ・フッターのリンクが既存記事と一致
- ✅ ブラウザで表示して黒×金のデザインが崩れないことを確認

### 注意点

- **日本語のフォルダ名**を扱います。GitHub APIはUTF-8のパスに対応していますが、
  投稿後は必ず実際のURLが開けるか確認してください
- `updateFacilitiesOnGitHub()` は `var FACILITIES = [...];` という書き方を
  前提にしています。ランキングページの作りを変えるときは、この関数も直す必要があります
- **トークンは絶対にコードに書かないこと。** スクリプトプロパティに入れてください

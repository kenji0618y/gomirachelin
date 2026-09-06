# AI引き継ぎ

最終更新：2026-09-06 12:30

このファイルは、Codex、Claude、Geminiなど複数のAIで作業するときに、会話だけでは失われる重要事項を共有するための記録です。

## 2026-09-06 12:30 Codex フェーズ2基本ファイル反映

- GitHub mainへ `docs/フェーズ2_補完整理計画.md`、`.nojekyll`、`robots.txt`、`404.html` を追加した。
- `index.html` の大きなWHYボタンを `/?page_id=37` から `/why/` へ変更。コミット `104896e` は1行追加・1行削除だけと確認済み。
- 関連コミット：`9419faa`、`18891a2`、`72a655c`、`104896e`。`404.html` もmainルートで存在確認済み。
- ConoHa、DNS、GAS、Sheets、`CNAME` は未変更。独自ドメイン切替も未実施。
- 次の1手は、サウナ大学のConoHa画像35件をGitHub内へ移す準備。その後、一般公開できる地図方式を決める。

## 2026-09-06 12:10 Codex DB保存完了

- phpMyAdminからDB `yux6k_54n7x7hu` をQuick / SQLで保存した。4,674,654 bytes、18テーブル、INSERT文103件、エラーHTML混入0件。
- SQL本体とSHA-256一覧はGitHubへ入れず、ローカルの `backups/conoha/2026-09-05/database/` に保存した。
- Web主要データとSQLが揃い、復旧可能なバックアップは成立。未取得10項目は完全スナップショットとの差として継続記録する。
- 次は公開サイトとGitHubの差分をフェーズ2の追加・整理候補へ落とし込む。地図の一般公開方法が公開前ブロッカー。
- ConoHa本番、DNS、DB内容、GASは変更していない。

## 2026-09-06 07:45 Codex再開

- GrokのGitHub main（`7964baf`）をZIPで取得し、別フォルダーへ展開して引き継いだ。
- ConoHa分割ZIPを統合解凍。8,450ファイル、189,625,554 bytes、内容衝突0件。`manifest.csv` に元ZIPのSHA-256を保存。
- `wp-content/uploads` 440ファイル、サウナ大学の元画像45枚を確認。
- Grokの「Web保存完了」は主要データについて正しいが、ルート88項目のうち10項目が未取得。施設5フォルダーとルート5ファイルを追加取得する。
- 次の1手はConoHa再ログイン後のDB SQLエクスポート。その後に残り10項目を取得する。
- ConoHa本番、DNS、DB、GASは変更していない。

## 2026-09-06 00:30 Grok 会話中断

- 利用者は寝に就くため作業中断。次回は `docs/LIMIT_CHECKPOINT.md` と `docs/STATE追記_2026-09-06.md` から再開する。
- Web手元保存は完了と報告。一括zipは504だったため、`wp-content` / `wp-includes` / `wp-admin` / 残りの順で分割した。
- DBエクスポート未実施。次の1手はphpMyAdminのクイックSQLエクスポート。
- リストア、本番変更、DNS変更はしていない。
- サーバー名 `wing-26-06-14-21-29`。自動バックアップは2026-08-22〜09-04がリストア可。

## 2026-09-05 Grok継続（公開情報だけ確認した分）

- 公開A: 157.120.209.148。MX: mail1004.conoha.ne.jp。NS: ns-a1/a2/a3.conoha.io。SPF: include:_spf.conoha.ne.jp。
- 本番 `/reviews/` は404。`robots.txt` も404。
- GitHubに `gas/` は無い。
- 詳細: `docs/公開サイトとGitHubの差分.md` / `docs/dns-mail-公開記録.md`

## 2026-09-05 ConoHaバックアップ開始

- 保存先 `gomirachelin-work/backups/conoha/2026-09-05/`。WordPress実体はGitHubへ入れない。
- ConoHa上のファイル、DB、DNS、メール、契約は変更していない。

## 2026-09-05 利用制限への対応

- 全AI共通ルールの正文は `AGENTS.md`。

## 2026-09-05 Claude / Codex

- GAS地図v91。未ログインではGoogleログイン画面。
- Claudeブランチ全体はマージしない。PR #3の2ファイルのみ取り込み済み。

## 共通の更新方法

- 作業前に `AGENTS.md` と `docs/STATE.md` を読む。
- 作業後に `docs/STATE.md` を更新する。

## フェーズ2開始（2026-09-06 Codex）

- `docs/フェーズ2_補完整理計画.md` を作成した。次は `.nojekyll`、`404.html`、`robots.txt`、トップのWHYリンク修正を準備する。
- サウナ大学はConoHa画像35枚を参照中。元画像45枚はバックアップ済みなので、GitHub内画像への移行が可能。
- GAS地図は未ログインで開けないため、方式決定前に全ページへメニュー展開しない。
- `CNAME`、DNS、ConoHa本番、フォルダー削除は未変更。

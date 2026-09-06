# AI引き継ぎ

最終更新：2026-09-06 00:30

このファイルは、Codex、Claude、Geminiなど複数のAIで作業するときに、会話だけでは失われる重要事項を共有するための記録です。

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

## 2026-09-05 Claude：Codex利用制限中の小さな修正

- Codexが利用制限に達したため、Kenjiさんの指示でClaudeが続きを担当。ConoHaへのログイン操作はClaudeにはできない（ブラウザ操作の手段がない）旨を伝え、「ConoHaに触れない安全なGitHub作業を先に進める」ことで合意した。
- PR #4（未マージ）で見つけた即修正可能な2件を実施：`index.html` の `/?page_id=37`→`/why/`、`sauna-daigaku.html` の `/category/review/`→`/reviews/`（本文中はabsolute URL形式のまま維持）。
- `reviews` を `data/urls.json` に登録。`robots.txt` を最小構成で新規作成（本番の実際の内容はPR #4のB-2で要確認、判明したらそちらを優先）。
- **Codexへの申し送りは変わらず最優先**：ConoHaバックアップに `wp-content/uploads/` を含めること（サウナ大学の写真35枚がここにしかない）。
- 新ブランチ `claude/small-fixes-and-migration-prep` で作業。PR作成後マージはKenjiさんの判断を仰ぐ。ConoHa、GAS、Google Sheets、本番サイトは未変更。

## 2026-09-05 Claude：PR #5とmainの衝突を解消

- Grokが会話再開後にConoHaへ再ログインし、Web手元保存を完了させ（`wing-content`等を分割ダウンロード）、`docs/LIMIT_CHECKPOINT.md`等をmainへ反映したため、Claudeが作業中のPR #5ブランチ（`claude/small-fixes-and-migration-prep`）とmainの間で `docs/LIMIT_CHECKPOINT.md` に衝突が発生した。
- mainを取り込んでマージし、衝突を解消（コミット`2bc61a7`）。Grok側の最新状況（Web手元保存完了、DB未実施、次の1手はphpMyAdmin）を残しつつ、Claude側が記録していたphpMyAdmin接続タイムアウトの詳細（原因の推測、未実施の切り分け方法、パスワード関連の安全上の注意）も「phpMyAdmin接続問題の記録」として残した。
- **重要**：phpMyAdminのSQLエクスポートは、Grok側の記録でもまだ「次の1手」のままで未完了。Claudeのセッションで発生した接続タイムアウト（`phpmyadmin2003.conoha.ne.jp`が`ERR_CONNECTION_TIMED_OUT`）が解消しているかどうかは未確認。次にこの作業を再開するAI・利用者は、まずこの問題が起きていないか確認すること。
- ConoHa、GAS、Google Sheets、本番サイトはClaude側では変更していない。PR #4・PR #5は引き続き未マージ（「マージせず止めて」の指示継続中）。

## 共通の更新方法

- 作業前に `AGENTS.md` と `docs/STATE.md` を読む。
- 作業後に `docs/STATE.md` を更新する。


## 2026-09-06 07:45 Codex再開

- Grokのmain `7964baf` を取得して引き継いだ。
- ConoHa分割ZIPを統合解凍。8,450ファイル、189,625,554 bytes、内容衝突0件。元ZIPのSHA-256一覧も保存済み。
- `wp-content/uploads` 440ファイル、サウナ大学の元画像45枚を確認。
- Web主要データは保存済みだが、ルート88項目のうち10項目が未取得。施設5フォルダーとルート5ファイルを追加取得する。
- 次の1手はConoHa再ログイン後のDB SQLエクスポート。その後に残り10項目を取得する。
- ConoHa本番、DNS、DB、GASは変更していない。


## 2026-09-06 12:10 Codex DB保存完了

- DB `yux6k_54n7x7hu` をQuick / SQLで保存。4,674,654 bytes、18テーブル、INSERT文103件、エラーHTML混入0件。
- SQL本体とSHA-256一覧はGitHubへ入れず、ローカルの `backups/conoha/2026-09-05/database/` に保存した。
- Web主要データとSQLが揃い、復旧可能なバックアップは成立。次はフェーズ2「GitHub補完・整理」。
- 地図の一般公開方法が公開前ブロッカー。ConoHa本番、DNS、DB内容、GASは変更していない。

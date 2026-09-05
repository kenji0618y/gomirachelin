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

## 共通の更新方法

- 作業前に `AGENTS.md` と `docs/STATE.md` を読む。
- 作業後に `docs/STATE.md` を更新する。

# 利用制限前チェックポイント

最終更新：2026-09-06 00:30 JST前後（Codex）＋2026-09-05 Claudeのメモを統合

状態：会話中断（利用者が寝に就く）。緊急の未完了操作なし。

## 現在の作業

- フェーズ1「ConoHaの棚卸しとバックアップ」。
- Webファイルの手元保存は利用者が完了と報告。DB・管理画面のDNS/メール追記は未実施。
- **DBのSQLエクスポート（phpMyAdmin）はまだ完了していない**。Claudeのセッションでは、ConoHaコントロールパネル経由・直接URLともに`phpmyadmin2003.conoha.ne.jp`が`ERR_CONNECTION_TIMED_OUT`でタイムアウトする問題が発生していた（下記「phpMyAdmin接続問題の記録」参照）。次にこの作業を再開する際は、まずこの問題が解消しているかを確認すること。

## 最後に完了した操作

- ConoHa再ログイン。サーバー `wing-26-06-14-21-29`。
- 自動バックアップ 2026-08-22〜2026-09-04、Web/Mail/DB全日リストア可。リストア未実行。
- ファイルマネージャーで `public_html/sauna-cospa.com` を確認（88項目、この階層表示902 KB）。`reviews` と `robots.txt` は無い。
- フォルダ一括ダウンロードはHTTP 504。`wp-content` → `wp-includes` → `wp-admin` → 残りの順で分割ダウンロードし、利用者が完了と報告。
- 手元保存先の目安: `gomirachelin-work/backups/conoha/2026-09-05/web/`
- 本番の削除・上書き・リストア・DNS変更はしていない。
- （Claude側）`index.html`、`sauna-daigaku.html`、`data/urls.json`、`robots.txt`の4ファイル修正をPR #5として作成（未マージ）。PR #4・PR #5とも複数回状態確認しているが、レビュー・コメント0件で変化なし。「マージせず止めて」の指示が継続中。

## phpMyAdmin接続問題の記録（Claude、2026-09-05）

- ConoHaコントロールパネルの「データベース」画面→「管理ツール」欄の`phpMyAdmin`リンクをクリックしても、直接URL入力でも、`phpmyadmin2003.conoha.ne.jp`が`ERR_CONNECTION_TIMED_OUT`でタイムアウトした。
- 原因はConoHa側ではなく、利用者のネット回線・PC側（セキュリティソフト、ルーター等が該当ドメインをブロックしている可能性）と推測。ConoHa側の障害は未確認。
- 提案したが**Claudeのセッション終了時点では未確認**の切り分け方法：①スマートフォンのモバイル回線で同じリンクを試す、②PCのセキュリティソフトを一時確認、③別のブラウザで試す。
- 代替案：手動SQLエクスポートにこだわらず、ConoHaの「自動バックアップ」機能（Web/Mail/DB全日リストア可と確認済み）で十分とする案も提示した。
- DBユーザー名`yux6k_x6j43h66`のパスワードは利用者が確認済み。**パスワードやSQLダンプの中身はこのMarkdownにもチャットにも記録していない**（安全のため）。

## 外部サービスの状態

- GitHub: 本チェックポイントと引き継ぎを更新。PR #4（調査文書のみ）、PR #5（小さな安全修正）とも未マージのまま open。
- ConoHa: ログイン済み。サーバー上のファイル・DBは未変更。
- GAS v91 / Sheets: 変更なし。

## 未保存作業

- なし（GitHubへ上げる本番ファイルの途中編集なし）。
- WordPress実体はGitHubに入れない。

## 次の1手

1. phpMyAdminへ接続できるか再確認する（上記の切り分け方法を試す）。接続できたら現行DBをSQLエクスポートし、`.../database/` へ保存する。
2. 手元webに `wp-config.php`、`.htaccess`、`wp-content/uploads` があるか目視する。
3. ConoHaのドメイン・DNS・メール画面を追記する。

## 戻し方

- ConoHa本番はそのまま。手元ファイルを消しても公開サイトは残る。
- リストアしていないので、`backup_data_web` の後処理は不要。
- バックアップが完成するまで、ConoHaの削除・移動・上書き、DNS変更、解約を行わない。
- DBユーザーのパスワードリセット（鉛筆マーク）は絶対に使わない。本番WordPressのDB接続が壊れるリスクがあるため。
- wp-config.phpは閲覧のみで、保存・上書きしない。
- 地図が未ログインで開けるようになるまで、本番メニューへ地図リンクを追加しない。
- 問題が起きた場合はConoHa本番をそのまま維持し、GitHub側の変更だけを見直す。

## 2026-09-06 07:50 Codexチェックポイント

- Web主要データは `web/extracted/sauna-cospa.com/` へ解凍済み。8,450ファイル、189,625,554 bytes、同名内容の衝突0件。
- `wp-content/uploads` 440ファイル、サウナ大学元画像45枚を確認済み（PR #4で最優先と申し送りしていた項目）。
- Web残り10項目とDB SQLが未取得。次はConoHaへ再ログインし、phpMyAdminからDBをエクスポートする。
- 本番、DNS、DB、GASは変更していない。
- `docs/STATE.md` と `docs/AI引き継ぎ.md` はGitHub mainへ更新済み。

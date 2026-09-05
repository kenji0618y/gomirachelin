# ConoHaバックアップ手順

最終更新：2026-09-06 00:30

対象：`sauna-cospa.com`

保存先：`gomirachelin-work/backups/conoha/2026-09-05/`

## 進捗（2026-09-06卌前）

- [済] 自動バックアップ一覧の確認（リストアはしない）
- [済] ファイルマネージャーで `public_html/sauna-cospa.com` を確認
- [済] Webを分割ダウンロード（一括は504）。利用者が完了と報告
- [未] phpMyAdminでSQLエクスポート
- [未] 手元ファイルの目視（`wp-config.php` / `.htaccess` / `uploads`）
- [未] 管理画面のDNS・メール・契約の追記

## 基本方針

- 確認とダウンロードだけを行う。
- ConoHa上の削除、移動、上書き、復元、DNS変更、解約は行わない。
- WordPressのバックアップは秘密情報を含む可能性があるためGitHubへ入れない。

## 次回の順番

1. 「サイト管理 → データベース」でDB名を確認する。
2. phpMyAdminから対象DBをクイック・SQLで `database/` へエクスポートする。インポートはしない。
3. 手元 `web/` に `wp-config.php`、`.htaccess`、`wp-content/uploads` があるか確認する。
4. DNS・メール・契約画面を `dns-mail/` へ追記する。
5. `docs/STATE.md` とロードマップを更新する。

## 注意点

- 自動バックアップは過去14日分。Web/Mailリストア結果は24時間で消える。
- ファイルマネージャーのフォルダ一括は504になりやすい。分割かFTPを使う。
- `wp-config.php`、SQL、パスワードはチャットに貼らない。

## 完了条件

- `web/` に公開フォルダーのバックアップがある。
- `database/` に開けるSQLがある。
- `dns-mail/` に切替前のDNS・メール・契約情報がある。

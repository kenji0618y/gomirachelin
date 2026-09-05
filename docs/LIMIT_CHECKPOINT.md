# 利用制限前チェックポイント

最終更新：2026-09-06 00:30 JST前後

状態：会話中断（利用者が寝に就く）。緊急の未完了操作なし。

## 現在の作業

- フェーズ1「ConoHaの棚卸しとバックアップ」。
- Webファイルの手元保存は利用者が完了と報告。DB・管理画面のDNS/メール追記は未実施。

## 最後に完了した操作

- ConoHa再ログイン。サーバー `wing-26-06-14-21-29`。
- 自動バックアップ 2026-08-22〜2026-09-04、Web/Mail/DB全日リストア可。リストア未実行。
- ファイルマネージャーで `public_html/sauna-cospa.com` を確認（88項目、この階層表示902 KB）。`reviews` と `robots.txt` は無い。
- フォルダ一括ダウンロードはHTTP 504。`wp-content` → `wp-includes` → `wp-admin` → 残りの順で分割ダウンロードし、利用者が完了と報告。
- 手元保存先の目安: `gomirachelin-work/backups/conoha/2026-09-05/web/`
- 本番の削除・上書き・リストア・DNS変更はしていない。

## 外部サービスの状態

- GitHub: 本チェックポイントと引き継ぎを更新。
- ConoHa: ログイン済み。サーバー上のファイル・DBは未変更。
- GAS v91 / Sheets: 変更なし。

## 未保存作業

- なし（GitHubへ上げる本番ファイルの途中編集なし）。
- WordPress実体はGitHubに入れない。

## 次の1手

1. phpMyAdminで現行DBをSQLエクスポートし、`.../database/` へ保存する。
2. 手元webに `wp-config.php`、`.htaccess`、`wp-content/uploads` があるか目視する。
3. ConoHaのドメイン・DNS・メール画面を追記する。

## 戻し方

- ConoHa本番はそのまま。手元ファイルを消しても公開サイトは残る。
- リストアしていないので、`backup_data_web` の後処理は不要。


## 2026-09-06 07:50 Codexチェックポイント

- Web主要データは `web/extracted/sauna-cospa.com/` へ解凍済み。8,450ファイル、189,625,554 bytes、同名内容の衝突0件。
- `wp-content/uploads` 440ファイル、サウナ大学元画像45枚を確認済み。
- Web残り10項目とDB SQLが未取得。次はConoHaへ再ログインし、phpMyAdminからDBをエクスポートする。
- 本番、DNS、DB、GASは変更していない。
- `docs/STATE.md` と `docs/AI引き継ぎ.md` はGitHub mainへ更新済み。

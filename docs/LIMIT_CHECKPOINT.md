# 利用制限前チェックポイント

最終更新：2026-09-05

状態：通常。緊急の未完了作業なし。

## 現在の作業

- 全体ロードマップのフェーズ1「ConoHaの棚卸しとバックアップ」を進行中。
- ConoHaの対象ドメインは `sauna-cospa.com`。
- ファイルマネージャーで `public_html/sauna-cospa.com` を読み取り確認済み。ルート表示は88項目、902 KB。WordPressの `wp-admin`、`wp-content`、`wp-includes` が存在する。

## 最後に完了した操作

- AI共通ルールを `AGENTS.md` へ一元化し、利用制限前の保存ルールを追加してGitHubのmainへ反映した。
- Claude用とGemini用のファイルは `AGENTS.md` を読み込む1行だけにした。GrokとCursorの専用ファイルは不要なため削除した。
- PR #3をmainへマージし、`sauna-app.webmanifest` と `sauna-icon-180.png` を追加した。
- GitHub側の既知のリンク切れ2件を解消した。
- Claudeブランチ全体はマージしていない。

## 外部サービスの状態

- GitHub：PR #3に加え、AIルール一元化と本チェックポイント文書をmainへ反映済み。AIルールの変更は直接コミットで、未保存作業なし。
- ConoHa：ログインして読み取り確認しただけ。ファイル、WordPress、DNS、メール設定は未変更。バックアップのダウンロードは未実施。
- GAS：地図v91。未ログインではGoogleログイン画面になるため、一般公開方法は未解決。
- Google Sheets：変更なし。

## 次の1手

1. ConoHaの `public_html/sauna-cospa.com` 全体を安全にバックアップする方法と容量を確認する。
2. WordPressデータベースのバックアップ場所を確認する。
3. DNS、MX、TXTの現在値を記録する。

## 中止・復旧条件

- バックアップが完成するまで、ConoHaの削除・移動・上書き、DNS変更、解約を行わない。
- 地図が未ログインで開けるようになるまで、本番メニューへ地図リンクを追加しない。
- 問題が起きた場合はConoHa本番をそのまま維持し、GitHub側の変更だけを見直す。

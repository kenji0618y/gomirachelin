# 利用制限前チェックポイント

最終更新：2026-09-06 22:06 JST前後

状態：フェーズ2進行中。WebとDBの復旧用バックアップ、サウナ大学画像移行、ログイン不要の静的地図準備まで完了。

## 2026-09-06 静的地図追加チェックポイント（Codex）

- GitHubへ反映する変更：新規 `map/index.html`、`map/MAP-LICENSE.txt`、トップ `index.html` の地図リンク、関連MarkdownとロードマップHTML。
- 検証済み：47都道府県、重複除外174施設、閉店記録3件、座標あり54施設、`google.script.run` 0件、FILTER欄0件。ローカルブラウザーで地図表示済み。
- 外部サービス：ConoHa、DNS、GAS v91、Google Sheets、`CNAME` は変更していない。
- 次の1手：コミットをGitHub mainへpushし、差分を確認する。その後GitHub Pagesの公開方式を確認する。
- 戻し方：この地図追加コミットをrevertする。公開中のConoHaサイトとGAS v91には影響しない。

## 現在の作業

- フェーズ1「ConoHaの棚卸しとバックアップ」。
- Web主要データとDB SQLを手元保存し、ハッシュ記録・構造確認まで完了。完全スナップショットとの差10項目は記録済み。

## 最後に完了した操作

- ConoHa再ログイン。サーバー `wing-26-（サーバー名・伏せ字）`。
- 自動バックアップ 2026-08-22〜2026-09-04、Web/Mail/DB全日リストア可。リストア未実行。
- 分割ZIPを `gomirachelin-work/backups/conoha/2026-09-05/web/` に保存し、`manifest.csv` にSHA-256を記録。
- `web/extracted/sauna-cospa.com/` へ統合解凍。8,450ファイル、189,625,554 bytes、同名内容の衝突0件。
- `wp-content/uploads` 440ファイル、サウナ大学の元画像45枚を確認。
- ConoHaルート88項目のうち78項目を保存。施設5フォルダーとルート5ファイルはZIPに含まれておらず、追加取得が必要。
- 本番の削除・上書き・リストア・DNS変更はしていない。

## 外部サービスの状態

- GitHub: 本チェックポイントと引き継ぎを更新。
- ConoHa: セッション期限切れ。サーバー上のファイル・DBは未変更。
- GAS v91 / Sheets: 変更なし。

## 未保存作業

- なし（GitHubへ上げる本番ファイルの途中編集なし）。
- WordPress実体はGitHubに入れない。

## 次の1手

1. `docs/公開サイトとGitHubの差分.md` をフェーズ2の追加・整理候補へ反映する。
2. 一般訪問者がログインせず開ける地図方式を決める。
3. GitHub Pagesのテスト公開に必要な不足ファイルを小分けで補う。

## 戻し方

- ConoHa本番はそのまま。手元ファイルを消しても公開サイトは残る。
- リストアしていないので、`backup_data_web` の後処理は不要。

## 2026-09-06 フェーズ2開始チェックポイント（Codex）

- フェーズ1のWeb・DBバックアップは完了。現在はフェーズ2「GitHub補完・整理」。
- `docs/フェーズ2_補完整理計画.md` を作成し、次の1手をPages基本ファイルとWHYリンク修正に決定。
- 外部サービス変更なし。ConoHa、DNS、GAS、Google Sheetsは未変更。
- 次回は `.nojekyll`、`404.html`、`robots.txt`、`index.html` の修正案を作成し、表示とリンクを確認する。
- 戻し方：この時点ではMarkdownだけの追加・更新なので、該当追記と新規計画書を戻せばよい。

## 2026-09-06 フェーズ2基本ファイル反映後チェックポイント（Codex）

- GitHub mainへ `docs/フェーズ2_補完整理計画.md`、`.nojekyll`、`robots.txt`、`404.html` を追加済み。
- `index.html` の大きなWHYボタンを `/why/` へ変更済み。コミット `104896e` は差分1行だけと確認した。
- 関連コミット：`9419faa`、`18891a2`、`72a655c`、`104896e`。`404.html` はmainルートに存在する。
- 未保存のGitHub編集画面はない。ConoHa、DNS、GAS、Google Sheets、`CNAME` は未変更。
- 次の1手：バックアップ済みのサウナ大学元画像45枚から、実際に参照中の35件をGitHub用に準備し、HTML参照先を小分けで変更する。
- 戻し方：GitHubの該当コミットを個別にrevertする。独自ドメインは未切替なので、現在のConoHa公開サイトには影響しない。

## 2026-09-06 サウナ大学画像準備チェックポイント（Codex）

- ローカル準備完了：`assets/images/sauna-university/` に画像35枚と `manifest.csv`。合計8,127,222 bytes、破損0件。
- ローカルの `sauna-daigaku.html` は旧ConoHa画像URL35件をGitHub内パスへ変更済み。旧URL残り0件。
- GitHub未反映：画像35枚、`manifest.csv`、HTML修正版。
- ブロッカー：Chrome拡張機能のファイルURL権限が無効で `fileChooser.setFiles` が拒否された。
- 次の1手：Chrome拡張機能の「ファイルのURLへのアクセスを許可する」をオンにする。画像を先にアップロードし、確認後にHTMLを反映する。
- ConoHa、DNS、GAS、Google Sheets、`CNAME` は未変更。

## 2026-09-06 サウナ大学画像移行完了チェックポイント（Codex）

- GitHub mainへ画像35枚と `manifest.csv` を追加済み（`146bfa6`）。フォルダー画面で36ファイルを確認した。
- `sauna-daigaku.html` の旧ConoHa画像URL 35件をGitHub内パスへ変更済み（`0f89c3b`）。差分は1ファイル・35行追加・35行削除。
- 未保存のGitHub編集はない。ローカルの画像・HTML・記録文書は保持している。
- ConoHa、DNS、GAS、Google Sheets、`CNAME` は未変更。
- 次の1手：未ログインで利用できる地図方式を決め、GitHub Pagesのテスト公開へ進む。
- 戻し方：`0f89c3b` をrevertしてHTML参照だけ旧ConoHa URLへ戻す。

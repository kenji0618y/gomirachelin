# AI引き継ぎ

最終更新：2026-09-05

このファイルは、Codex、Claude、Geminiなど複数のAIで作業するときに、会話だけでは失われる重要事項を共有するための記録です。

## 2026-09-05 Grok継続（ConoHa未ログインで進めた分）

- 次の1手はConoHaバックアップだが、再ログインが要るため本番バックアップは未実施。
- 代わりに公開DNSと生産HTTPを確認し、`docs/公開サイトとGitHubの差分.md` と `docs/dns-mail-公開記録.md` を追加した。
- 公開A: 157.120.209.148。MX: mail1004.conoha.ne.jp。NS: ns-a1/a2/a3.conoha.io。SPF: include:_spf.conoha.ne.jp。
- 生産 `/reviews/` は404。`robots.txt` も404。トップの「レビュー一覧を見る」は `/reviews/` 向きのまま。
- GitHubに `gas/` は無い。
- 生産へのアップロードはしていない。

## 2026-09-05 ConoHaバックアップ開始

- 全体ロードマップの現在地はフェーズ1「ConoHaの棚卸しとバックアップ」。
- ローカル保存先 `gomirachelin-work/backups/conoha/2026-09-05/` と `docs/ConoHaバックアップ手順.md` を準備済み。WordPressバックアップは秘密情報を含むためGitHubへ入れない。
- ConoHaのログイン期限が切れ、現在はログイン画面。利用者が再ログインしたら、自動バックアップ確認、DB書き出し、Webデータ取得、DNS・メール記録の順で続行する。
- ConoHa上のファイル、データベース、DNS、メール、契約設定は変更していない。

## 2026-09-05 利用制限への対応

- 利用者は、突然利用制限に達してもGrok、Claude、Gemini、Codexが作業を継続できることを最優先で希望している。
- 全AIは `AGENTS.md` の利用制限ルールに従う。
- 全AI共通ルールの唯一の正文は `AGENTS.md`。

## 2026-09-05 Claudeセッションからの引き継ぎ

確認元：Claude Codeセッション `session_012z7Kpw3eTFZuubAjTQe91B`

- Claude側の作業ブランチは `claude/grok-stopped-tznre4` で、PR #2はmainへマージ済みと報告されている。
- サイト構成の方針は「GitHubの静的サイトとGASバックエンドを当面併用する」。
- GASの公開設定は利用者本人のみ。
- 主な不足は、現在公開中のGAS本体ソースがGitHubに完全保存されていないことと、Google Sheetsの全データがGitHubに保存されていないこと。
- 未解決事項は、10評価項目の定義差（⑤・⑦・⑧）、独自ドメイン管理先の確認、GitHubリポジトリを公開にするか非公開のままにするか。

## 2026-09-05 Codex地図作業

- 公開中のGAS地図はバージョン91。
- GitHubのトップへ「サウナ地図」追加済み。ConoHa本番への反映は未実施。

## 2026-09-05 Claude再確認後のCodex検証

- 未ログインでGAS地図URLを開くとGoogleログイン画面になる。
- Claudeブランチ全体はそのままマージしない。

## 2026-09-05 Claudeとの選択統合

- PR #3で `sauna-app.webmanifest` と `sauna-icon-180.png` のみmainへマージ済み。
- ConoHa本番は未変更。

## 共通の更新方法

- 作業前に `AGENTS.md` と `docs/STATE.md` を読む。
- 作業後に `docs/STATE.md` を更新する。
- 他のAIの会話で重要な決定や未完了作業が分かった場合は、このファイルへ追記する。

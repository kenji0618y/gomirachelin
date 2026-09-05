# AI引き継ぎ

最終更新：2026-09-05

このファイルは、Codex、Claude、Geminiなど複数のAIで作業するときに、会話だけでは失われる重要事項を共有するための記録です。

## 2026-09-05 利用制限への対応

- 利用者は、突然利用制限に達してもGrok、Claude、Gemini、Codexが作業を継続できることを最優先で希望している。
- 全AIは `AGENTS.md` の利用制限ルールに従う。残り約20%以下、コンテキスト約80%以上、警告表示時は新しい作業を止める。
- `docs/STATE.md` と `docs/LIMIT_CHECKPOINT.md` を先に更新し、現在の作業、外部変更、ブランチ・コミット・PR、未保存作業、次の1手、戻し方を残す。
- 外部サービス変更やPR作成・マージの直後にも記録し、セッション終了まで先送りしない。
- 全AI共通ルールの唯一の正文は `AGENTS.md`。Claude用 `CLAUDE.md` は `@AGENTS.md`、Gemini用 `GEMINI.md` は `@./AGENTS.md` の1行だけで正文をimportする。GrokとCursorは `AGENTS.md` を直接読むため専用ファイルを置かない。
- この一元化と `docs/LIMIT_CHECKPOINT.md` はGitHubのmainへ反映済み。今後、共通ルールを変えるときは `AGENTS.md` だけを編集する。

## 2026-09-05 Claudeセッションからの引き継ぎ

確認元：Claude Codeセッション `session_012z7Kpw3eTFZuubAjTQe91B`

- Claude側の作業ブランチは `claude/grok-stopped-tznre4` で、PR #2はmainへマージ済みと報告されている。
- `gas/github_post.gs`、`gas/README.md`、`docs/GASとGitHubの役割分担.md`、`docs/STATE.md`、`AGENTS.md` などを整備したと報告されている。GitHub上の最新版を取得するときに実在と内容を再確認する。
- サイト構成の方針は「GitHubの静的サイトとGASバックエンドを当面併用する」。GitHub一本化自体を目的にせず、運用費と保守性を見ながら段階的に進める。
- GASの公開設定は利用者本人のみ。過去の「GASを廃止する」という記録は現在の方針と一致しない。
- 主な不足は、現在公開中のGAS本体ソースがGitHubに完全保存されていないことと、Google Sheetsの全データがGitHubに保存されていないこと。
- GASは不要な再デプロイを避け、実際のHTML/CSSを確認してから一度ずつ小さく変更する。
- 未解決事項は、10評価項目の定義差（⑤・⑦・⑧）、独自ドメイン管理先の確認、GitHubリポジトリを公開にするか非公開のままにするか。

## 2026-09-05 Codex地図作業

- 公開中のGAS地図は、2026-09-05 0:17にバージョン90へ更新済み。
- バージョン90では、都道府県境界を実地図で表示し、各県の数字を本サイトの掲載施設数に修正した。
- バージョン91でFILTER欄を削除し、県境と施設ピンを1枚の地図へ統合した。縮尺9以上で施設ピンを表示し、ピンからGoogleマップと公式サイトを開ける。公開画面で確認済み。
- GitHubのトップページのメインメニューへ「サウナ地図」を追加し、コミット `1f2cad1` でmainへ反映した。ConoHaの公開サイトへの反映は未実施。
- 作業バックアップはローカルの `gomirachelin-work/map-fix/` にある。公開後はGAS本体ソースをGitHubの `gas/` に保存することが望ましい。

## 2026-09-05 Claude再確認後のCodex検証

- 未ログイン状態のアプリ内ブラウザーでGAS地図URLを開くと、地図ではなくGoogleログイン画面になった。現状では一般訪問者は地図を開けない。
- GitHub mainの地図リンクはトップ `index.html` だけにあり、ConoHa本番には未反映。公開方法が決まるまで本番メニューへ反映しない。
- `main...claude/grok-stopped-tznre4` の比較は7コミット・85ファイルで、自動マージ不可と表示された。
- Claudeブランチには、利用者が撤回したHTMLサイトマップを全ページへ追加する変更と、切替前の `CNAME` が含まれるため、ブランチ全体はそのままマージしない。
- 個別に取り込む候補は、2件のリンク修正、`sauna-app.webmanifest`、`sauna-icon-180.png`、`404.html`、必要性を確認後の `.nojekyll`、内容を再確認したドキュメント。
- `gas/github_post.gs` はGitHub書き込み権限を持つトークンを使うため、現在のGAS本体と投稿運用を確認してから別作業で安全性と失敗時の復旧を検証する。
- 判断と理由: 丸ごとマージではなく選択統合にする。撤回済み機能、時期尚早なDNS設定、現在の方針と異なる古い記録をmainへ混ぜないため。

## 2026-09-05 Claudeとの選択統合

- Claudeへ読み取り確認を依頼し、「リンク切れ2件」は `sauna-daigaku.html` が参照する `sauna-app.webmanifest` と `sauna-icon-180.png` の不足そのものだと確認した。
- Claudeが最新mainから `claude/fix-sauna-daigaku-404-assets` を作成し、この2ファイルだけを追加するPR #3を作成。CodexがGitHubの差分を再確認してmainへマージした。
- PR #3は新規2ファイル、既存ファイル変更0件、1コミット、競合なし。`CNAME`、`.nojekyll`、`404.html`、サイトマップ、`gas/github_post.gs` は含めていない。
- 黒×金のGアイコンはClaudeが作成した代替品。元のアイコンが見つかった場合は差し替え可能。
- `404.html` は `/サイトマップ/` へのリンクを3か所含み、現在のConoHaでは自動適用されない。GitHub Pages方式が決まるまで保留する。
- ConoHa本番は未変更。GitHub側だけでリンク切れ2件が解消した。

## 共通の更新方法

- 作業前に `AGENTS.md` と `docs/STATE.md` を読む。
- 作業後に `docs/STATE.md` を更新する。
- 他のAIの会話で重要な決定や未完了作業が分かった場合は、このファイルへ追記する。

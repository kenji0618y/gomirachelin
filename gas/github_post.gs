/**
 * github_post.gs
 * ============================================================
 * GOMIRACHELIN — 記事をWordPressではなくGitHubへ投稿するためのモジュール
 * ============================================================
 *
 * 【これは何？】
 *   今まで postArticleToCospa() が WordPress に下書きを投稿していました。
 *   その代わりに、GitHubリポジトリへ直接ファイルを作るのがこのファイルです。
 *   GitHubに置かれたファイルは、GitHub Pagesが自動でサイトに公開します。
 *
 * 【使う前の準備（1回だけ）】
 *   1. GitHubでトークンを作る（下の「トークンの作り方」参照）
 *   2. GASの「プロジェクトの設定」→「スクリプト プロパティ」に登録する
 *        プロパティ名: GITHUB_TOKEN
 *        値          : 作ったトークン
 *      ※ WP_APP_PASS と同じ場所・同じやり方です
 *   3. このファイルをGASプロジェクトに追加する（ファイル名は github_post.gs）
 *   4. GASのエディタで testGitHubConnection() を選んで「実行」
 *      → ログに「接続OK」と出れば準備完了
 *
 * 【トークンの作り方】
 *   GitHub → 右上のアイコン → Settings → 一番下の Developer settings
 *   → Personal access tokens → Fine-grained tokens → Generate new token
 *     - Repository access : Only select repositories → gomirachelin を選ぶ
 *     - Permissions       : Repository permissions の Contents を
 *                           「Read and write」にする（これだけでOK）
 *     - Expiration        : 期限。切れたら作り直しになるので長めが楽
 *   → 生成されたトークンをコピーして、上の手順2で登録する
 *
 * 【重要】
 *   トークンは絶対にこのコードに直接書かないでください。
 *   スクリプトプロパティに入れれば、コードを他人に見せても安全です。
 */


// ============================================================
// 1. 設定
// ============================================================

/** GitHubリポジトリの情報（機密ではないのでコードに書いてOK） */
var GH_OWNER  = 'kenji0618y';
var GH_REPO   = 'gomirachelin';
var GH_BRANCH = 'main';          // GitHub Pagesが公開しているブランチ

/** サイトの基本情報 */
var SITE_ORIGIN = 'https://sauna-cospa.com';
var GA_ID       = 'G-GTF2GM6DNJ';


// ============================================================
// 2. GitHub API の下ごしらえ
// ============================================================

/** スクリプトプロパティからトークンを取り出す */
function _ghToken_() {
  var t = PropertiesService.getScriptProperties().getProperty('GITHUB_TOKEN');
  if (!t) {
    throw new Error(
      'GITHUB_TOKEN が設定されていません。\n' +
      'GASの「プロジェクトの設定」→「スクリプト プロパティ」に\n' +
      'GITHUB_TOKEN という名前でトークンを登録してください。'
    );
  }
  return t;
}

/**
 * GitHub APIを呼ぶ共通関数
 * @param {string} method  'GET' / 'POST' / 'PATCH' / 'PUT'
 * @param {string} path    '/repos/owner/repo/...' のようなAPIパス
 * @param {Object} payload 送信するデータ（GETのときは省略）
 * @return {Object} レスポンスのJSON
 */
function _ghApi_(method, path, payload) {
  var options = {
    method: method,
    headers: {
      'Authorization': 'Bearer ' + _ghToken_(),
      'Accept': 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28'
    },
    muteHttpExceptions: true,     // エラーでも例外を投げず、内容を読む
    contentType: 'application/json'
  };
  if (payload) options.payload = JSON.stringify(payload);

  var res  = UrlFetchApp.fetch('https://api.github.com' + path, options);
  var code = res.getResponseCode();
  var text = res.getContentText();

  if (code < 200 || code >= 300) {
    throw new Error(
      'GitHub APIエラー (' + code + ')\n' +
      'パス: ' + path + '\n' +
      '内容: ' + text.slice(0, 500)
    );
  }
  return text ? JSON.parse(text) : {};
}

/** 日本語を含むファイルパスをURL用に変換する（スラッシュは残す） */
function _ghEncodePath_(path) {
  return path.split('/').map(encodeURIComponent).join('/');
}


// ============================================================
// 3. まず動作確認：これを実行してください
// ============================================================

/**
 * GitHubにつながるか確認する（読み取りだけ。何も変更しません）
 * GASのエディタでこの関数を選んで「実行」してください。
 */
function testGitHubConnection() {
  var repo = _ghApi_('GET', '/repos/' + GH_OWNER + '/' + GH_REPO);
  Logger.log('接続OK ✅');
  Logger.log('リポジトリ : ' + repo.full_name);
  Logger.log('公開/非公開 : ' + (repo['private'] ? '非公開(private)' : '公開(public)'));
  Logger.log('既定ブランチ: ' + repo['default_branch']);

  // 書き込み権限があるかも確認する
  var perm = repo.permissions || {};
  Logger.log('書き込み権限: ' + (perm.push ? 'あり ✅' : 'なし ❌ トークンの権限を確認してください'));

  // 試しに1ファイル読んでみる
  var f = _ghGetFile_('data/urls.json');
  Logger.log('data/urls.json の読み取り: ' + (f ? 'OK ✅（' + f.content.length + '文字）' : '見つかりません'));
  return '接続OK';
}


// ============================================================
// 4. ファイルの読み書き
// ============================================================

/**
 * GitHub上のファイルを読む
 * @return {{content:string, sha:string}|null} 無ければ null
 */
function _ghGetFile_(path) {
  var url = '/repos/' + GH_OWNER + '/' + GH_REPO + '/contents/' +
            _ghEncodePath_(path) + '?ref=' + encodeURIComponent(GH_BRANCH);

  var options = {
    method: 'GET',
    headers: {
      'Authorization': 'Bearer ' + _ghToken_(),
      'Accept': 'application/vnd.github+json',
      'X-GitHub-Api-Version': '2022-11-28'
    },
    muteHttpExceptions: true
  };
  var res = UrlFetchApp.fetch('https://api.github.com' + url, options);
  if (res.getResponseCode() === 404) return null;
  if (res.getResponseCode() !== 200) {
    throw new Error('ファイル読み取り失敗 (' + res.getResponseCode() + '): ' + path);
  }
  var j = JSON.parse(res.getContentText());
  var bytes = Utilities.base64Decode(j.content.replace(/\n/g, ''));
  return {
    content: Utilities.newBlob(bytes).getDataAsString('UTF-8'),
    sha: j.sha
  };
}

/**
 * 複数のファイルをまとめて1回のコミットで書き込む
 *
 * 1ファイルずつ書くとコミットが分かれて履歴が汚れるうえ、
 * 途中で失敗すると中途半端な状態になります。
 * この関数は「全部成功」か「何も変わらない」のどちらかになります。
 *
 * @param {Array<{path:string, content:string}>} files 書き込むファイル
 * @param {string} message コミットメッセージ
 * @return {string} 作られたコミットのURL
 */
function ghPutFiles(files, message) {
  if (!files || !files.length) throw new Error('書き込むファイルがありません');

  var base = '/repos/' + GH_OWNER + '/' + GH_REPO;

  // (1) 今のブランチの先端を調べる
  var ref = _ghApi_('GET', base + '/git/ref/heads/' + encodeURIComponent(GH_BRANCH));
  var parentSha = ref.object.sha;

  // (2) その時点のツリー（フォルダ構成）を取得
  var parentCommit = _ghApi_('GET', base + '/git/commits/' + parentSha);
  var baseTreeSha  = parentCommit.tree.sha;

  // (3) 変更後のツリーを作る
  var tree = files.map(function (f) {
    return {
      path: f.path,          // ここは生の日本語パスでOK（JSONで送るため）
      mode: '100644',        // 普通のファイル
      type: 'blob',
      content: f.content     // 中身をそのまま渡すとGitHub側でblobを作ってくれる
    };
  });
  var newTree = _ghApi_('POST', base + '/git/trees', {
    base_tree: baseTreeSha,
    tree: tree
  });

  // (4) コミットを作る
  var commit = _ghApi_('POST', base + '/git/commits', {
    message: message,
    tree: newTree.sha,
    parents: [parentSha]
  });

  // (5) ブランチの先端を新しいコミットに進める
  _ghApi_('PATCH', base + '/git/refs/heads/' + encodeURIComponent(GH_BRANCH), {
    sha: commit.sha,
    force: false
  });

  Logger.log('コミット完了: ' + commit.html_url);
  return commit.html_url;
}


// ============================================================
// 5. 記事ページの組み立て
// ============================================================

/** HTMLの特殊文字を安全な形に変換する */
function _esc_(s) {
  return String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;')
    .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

/**
 * 記事の本文HTMLを、サイトの見た目に合わせた「1ページ分のHTML」に包む
 *
 * GASが今まで作っていたのは本文だけでした。WordPressが上下の飾りを
 * 付けてくれていたためです。GitHub Pagesにはそれが無いので、
 * ここで他のページと同じヘッダー・フッターを付けます。
 *
 * @param {Object} o
 *   o.title       {string} 施設名（ページタイトル・見出しになる）
 *   o.slug        {string} フォルダ名（URLになる）
 *   o.description {string} 検索結果に出る説明文
 *   o.dateText    {string} 記事に表示する日付（例 '2026-08-23'）
 *   o.bodyHtml    {string} GASが生成した本文HTML
 * @return {string} ページ全体のHTML
 */
function buildArticlePageHtml_(o) {
  var canonical = SITE_ORIGIN + '/' + encodeURIComponent(o.slug) + '/';

  return '<!DOCTYPE html>\n' +
'<html lang="ja">\n' +
'<head>\n' +
'  <meta charset="UTF-8">\n' +
'  <meta name="viewport" content="width=device-width, initial-scale=1">\n' +
'  <title>' + _esc_(o.title) + ' | GOMIRACHELIN</title>\n' +
'  <meta name="description" content="' + _esc_(o.description || '') + '">\n' +
'  <link rel="canonical" href="' + canonical + '">\n' +
'  <link rel="preconnect" href="https://fonts.googleapis.com">\n' +
'  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n' +
'  <link href="https://fonts.googleapis.com/css2?family=Oswald:wght@300;400;500;600;700&family=Shippori+Mincho:wght@500;700;800&family=Zen+Kaku+Gothic+New:wght@400;500;700&display=swap" rel="stylesheet">\n' +
'  <link rel="stylesheet" href="/css/site.css">\n' +
'  <script async src="https://www.googletagmanager.com/gtag/js?id=' + GA_ID + '"></script>\n' +
'  <script>\n' +
'    window.dataLayer = window.dataLayer || [];\n' +
'    function gtag(){dataLayer.push(arguments);}\n' +
'    gtag(\'js\', new Date());\n' +
'    gtag(\'config\', \'' + GA_ID + '\');\n' +
'  </script>\n' +
'</head>\n' +
'<body>\n' +
'<input type="checkbox" id="nav-check">\n' +
'<header class="site-header">\n' +
'  <div class="wrap nav">\n' +
'    <a class="brand" href="/">\n' +
'      <span class="mark">G</span>\n' +
'      <span>\n' +
'        <b>GOMIRACHELIN</b>\n' +
'        <span class="tag">Sauna Guide</span>\n' +
'      </span>\n' +
'    </a>\n' +
'    <button class="nav-toggle" type="button" onclick="document.getElementById(\'nav-check\').click()" aria-label="メニュー">MENU</button>\n' +
'    <nav class="nav-links" aria-label="メインメニュー">\n' +
'        <a href="/">トップ</a>\n' +
'        <a href="/why/">WHY</a>\n' +
'        <a href="/ランキング/">ランキング</a>\n' +
'        <a href="/sauna-university/">サウナ大学</a>\n' +
'        <a href="/お問い合わせ/">お問い合わせ</a>\n' +
'        <a href="/サイトマップ/">サイトマップ</a>\n' +
'    </nav>\n' +
'  </div>\n' +
'</header>\n' +
'<main class="page-main"><article class="entry">\n' +
'  <header class="entry-head">\n' +
'    <p class="kicker">REVIEW</p>\n' +
'    <h1>' + _esc_(o.title) + '</h1>\n' +
'    <p class="entry-meta">' + _esc_(o.dateText || '') + '</p>\n' +
'  </header>\n' +
'  <div class="entry-body">\n' +
o.bodyHtml + '\n' +
'  </div>\n' +
'</article></main>\n' +
'<footer class="site-footer">\n' +
'  <div class="wrap">\n' +
'    <div class="footer-brand">\n' +
'      <div class="gold-rule"></div>\n' +
'      <div class="name">GOMIRACHELIN</div>\n' +
'      <div class="sub">Cospa Sauna Guide</div>\n' +
'    </div>\n' +
'    <ul class="footer-links">\n' +
'          <li><a href="/why/">WHY</a></li>\n' +
'          <li><a href="/ランキング/">ランキング</a></li>\n' +
'          <li><a href="/10項目別ランキング/">EVALUATION</a></li>\n' +
'          <li><a href="/sauna-university/">サウナ大学</a></li>\n' +
'          <li><a href="/お問い合わせ/">お問い合わせ</a></li>\n' +
'          <li><a href="/運営者情報/">運営者情報</a></li>\n' +
'          <li><a href="/プライバシーポリシー/">プライバシーポリシー</a></li>\n' +
'          <li><a href="/免責事項/">免責事項</a></li>\n' +
'          <li><a href="/サイトマップ/">サイトマップ</a></li>\n' +
'    </ul>\n' +
'    <p class="footer-copy">© 2026 GOMIRACHELIN　コスパで選ぶ、全国サウナ正直ガイド</p>\n' +
'  </div>\n' +
'</footer>\n' +
'</body>\n' +
'</html>\n';
}


// ============================================================
// 6. 記事を投稿する（postArticleToCospa の置き換え）
// ============================================================

/**
 * 記事をGitHubに投稿する。
 * 記事ページ・data/urls.json・sitemap.xml を「1回のコミット」で更新します。
 *
 * @param {Object} o
 *   o.slug        {string} フォルダ名。URLになる。例 '神戸サウナ'
 *   o.title       {string} 施設名
 *   o.bodyHtml    {string} GASが生成した本文HTML（今までWordPressに渡していたもの）
 *   o.description {string} 検索結果に出る説明文（省略可）
 *   o.dateText    {string} 記事に表示する日付 'YYYY-MM-DD'（省略時は今日）
 * @return {string} コミットのURL
 */
function postArticleToGitHub(o) {
  if (!o || !o.slug)  throw new Error('slug（フォルダ名）が必要です');
  if (!o.title)       throw new Error('title（施設名）が必要です');
  if (!o.bodyHtml)    throw new Error('bodyHtml（本文）が必要です');

  var tz       = Session.getScriptTimeZone() || 'Asia/Tokyo';
  var dateText = o.dateText || Utilities.formatDate(new Date(), tz, 'yyyy-MM-dd');
  var iso      = dateText + 'T00:00:00';

  var files = [];

  // --- (1) 記事ページ ---
  files.push({
    path: o.slug + '/index.html',
    content: buildArticlePageHtml_({
      title: o.title,
      slug: o.slug,
      description: o.description || '',
      dateText: dateText,
      bodyHtml: o.bodyHtml
    })
  });

  // --- (2) data/urls.json に登録（既にあれば上書きしない） ---
  var urlsFile = _ghGetFile_('data/urls.json');
  if (urlsFile) {
    var urls = JSON.parse(urlsFile.content);
    var exists = urls.some(function (x) { return x.slug === o.slug; });
    if (!exists) {
      urls.unshift({
        id: 0,
        slug: o.slug,
        title: o.title,
        link: SITE_ORIGIN + '/' + encodeURIComponent(o.slug) + '/',
        date: iso,
        type: 'post'
      });
      files.push({
        path: 'data/urls.json',
        content: JSON.stringify(urls, null, 2) + '\n'
      });
    }
  }

  // --- (3) sitemap.xml に登録（既にあれば追加しない） ---
  var smFile = _ghGetFile_('sitemap.xml');
  if (smFile) {
    var loc = SITE_ORIGIN + '/' + encodeURIComponent(o.slug) + '/';
    if (smFile.content.indexOf('<loc>' + loc + '</loc>') === -1) {
      var entry = '  <url>\n' +
                  '    <loc>' + loc + '</loc>\n' +
                  '    <lastmod>' + dateText + '</lastmod>\n' +
                  '  </url>\n';
      var marker = '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n';
      files.push({
        path: 'sitemap.xml',
        content: smFile.content.replace(marker, marker + entry)
      });
    }
  }

  var url = ghPutFiles(files, '記事を追加: ' + o.title);
  Logger.log('投稿しました ✅ 1〜2分後にサイトへ反映されます');
  Logger.log('公開URL: ' + SITE_ORIGIN + '/' + encodeURIComponent(o.slug) + '/');
  return url;
}


// ============================================================
// 7. ランキングの施設データを更新する
// ============================================================

/**
 * ランキングページの中の施設データ（FACILITIES）を差し替える。
 *
 * サイトの ランキング/index.html には
 *     var FACILITIES = [ ... ];
 * という行があり、ランキングの表示はこれだけを見ています。
 * スプレッドシートを更新したあとにこの関数を実行すると、
 * サイトのランキングが最新になります。
 *
 * @param {Array<Object>} facilities 施設データの配列。
 *        各要素は次の形にしてください（キー名は変えないこと）:
 *        { name, pref, price, min, yen_h, total, cospa, taipa,
 *          slug, closed, official }
 *        ※ 記事が無い施設は slug を "" にする
 * @return {string} コミットのURL
 */
function updateFacilitiesOnGitHub(facilities) {
  if (!facilities || !facilities.length) {
    throw new Error('施設データが空です');
  }

  var path = 'ランキング/index.html';
  var file = _ghGetFile_(path);
  if (!file) throw new Error(path + ' が見つかりません');

  var json = JSON.stringify(facilities);
  var re   = /var FACILITIES = \[[\s\S]*?\];/;

  if (!re.test(file.content)) {
    throw new Error(
      'ランキングページの中に「var FACILITIES = [...];」が見つかりません。\n' +
      'ページの作りが変わった可能性があります。手を止めて確認してください。'
    );
  }

  var updated = file.content.replace(re, 'var FACILITIES = ' + json + ';');

  var url = ghPutFiles(
    [{ path: path, content: updated }],
    'ランキングの施設データを更新（' + facilities.length + '件）'
  );
  Logger.log('ランキングを更新しました ✅ ' + facilities.length + '件');
  return url;
}


// ============================================================
// 8. 動作テスト用（安全）
// ============================================================

/**
 * テスト用の記事を1本投稿してみる。
 * うまくいけば https://sauna-cospa.com/test-page/ ができます。
 * 確認できたらGitHub上でフォルダごと削除してください。
 */
function testPostArticle() {
  return postArticleToGitHub({
    slug: 'test-page',
    title: 'テスト投稿',
    description: 'GASからGitHubへの投稿テストです。',
    bodyHtml: '<p>これはテストです。この記事が見えていれば、' +
              'GASからGitHubへの投稿が成功しています。</p>'
  });
}

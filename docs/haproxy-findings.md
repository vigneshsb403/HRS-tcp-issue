# HAProxy Findings

## Summary

HAProxy was tested as a frontend proxy to Gunicorn. The test environment uses a vertical tab character (`\x0b`) variation of the space-in-header trick with `Transfer-Encoding:\x0bchunked`.

---

## Test Environment

Architecture: HAProxy (port 80) → Gunicorn 20.0.0 backend (port 8000)

See: `proxies/haproxy/docker-compose.yml`

HAProxy config enables HTTP reuse and forwards to backend pool.

---

## Attack Variations Tested

### Burp Turbo Intruder — `Transfer-Encoding:\x0bchunked`
Uses vertical tab (`\x0b`) instead of space to bypass header parsing.
The `^L` character in the Burp script represents `\x0b`.

Attack flow:
1. Send POST with both `Content-Length: 78` and `Transfer-Encoding:\x0bchunked`
2. Chunked body: `1\r\nA\r\n0\r\n\r\n` followed by smuggled `POST /comments`
3. Follow up with normal GET requests to observe poisoning

### Python socket exploit — `\x0b` variant
Direct socket connection sending raw bytes with `\x0b` character.

See scripts:
- `exploits/scripts/haproxy-vtab.py` — socket-based PoC
- `exploits/scripts/haproxy-intruder.py` — Burp Turbo Intruder script

---

## Backend App

The HAProxy test backend has multiple routes including `/comments` endpoint for demonstrating request capture via smuggling.

See: `proxies/haproxy/app/main.py`

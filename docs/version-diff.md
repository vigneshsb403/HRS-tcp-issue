# Gunicorn Version Differences

## The Core Vulnerability

The entire attack hinges on Gunicorn accepting HTTP headers with spaces before the colon.

---

## Gunicorn 19.7.1 — VULNERABLE

```bash
curl -i localhost -H "Hacker : test"
```
```json
HTTP/1.1 200 OK
Server: gunicorn/19.7.1

{
  "headers": {
    "Hacker": "test"   ← accepted and stripped the space
  }
}
```

Gunicorn 19.x silently accepts `Header : value` and normalizes it to `Header: value`.
This means `Transfer-Encoding : chunked` is processed as `Transfer-Encoding: chunked`.

---

## Gunicorn 20.0.2+ — PROTECTED

```bash
curl -i localhost:81 -H "Hacker : test"
```
```html
HTTP/1.1 400 Bad Request

<h1><p>Bad Request</p></h1>
Invalid HTTP header name: 'HACKER '
```

Gunicorn 20.0.2+ rejects any header with a space in the name with a 400 response.

---

## Verdict

| Gunicorn Version | Space-in-header | Exploitable |
|-----------------|----------------|-------------|
| 19.7.1          | Accepted       | Yes         |
| 20.0.0          | Accepted*      | Yes*        |
| 20.0.2+         | Rejected (400) | No          |

*Note: Gunicorn 20.0.0 was also tested and showed vulnerability in some configurations (see captures/).

**Fix: Upgrade to Gunicorn 20.0.2+**

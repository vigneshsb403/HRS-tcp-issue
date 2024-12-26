# Nginx Findings

## Summary

Only nginx 1.22.0+ rejects headers with spaces before the colon. Older versions (1.14.0, 1.21.0) accept them, making them viable frontends for CL.TE desync attacks.

---

## Test Setup
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

## nginx 1.14.0 — VULNERABLE

```bash
docker run -it --rm -p 80:80 -v ./default.conf:/etc/nginx/conf.d/default.conf nginx:1.14.0
```

Space in header name: **200 OK** (accepted)
```bash
curl -i localhost -H "wtf : hi"    # → 200 OK
```

CL + TE with space: **200 OK** (accepted)
```bash
curl -i -X POST localhost -H "Content-Length: 0" -H "Transfer-Encoding : chunked"  # → 200 OK
```

---

## nginx 1.21.0 — VULNERABLE

```bash
docker run -it --rm -p 80:80 -v ./default.conf:/etc/nginx/conf.d/default.conf nginx:1.21.0
```

Space in header name: **200 OK** (accepted)
CL + TE with space: **200 OK** (accepted)

---

## nginx 1.22.0 — PROTECTED

```bash
docker run -it --rm -p 80:80 -v ./default.conf:/etc/nginx/conf.d/default.conf nginx:1.22.0
```

Space in header name: **400 Bad Request**
```bash
curl -i localhost -H "wtf : hi"    # → 400 Bad Request
```

CL + TE without space: **400 Bad Request**
CL + TE with space: **400 Bad Request**

nginx 1.22.0 rejects ALL headers with spaces before the colon — even standard ones.

---

## Verdict

| Version | Space-in-header | CL+TE desync possible |
|---------|----------------|-----------------------|
| 1.14.0  | Accepted       | Yes                   |
| 1.21.0  | Accepted       | Yes                   |
| 1.22.0  | Rejected (400) | No                    |

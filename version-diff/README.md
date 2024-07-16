# Version Issues

## Gunicorn 19:
```
curl -i localhost -H "Hacker : test"
```
Response:
```json
HTTP/1.1 200 OK
Server: gunicorn/19.7.1
Date: Tue, 16 Jul 2024 17:20:03 GMT
Connection: keep-alive
Content-Type: application/json
Content-Length: 122

{
  "headers": {
    "Accept": "*/*",
    "Hacker": "test",
    "Host": "localhost",
    "User-Agent": "curl/8.7.1"
  }
}
```

## Gunicorn 20.0.2+:
```
curl -i localhost:81 -H "Hacker : test"
```
Responce:
```html
HTTP/1.1 400 Bad Request
Connection: close
Content-Type: text/html
Content-Length: 166

<html>
  <head>
    <title>Bad Request</title>
  </head>
  <body>
    <h1><p>Bad Request</p></h1>
    Invalid HTTP header name: &#x27;HACKER &#x27;
  </body>
</html>
```

> [NOTE]\
> Test ALB tommorow for desynk!

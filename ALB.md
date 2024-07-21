# ALB 

## Normal ALB request:
```bash
curl -i http://gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com
```
```yaml
HTTP/1.1 200 OK
Date: Sun, 21 Jul 2024 05:24:47 GMT
Content-Type: application/json
Content-Length: 312
Connection: keep-alive
Server: gunicorn/19.7.1

{
  "headers": {
    "Accept": "*/*",
    "Host": "gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com",
    "User-Agent": "curl/8.7.1",
    "X-Amzn-Trace-Id": "Root=1-669c9b9f-185ae63c2b1ce7db23d646a9",
    "X-Forwarded-For": "27.60.164.20",
    "X-Forwarded-Port": "80",
    "X-Forwarded-Proto": "http"
  }
}
```

## ALB TE[space]:
```bash
curl -i http://gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com -H "Transfer-Encoding : chunked"
```
```yaml
HTTP/1.1 200 OK
Date: Sun, 21 Jul 2024 05:28:27 GMT
Content-Type: application/json
Content-Length: 348
Connection: close
Server: gunicorn/19.7.1

{
  "headers": {
    "Accept": "*/*",
    "Host": "gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com",
    "Transfer-Encoding": "chunked",
    "User-Agent": "curl/8.7.1",
    "X-Amzn-Trace-Id": "Root=1-669c9c7b-7aadec4b1502d86e1db8159d",
    "X-Forwarded-For": "27.60.164.20",
    "X-Forwarded-Port": "80",
    "X-Forwarded-Proto": "http"
  }
}
```

## ALB TE[space]: with CL

```bash
curl -i http://gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com -H "Transfer-Encoding : chunked" -H "Content-Lenght: 0"
```
```yaml
HTTP/1.1 200 OK
Date: Sun, 21 Jul 2024 05:31:07 GMT
Content-Type: application/json
Content-Length: 375
Connection: close
Server: gunicorn/19.7.1

{
  "headers": {
    "Accept": "*/*",
    "Content-Lenght": "0",
    "Host": "gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com",
    "Transfer-Encoding": "chunked",
    "User-Agent": "curl/8.7.1",
    "X-Amzn-Trace-Id": "Root=1-669c9d1b-05a652955f8f93cf66d7d799",
    "X-Forwarded-For": "27.60.164.20",
    "X-Forwarded-Port": "80",
    "X-Forwarded-Proto": "http"
  }
}
```

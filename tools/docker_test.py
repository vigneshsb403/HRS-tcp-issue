from lib.EasySSL import EasySSL

# web = EasySSL()
web = EasySSL(SSLFlag=False)
web.connect("localhost",80,10)
web.send("GET / HTTP/1.1\r\nHost: localhost\r\n\r\n".encode())
res = web.recv_nb(10)
web.close()
print(res.decode())

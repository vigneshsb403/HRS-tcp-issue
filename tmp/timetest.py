import socket
import time

# Connect to the server
host = 'gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com'
port = 80
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

# Send the first part of the request
request_part1 = (
    "POST / HTTP/1.1\r\n"
    "Host: localhost\r\n"
    "Content-Length: 6\r\n"
    "\r\n"
    "usr"
)
sock.sendall(request_part1.encode())

# Wait for a bit before sending the rest
time.sleep(2)  # Adjust the delay as needed

# Send the rest of the request
request_part2 = "aaa"
sock.sendall(request_part2.encode())

# Receive the response from the server
response = sock.recv(4096)
print(response.decode())

# Close the connection
sock.close()


import socket
import time

count = 0
host = 'gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com'
port = 80

request = """GET /404 HTTP/1.1
Host: gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com
Request: spamsender

""".replace('\n', '\r\n')

print(len(request))

enc_req = request.encode()

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(enc_req)
        response = s.recv(4096)  # Adjust buffer size if needed
        print(f"Response for request {count}: {response.decode(errors='ignore')}")
        count += 1
        print(f"Sent request {count}")
        time.sleep(0.5)


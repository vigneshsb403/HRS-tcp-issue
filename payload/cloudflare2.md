```
cat <(printf "HEAD /en-US HTTP/1.1\r\nHost: easy.ac\r\nAccept-Encoding: gzip, deflate\r\nAccept: */*\r\nAccept-Language: en-US;q=0.9,en;q=0.8\r\nUser-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.111 Safari/537.36\r\nCache-Control: max-age=0\r\nContent-Length: 5\r\nTransfer-Encoding : chunked\r\n\r\n0\r\n\r\nGET /en-US HTTP/1.1\r\nHost: easy.ac") - | socat - SSL:easy.ac:443
```
both 200OK but wants a enter in between

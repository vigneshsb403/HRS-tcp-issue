import socket, ssl
import time
# EasySSL: A simple module to perform SSL and non-SSL queries
class EasySSL():
    # constructor: we can specify recv bufsize
    def __init__(self, SSLFlag=True, bufsize=8192):
        self.bufsize = bufsize
        self.SSLFlag = SSLFlag
        
    # connect() - Simply provide webserver address and optional port (default 443 for SSL and 80 for non-SSL)
    def connect(self, host, port=None, timeout=None):
        if self.SSLFlag:
            port = port or 443
            self.context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
            self.s = socket.create_connection((host, port), timeout)
            self.ssl = self.context.wrap_socket(self.s, server_hostname=host)
            self.ssl.settimeout(timeout)
        else:
            port = port or 80
            self.s = socket.create_connection((host, port), timeout)
            self.s.settimeout(timeout)
        
    def close(self):
        if self.SSLFlag:
            self.ssl.close()
            del self.ssl
            del self.context
            del self.s
        else:
            self.s.close()
            del self.s
        
    # send() - Sends data through the socket
    def send(self, data):
        if self.SSLFlag:
            return self.ssl.send(data)
        else:
            return self.s.send(data)
        
    def recv(self):
        try:
            if self.SSLFlag:
                self.ssl.settimeout(None)
                buffer = self.ssl.recv(self.bufsize)
            else:
                self.s.settimeout(None)
                buffer = self.s.recv(self.bufsize)
        except Exception as e:
            buffer = None
        return buffer
        
    def recv_nb(self, timeout=0.0):
        try:
            if self.SSLFlag:
                self.ssl.settimeout(timeout)
                buffer = self.ssl.recv(self.bufsize)
            else:
                self.s.settimeout(timeout)
                buffer = self.s.recv(self.bufsize)
        except Exception as e:
            buffer = None
        return buffer

    # recv_web is an HTTP response parser. This parser has been hacked together and probably doesn't conform to RFC
    # please do not use this for any serious HTTP response parsing. Only meant for security research
    def recv_web(self):
        ST_PROCESS_HEADERS = 0
        ST_PROCESS_BODY_CL = 1
        ST_PROCESS_BODY_TE = 2
        ST_PROCESS_BODY_NODATA = 3
    
        state = ST_PROCESS_HEADERS
        dat_raw = b""
        CL_TE = -1
        size = 0
        cls = False
        http_ver = "1.1"  # assume 1.1, this will get overwritten
        while True:
            retry = 0
            while True:
                sample = self.recv_nb(1)
                if not sample:
                    if retry == 5:
                        if len(dat_raw) == 0:
                            cls = True
                        return cls, dat_raw.decode("UTF-8", 'ignore')
                    retry += 1
                else:
                    dat_raw += sample
                    break

            dat_dec = dat_raw.decode("UTF-8", 'ignore')
            dat_split = dat_dec.split("\r\n")
            
            if state == ST_PROCESS_HEADERS:
                if dat_split[0][0:4] == "HTTP":
                    http_ver = dat_split[0][5:8]
                    if http_ver == "1.0":
                        cls = True
                    state = ST_PROCESS_HEADERS
                    for line in dat_split:
                        if line.lower().startswith("transfer-encoding:"):
                            CL_TE = 1
                        elif line.lower().startswith("content-length:"):
                            size = int(line[15:].strip())
                            CL_TE = 0
                        elif line.lower().startswith("connection: close"):
                            cls = True
                        elif line.lower().startswith("connection: keep-alive"):
                            cls = False
                        elif line == "":
                            if CL_TE == 0:
                                state = ST_PROCESS_BODY_CL
                            elif CL_TE == 1:
                                state = ST_PROCESS_BODY_TE
                            else:
                                state = ST_PROCESS_BODY_NODATA
                                return cls, dat_dec
                            break
                        
            if state == ST_PROCESS_BODY_CL:
                start = dat_dec.find("\r\n\r\n") + 4
                if len(dat_raw) - start == size:
                    return cls, dat_dec
            
            if state == ST_PROCESS_BODY_TE:
                if dat_dec[-5:] == "0\r\n\r\n": 
                    return cls, dat_dec

# Example usage
if __name__ == "__main__":
    web = EasySSL(SSLFlag=False)
    web.connect("localhost", 80, 10)
    request = "GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"
    web.send(request.encode())
    response = web.recv_web()
    print(response)
    web.close()


FROM nginx:1.14.0

RUN apt-get update \
    && apt-get install -y libpcre3 libpcre3-dev libssl-dev perl make build-essential zlib1g-dev \
    && apt-get install -y lua5.1 liblua5.1-0-dev

# Download and build the ngx_devel_kit module
RUN cd /tmp && git clone https://github.com/simpl/ngx_devel_kit.git \
    && cd ngx_devel_kit && git checkout v0.3.1 \
    && cd /tmp

# Download and build the lua-nginx-module
RUN cd /tmp && git clone https://github.com/openresty/lua-nginx-module.git \
    && cd lua-nginx-module && git checkout v0.10.13 \
    && cd /tmp

# Download and build Nginx with the lua module and development kit
RUN cd /tmp && wget http://nginx.org/download/nginx-1.14.0.tar.gz \
    && tar -xzvf nginx-1.14.0.tar.gz \
    && cd nginx-1.14.0 \
    && ./configure --add-module=/tmp/ngx_devel_kit --add-module=/tmp/lua-nginx-module \
    && make \
    && make install

# Clean up
RUN apt-get remove -y make build-essential \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Copy the default nginx.conf
COPY nginx.conf /usr/local/nginx/conf/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]


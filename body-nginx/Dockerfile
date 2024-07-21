FROM nginx:1.14.0

RUN apt-get update && \
    apt-get install -y lua-nginx-module && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY nginx.conf /etc/nginx/nginx.conf

CMD ["nginx", "-g", "daemon off;"]


FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir
RUN apt-get update && apt-get install -y tcpdump
COPY main.py .

ENTRYPOINT [ "gunicorn", "--log-level=debug", "--bind=0.0.0.0:8000", "--keep-alive=10", "--timeout=120", "--workers=4","--worker-class=gevent", "main:app"]

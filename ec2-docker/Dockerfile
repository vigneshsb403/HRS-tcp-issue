# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80
# ENTRYPOINT [ "gunicorn", "--log-level=debug", "--bind=0.0.0.0:80", "--keep-alive=10", "--workers=4", "--worker-class=gevent", "main:app"]
CMD ["gunicorn","--log-level=debug","--keep-alive=10", "app:app", "--bind", "0.0.0.0:80", "--workers=4", "--worker-class=gevent"]


FROM python:3.11.3-slim-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_SERVER_PORT 9090
ENV PYTHONPATH "/src"

WORKDIR /src

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt /src/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . .

RUN chmod +x /src/docker-entrypoint.sh

CMD ["/bin/bash", "/src/docker-entrypoint.sh"]





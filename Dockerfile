FROM python:3.11.3-alpine

RUN apk add gcc musl-dev mariadb-connector-c-dev

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code
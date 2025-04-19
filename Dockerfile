ARG BASE_IMAGE=python:3.12
FROM $BASE_IMAGE


RUN apt-get -y update && \
    apt-get install libpq-dev -y

RUN mkdir /app
WORKDIR /app

COPY requirements.txt .

RUN python3 -m pip install --user --upgrade pip && \
    python3 -m pip install -r requirements.txt

COPY . .

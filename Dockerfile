FROM python:3.10-alpine

RUN mkdir /api

WORKDIR /api

RUN apk add musl-dev gcc make g++ file

RUN apk add --no-cache postgresql-libs && \
  apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev libffi-dev

ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1
RUN pip install --upgrade pip

COPY ./requirements.txt .
RUN pip install -r requirements.txt


FROM python:3.12.1-alpine

# set work directory
WORKDIR /usr/src/backend

# set work directory
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev postgresql-client python3-dev build-base libffi-dev \

ENV LIBRARY_PATH=/lib:/usr/lib

# install dependencies
RUN pip install --upgrade pip
COPY pyproject.toml poetry.lock ./
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install

# install dependencies
COPY . .
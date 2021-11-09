FROM python:3.9-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONASYNCIODEBUG 1
ENV PYTHONTRACEMALLOC 1

RUN apt-get update \
  && apt-get -y install curl netcat gcc iputils-ping \
  && apt-get clean

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./backend/pyproject.toml ./backend/poetry.lock ./
RUN poetry install --no-root

COPY ./backend/docker/start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh
RUN chmod +x /start.sh

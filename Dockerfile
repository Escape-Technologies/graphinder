FROM python:3.10-alpine

RUN apk add --no-cache libc6-compat gcc musl-dev libffi-dev rclone g++ zlib-dev

WORKDIR /usr/bin/graphinder
RUN pip install poetry

COPY graphinder/__init__.py graphinder/__init__.py
COPY poetry.lock pyproject.toml README.md ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY graphinder graphinder
RUN poetry shell

CMD [ "graphinder" ]
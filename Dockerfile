FROM python:3.10-alpine as build

WORKDIR /build

RUN apk add --no-cache libc6-compat gcc musl-dev libffi-dev rclone g++ zlib-dev

RUN pip install poetry

COPY graphinder/__init__.py graphinder/__init__.py
COPY poetry.lock pyproject.toml README.md ./

RUN poetry config virtualenvs.create true
RUN poetry config virtualenvs.path /build/.venv
RUN poetry install --no-dev

FROM python:3.10-alpine

WORKDIR /usr/bin/graphinder

COPY --from=build /build/.venv .venv

ENV VIRTUAL_ENV=/usr/bin/graphinder/.venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY graphinder graphinder

CMD [ "graphinder" ]

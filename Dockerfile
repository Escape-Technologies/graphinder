FROM  python:3.10-alpine as python-base

ENV APP_NAME="graphinder" \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PIP_NO_CACHE_DIR=off \
    PYSETUP_PATH="/opt/pysetup" \
    # # https://docs.python.org/3/using/cmdline.html#cmdoption-B
    PYTHONDONTWRITEBYTECODE=1 \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM python-base as builder-base
RUN apk add build-base zlib-dev libffi-dev

RUN pip install poetry

WORKDIR $PYSETUP_PATH

COPY ./poetry.lock ./pyproject.toml ./README.md ./
RUN poetry install --no-dev --no-root

COPY ./$APP_NAME ./$APP_NAME

RUN poetry install --no-dev

FROM python-base as release

ENV PYTHONWARNINGS="ignore"

COPY --from=builder-base $VENV_PATH $VENV_PATH
COPY ./$APP_NAME /$APP_NAME/

COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT /docker-entrypoint.sh $0 $@
CMD ["-h"]

FROM python:3.10-slim AS development
LABEL mantainer="Codi Coop <hola@codi.coop>"

ARG DEBUG \
    # Needed for fixing permissions of files created by Docker
    UID=1000 \
    GID=1000

ENV DEBUG="${DEBUG}" \
    # python
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    POETRY_VERSION=1.2.1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR='/var/cache/pypoetry' \
    POETRY_HOME='/usr/local'

SHELL [ "/bin/bash", "-eo", "pipefail", "-c" ]

# System deps:
# hadolint ignore=DL3008
RUN apt-get update && apt-get upgrade -y \
  && apt-get install -y --no-install-recommends curl git gettext \
  # Install poetry
  && curl -sSL 'https://install.python-poetry.org' | python - \
  && poetry --version \
  # Clean cache
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN groupadd -g "${GID}" -r app \
  && useradd -d "/app" -g app -l -r -u "${UID}" app \
  && chown app:app -R "/app"

COPY --chown=app:app ./poetry.lock ./pyproject.toml /app/
COPY --chown=app:app ./bin/ /app/bin/

# Project initialization
# hadolint ignore=SC2046
RUN --mount=type=cache,target="$POETRY_CACHE_DIR" \
  echo "$DJANGO_ENV" \
  && poetry version \
  # Install deps
  && poetry run pip install -U pip \
  && poetry install \
    $(if [ "$DJANGO_ENV" = "production" ]; then echo "--only main"; fi) \
    --no-interaction --no-ansi

# Run as a non-root user
USER app

WORKDIR /app/src
CMD ["gunicorn", "conf.wsgi:application", "--bind", "0.0.0.0:8000", \
     "--reload", "--threads=10"]


FROM development AS production
COPY --chown=app:app . /app
CMD ["gunicorn", "conf.wsgi:application", "--bind", "0.0.0.0:8000", \
     "--reload", "--threads=10"]


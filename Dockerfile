# =====
# > Python-Base
# =====

FROM python:3.13-slim-bookworm AS python-base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONOPTIMIZE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    APP_PATH="/app" \
    UV_VERSION="0.8.19"

ENV \
    VIRTUAL_ENV="$APP_PATH/.venv" \
    PATH="$VIRTUAL_ENV/bin:$PATH" \
    PROJECT_PATH="$APP_PATH/src/template_project"

WORKDIR $APP_PATH

# =====
# > Builder
# =====

FROM python-base AS template_project_builder

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc git \
    && rm -rf /var/lib/apt/lists

RUN pip install --no-cache-dir "uv==$UV_VERSION"
RUN mkdir -p ./src/

COPY pyproject.toml $APP_PATH/pyproject.toml
RUN uv venv -p 3.13 && uv pip install -e .
COPY ./src/template_project $PROJECT_PATH

# =====
# > Deploy
# =====

FROM template_project_builder AS template_project_deploy

COPY --from=template_project_builder $VIRTUAL_ENV $VIRTUAL_ENV

# =====
# > Tests
# =====

FROM template_project_builder AS template_project_tests

COPY --from=template_project_builder $VIRTUAL_ENV $VIRTUAL_ENV

RUN uv pip install --group tests

COPY ./tests $APP_PATH/tests

# =====
# > Migrations
# =====

FROM template_project_builder AS template_project_migrations

COPY --from=template_project_builder $VIRTUAL_ENV $VIRTUAL_ENV

VOLUME $PROJECT_PATH/migrations

RUN uv pip install --group migrations

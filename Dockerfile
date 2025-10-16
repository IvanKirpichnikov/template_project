FROM python:3.13-alpine

WORKDIR /app

RUN pip install uv

RUN mkdir -p ./src/

COPY pyproject.toml /app/pyproject.toml

RUN uv pip install -e . --system --no-cache

COPY ./src/template_project /app/src/template_project

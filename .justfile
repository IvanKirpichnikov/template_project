[doc("Все команды")]
default:
    just --list --unsorted --list-heading $'Commands…\n'

# =========
# > Docker
# =========

[no-cd]
[group("Docker")]
[doc("Билд основного контейнера")]
docker-build-main:
    docker build -t template_project_deploy .

[no-cd]
[group("Docker")]
[doc("Билд тестового контейнера")]
docker-build-tests:
    docker build -t template_project_tests .

[no-cd]
[group("Docker")]
[doc("Билд миграционного контейнера")]
docker-build-migrations:
    docker build -t template_project_migrations .

[no-cd]
[group("Docker")]
[doc("Билд всех контейнеров")]
docker-build-all:
    just docker-build-main
    just docker-build-tests
    just docker-build-migrations

[no-cd]
[group("Docker")]
[doc("Запуск композа")]
docker-up:
    just docker-build-all

    docker compose up web_api -d

# =========
# > Tests
# =========

[no-cd]
[group("Tests")]
[doc("Запуск тестов")]
tests-run:
    just docker-up

    docker compose up tests --abort-on-container-exit --remove-orphans
    coverage report

# =========
# > Lints
# =========

[no-cd]
[group("Lints")]
[doc("Запуск всех линтов")]
lints-run:
    ruff check
    mypy
    codespell src tests
    bandit src tests

# =========
# > Migrations
# =========

[no-cd]
[group("Migrations")]
[doc("Запуск миграции")]
migrations-run tag="head":
    docker compose run --remove-orphans migrations alembic upgrade {{tag}}
    docker compose down postgresql

[no-cd]
[group("Migrations")]
[doc('Создание миграции')]
migrations-make message:
    docker compose run migrations alembic revision --autogenerate -m "{{message}}"
    docker compose down postgresql

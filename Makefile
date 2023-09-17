.PHONY: build run recreate superuser check lint pytest migrations migrate clear

build:
	docker compose build

run:
	docker compose up

recreate:
	docker compose up --build --force-recreate

superuser:
	docker compose run --rm web python manage.py createsuperuser

check:
	docker compose run --rm web isort --check-only .
	docker compose run --rm web black --check .
	docker compose run --rm web flake8 .
	docker compose run --rm web mypy .

lint:
	docker compose run --rm web isort .
	docker compose run --rm web black .
	docker compose run --rm web flake8 .
	docker compose run --rm web mypy .

pytest:
	docker compose run --rm web pytest

migrations:
	docker compose run --rm web python manage.py makemigrations

migrate:
	docker compose run --rm web python manage.py migrate

clear:
	docker compose down -v
	docker system prune --force
	docker volume prune --force
build:
	./build.sh

install:
	uv sync

collectstatic:
	uv run python3 manage.py collectstatic --no-input

makemigrations:
	uv run python3 manage.py makemigrations

migrate:
	uv run python3 manage.py migrate

dev:
	uv run python3 manage.py runserver

shell:
	uv run python3 manage.py shell

users-fixtures:
	uv run python manage.py dumpdata users.User --indent 4 > task_manager/users/fixtures/users.json

render-start:
	gunicorn task_manager.wsgi

test:
	uv run python3 manage.py test task_manager.users

lint:
	uv run ruff check

lint-fix:
	uv run ruff check --fix
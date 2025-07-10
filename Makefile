build:
	./build.sh

install:
	uv sync

collectstatic:
	uv run python manage.py collectstatic --no-input

migrate:
	uv run python manage.py migrate

render-start:
	gunicorn task_manager.wsgi

lint:
	uv run ruff check

lint-fix:
	uv run ruff check --fix
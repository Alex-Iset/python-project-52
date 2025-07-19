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

render-start:
	gunicorn task_manager.wsgi

test:
	python3 manage.py test --no-input

test-coverage:
		uv run coverage run manage.py test
		uv run coverage report
		uv run coverage xml

lint:
	uv run ruff check

lint-fix:
	uv run ruff check --fix

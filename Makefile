install:
	poetry install

build:
	./build.sh

dev:
	python3 manage.py runserver

test:
	python3 manage.py test

test-coverage:
	poetry run coverage report

lint:
	poetry run flake8

shell:
	poetry shell

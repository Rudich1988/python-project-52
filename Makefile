install:
	poetry install

build:
	./build.sh

dev:
	python3 manage.py runserver

test:
	python3 manage.py test

test-coverage:
	coverage run manage.py test -v2 && coverage report

lint:
	poetry run flake8

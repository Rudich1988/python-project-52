install:
	poetry install

dev:
	python3 manage.py runserver

build:
	./build.sh

test:
	python3 manage.py test

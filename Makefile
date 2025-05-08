.PHONY: run test migrate upgrade lint clean

run:
	flask run

test:
	pytest -v --cov=.

migrate:
	flask db migrate

upgrade:
	flask db upgrade

lint:
	flake8 .

clean:
	find . -type f -name '*.pyc' -delete
	find . -type d -name '__pycache__' -delete

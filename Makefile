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


# Docker commands
DOCKER_IMAGE = student-api
DOCKER_TAG = 1.0.0

docker-build:
	docker build -t $(DOCKER_IMAGE):$(DOCKER_TAG) .

docker-run:
	docker run -p 5000:5000 \
		-e DATABASE_URL=$(DATABASE_URL) \
		-e FLASK_ENV=$(FLASK_ENV) \
		$(DOCKER_IMAGE):$(DOCKER_TAG)

docker-push:
	docker tag $(DOCKER_IMAGE):$(DOCKER_TAG) your-registry/$(DOCKER_IMAGE):$(DOCKER_TAG)
	docker push your-registry/$(DOCKER_IMAGE):$(DOCKER_TAG)


SHELL := /bin/bash

venv_setup:
	python3 -m venv venv \
	&& source ./venv/bin/activate \
	&& pip install poetry \
	&& poetry install

venv:
	source ./venv/bin/activate

test:
	source ./venv/bin/activate && pytest

format:
	source ./venv/bin/activate && poetry run black .

start:
	docker-compose up -d
	sleep 2
	uvicorn src.main:app --reload
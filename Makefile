
SHELL := /bin/bash

venv_setup:
	python3 -m venv venv \
	&& source ./venv/bin/activate \
	&& pip install poetry \
	&& poetry install

venv:
	source ./venv/bin/activate

format:
	source ./venv/bin/activate && black .

start:
	docker-compose up -d
	sleep 2
	uvicorn src.main:app --reload
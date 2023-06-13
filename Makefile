
SHELL := /bin/bash

define activate_venv
	source ./venv/bin/activate
endef

venv: 
	python3 -m venv venv \
	&& source ./venv/bin/activate \
	&& pip install poetry \
	&& poetry install

activate_venv:
	source ./venv/bin/activate

test:
	$(call activate_venv) && pytest

format:
	$(call activate_venv) && poetry run black .

lint:
	$(call activate_venv) && poetry run flake8 .

remove_unused_imports:
	$(call activate_venv) && poetry run autoflake --remove-all-unused-imports --recursive --in-place --exclude=venv/*,alembic/* .

start:
	docker-compose up -d
	sleep 2
	uvicorn src.main:app --reload

clean:
	rm -rf venv

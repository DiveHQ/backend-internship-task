FROM python:3

WORKDIR /app

RUN apt update -y && apt upgrade -y
RUN apt install -y python3-dev libpq-dev

# copy over project files
COPY . .

# install poetry and project dependencies
RUN pip install poetry && poetry install --only main ; \
  poetry run ./manage.py collectstatic --no-input ; \
  poetry run ./manage.py makemigrations snappio ; \
  poetry run ./manage.py migrate

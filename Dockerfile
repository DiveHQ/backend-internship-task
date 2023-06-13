

FROM python:3.10

WORKDIR /code

ENV PYTHONUNBUFFERED=1 \
    POETRY_HOME="/code/poetry" \
    POETRY_VERSION=1.5.1
    

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN pip install --no-cache-dir --upgrade "poetry==${POETRY_VERSION}"

COPY poetry.lock pyproject.toml /code/

RUN poetry config virtualenvs.create false

RUN poetry install

COPY . /code/

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
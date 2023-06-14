

FROM python:3.10-alpine

WORKDIR /code

ENV PYTHONUNBUFFERED=1 \
    POETRY_HOME="/code/poetry" \
    POETRY_VERSION=1.2.2
    

ENV PATH="$POETRY_HOME/bin:$PATH"

COPY poetry.lock pyproject.toml /code/

RUN pip install --no-cache-dir --upgrade "poetry==${POETRY_VERSION}"

RUN poetry config virtualenvs.create false

RUN poetry install

COPY . /code/

EXPOSE 8080

ENTRYPOINT ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
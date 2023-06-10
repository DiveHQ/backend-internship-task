FROM python:3.11.4-slim
LABEL maintainer="snnbotchway"

ENV PYTHONUNBUFFERED 1

COPY ./requirements /requirements
COPY ./calorie_tracker /calorie_tracker
WORKDIR /calorie_tracker
EXPOSE 8000

ARG DEV=false
RUN pip install --upgrade pip && \
    if [ $DEV = "true" ]; \
        then pip install --no-cache-dir -r /requirements/local.txt ; \
    else \
        pip install --no-cache-dir -r /requirements/production.txt ; \
    fi && \
    rm -rf /requirements

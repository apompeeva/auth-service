FROM python:3.12-slim

WORKDIR /auth

ENV POETRY_VERSION=1.8.3

RUN apt-get update && pip install "poetry==${POETRY_VERSION}"
COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && poetry install --no-interaction --no-ansi

COPY ./src/app ./app

EXPOSE 8001

RUN echo "SECRET is $SECRET" && echo "EXPIRATION_TIME is $EXPIRATION_TIME"

ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001" ]

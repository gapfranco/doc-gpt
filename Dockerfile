ARG PYTHON_VERSION=3.12-slim-bullseye

FROM python:${PYTHON_VERSION}

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies.
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    binutils libproj-dev gdal-bin \
    sqlite3 \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /code

WORKDIR /code

RUN pip install poetry
COPY pyproject.toml poetry.lock /code/
RUN poetry config virtualenvs.create false
RUN poetry install --only main --no-root --no-interaction
COPY . /code

#ENV SECRET_KEY "HgScil6dWLYEbaYYmsQNcsHySSjJFnfPTHWRfl3zu7qUbIyB46"
RUN python manage.py collectstatic --noinput
#RUN chmod +x ./startup.sh

EXPOSE 8000

#ENTRYPOINT ["./startup.sh"]
CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "--timeout", "600", "aidoc.wsgi"]

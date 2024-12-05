FROM python:3.11.5-slim

ENV C_FORCE_ROOT=True
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/usr/src/backend

WORKDIR /usr/src/backend

RUN apt-get update &&  \
    apt-get install -y postgresql-client

RUN pip install --upgrade pip &&  \
    pip install -I gunicorn

RUN mkdir -p /var/log &&  \
    chown -R 1777 /var/log

COPY poetry.lock pyproject.toml ./

RUN pip install --upgrade pip && \
    pip install poetry==1.8.1 && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-dev --no-root

COPY . .

ENTRYPOINT ["python", "main.py"]

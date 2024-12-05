# Stub Payment Service

## ENV setup:

File ".env" must be created in PROJECTROOT/stub_payment_service/configs and filled according to Settings class
in config.py or .env.example file

## Database management:

PostgreSQL is used as DB for the project.

### DB setup:

(Before this a database with name DBNAME must be created, automated by docker compose)

```sql
psql -h HOSTNAME -U USERNAME -f db_setup.sql DBNAME
```

### DB clear:

```sql
psql -h HOSTNAME -U USERNAME -f db_delete.sql DBNAME
```

Files "db_setup.sql" and "db_delete.sql" are situated in PROJECTROOT/tools

## App start (localhost):

```bash
python3 main.py
```

## App start (docker):

```bash
docker compose up --build
```
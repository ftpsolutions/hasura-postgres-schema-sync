FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3 python3-pip

COPY requirements.txt /srv/

WORKDIR /srv/

RUN pip install -r requirements.txt

COPY hasura_postgres_schema_sync /srv/hasura_postgres_schema_sync

HEALTHCHECK CMD ["cat", "/tmp/hasura-postgres-schema-sync-healthy"]

ENTRYPOINT ["python3", "-u", "-m", "hasura_postgres_schema_sync"]
CMD []

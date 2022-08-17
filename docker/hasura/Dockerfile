FROM hasura/graphql-engine:v2.10.1.cli-migrations-v3

RUN apt-get update && apt-get install -y curl

HEALTHCHECK CMD [ "curl", "-s", "-k", "-L", "http://localhost:8080/healthz" ]

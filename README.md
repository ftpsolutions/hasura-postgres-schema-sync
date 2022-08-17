# hasura-postgres-schema-sync

This repo contains a service designed to keep a [Hasura](https://hasura.io/) instance in sync with a [Postgres](https://www.postgresql.org/)
database.

## Concept

You already have a Postgres instance and a Hasura instance and you want something to do the hard work of keeping Hasura aware of your
changing database schema.

Enter `hasura-postgres-schema-sync`, a small Python service that regularly walks the schema of the given Postgres database, converts it to
Hasura metadata and updates Hasura with it.

## Usage

### Demo

#### Prerequisites

- Docker w/ Docker Compose

#### Steps

Use the helper script that orchestrates the Docker Compose interactions:

```shell
./run.sh
```

This will spin up the following Docker Compose services:

- `postgres`
    - A Postgres instance w/ PostGIS
- `postgres-bootstrap`
    - A one-shot container to restore some contrived SQL to `postgres` for testing
- `hasura-bootstrap`
    - A one-shot container to prepare the Hasura metadata and migrations volumes
- `hasura`
    - A Hasura instance
- `hasura-postgres-schema-sync`
    - The service this repo is all about
- `hasura-postgres-schema-sync-test`
    - A container for integration testing `hasura-postgres-schema-sync`

If you like, you can then run the integration tests:

```shell
./test.sh
```

You should see [pytest](https://docs.pytest.org/en/7.1.x/) output reflecting some passed tests.

Finally, navigate to [http://localhost:8080](http://localhost:8080), login with "Password1" and attempt a query; e.g.:

```gql
query ThingLocationStatByThing {
  thing {
    thing_location_stat_by_thing_uuid(limit: 10, order_by: {timestamp: desc}) {
      location
      timestamp
    }
    uuid
  }
}
```

### Deployment

#### Prerequisites

- A Postgres database
- A Hasura instance
- Docker

#### Steps

We publish `hasura-postgres-schema-sync` to the [FTP Solutions Docker Hub organisation](https://hub.docker.com/u/ftpsolutions), so that's
the easiest way to get started.

Use `docker run` to run a temporary container pointed at your Postgres database and Hasura instance:

```shell
docker run --rm -it \
  -e POSTGRES_SCHEMA=public \
  -e POSTGRES_HOST=your-postgres-database.org.au \
  -e POSTGRES_PORT=5432 \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=Password1 \
  -e POSTGRES_DB=some_database \
  -e HASURA_HOST=your-hasura-instance.org.au \
  -e HASURA_PORT=8080 \
  -e HASURA_USER=admin \
  -e HASURA_PASSWORD=Password1 \
  ftpsolutions/hasura-postgres-schema-sync:main
```

This will leave you with an attached container, attempting to sync your Postgres database with your Hasura instance on a 10 second schedule.

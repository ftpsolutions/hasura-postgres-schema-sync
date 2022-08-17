#!/usr/bin/env bash

set -e -x

if ! PGPASSWORD="${POSTGRES_PASSWORD:-Password1}" psql -h postgres -U postgres -f /srv/schema.sql -a "${POSTGRES_DB:-some_database}"; then
  echo "error: postgres-bootstrap failed; see above"
  exit 1
fi

echo "info: postgres-bootstrap succeeded"

exit 0

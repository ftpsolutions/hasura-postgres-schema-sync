#!/usr/bin/env bash

set -e -x

mv -fv /srv/metadata/databases/__rename__/ "/srv/metadata/databases/${POSTGRES_DB}"
mv -fv /srv/migrations/__rename__/ "/srv/migrations/${POSTGRES_DB}"

sed -i "s/__rename__/${POSTGRES_DB}/g" "/srv/metadata/databases/databases.yaml"

mv -fv /srv/metadata/* /hasura-metadata/
mv -fv /srv/migrations/* /hasura-migrations/

echo "info: hasura-bootstrap succeeded"

exit 0

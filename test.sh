#!/usr/bin/env bash

set -e -x

docker-compose -f docker/docker-compose.yml exec -T hasura-postgres-schema-sync-test python3 -m pytest -vv /srv/test.py

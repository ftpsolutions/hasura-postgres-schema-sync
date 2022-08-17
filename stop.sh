#!/usr/bin/env bash

set -e -x

docker-compose -f docker/docker-compose.yml down --remove-orphans --volumes

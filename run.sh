#!/usr/bin/env bash

set -e -x

skip_cleanup="0"
if [[ "${1}" == '-d' ]] || [[ "${1}" == '--detach' ]]; then
  skip_cleanup=1
fi

function cleanup() {
  if [[ "${skip_cleanup}" == "1" ]]; then
    return
  fi

  ./stop.sh || true
}
trap cleanup EXIT

# shellcheck disable=SC2068
docker-compose -f docker/docker-compose.yml up --build ${@}

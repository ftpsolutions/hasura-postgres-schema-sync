import json
from sys import stderr
from typing import Any

from requests import Session

from .config import (
    HASURA_HOST,
    HASURA_PORT,
    HASURA_USER,
    HASURA_PASSWORD,
)

_SESSION = Session()

_SOURCE_NAME = "default"


def is_hasura_available() -> bool:
    with _SESSION as s:
        r = s.get(
            f"http://{HASURA_HOST}:{HASURA_PORT}/healthz",
            timeout=1,
        )

    return r.status_code == 200


def export_metadata() -> Any:
    with _SESSION as s:
        r = s.post(
            url=f"http://{HASURA_HOST}:{HASURA_PORT}/v1/query",
            headers={
                "Content-Type": "application/json",
                "X-Hasura-Role": HASURA_USER,
                "X-Hasura-Admin-Secret": HASURA_PASSWORD,
            },
            data=json.dumps(
                {
                    "type": "export_metadata",
                    "args": {},
                }
            ),
            timeout=300,
        )

    if r.status_code != 200:
        raise ValueError(r.text)

    return r.json()


def replace_metadata(metadata: Any) -> Any:
    with _SESSION as s:
        r = s.post(
            url=f"http://{HASURA_HOST}:{HASURA_PORT}/v1/query",
            headers={
                "Content-Type": "application/json",
                "X-Hasura-Role": HASURA_USER,
                "X-Hasura-Admin-Secret": HASURA_PASSWORD,
            },
            data=json.dumps(
                {
                    "type": "replace_metadata",
                    "args": metadata,
                }
            ),
            timeout=300,
        )

    if r.status_code != 200:
        print(json.dumps(r.json(), indent=4, sort_keys=True), file=stderr)
        raise ValueError("(see lump of JSON above)")

    return r.json()

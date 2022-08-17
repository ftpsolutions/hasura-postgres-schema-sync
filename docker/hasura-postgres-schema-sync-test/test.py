import datetime
import json
import os
import unittest
from uuid import UUID

from dateutil.parser import parse
from mock import ANY
from requests import Session

HASURA_HOST = os.getenv("HASURA_HOST") or "localhost"

HASURA_PORT = os.getenv("HASURA_PORT") or "8080"
HASURA_PORT = int(HASURA_PORT)

HASURA_USER = os.getenv("HASURA_USER") or "admin"

HASURA_PASSWORD = os.getenv("HASURA_PASSWORD") or "Password1"

_query = """
query ThingLocationStatByThing {
  thing {
    thing_location_stat_by_thing_uuid(limit: 10, order_by: {timestamp: desc}) {
      location
      timestamp
    }
    uuid
  }
}
"""


class HasuraPostgresSchemaSync(unittest.TestCase):
    maxDiff = None

    def setUp(self) -> None:
        self._base_url = f"http://{HASURA_HOST}:{HASURA_PORT}"
        self._headers = {
            "Content-Type": "application/json",
            "X-Hasura-Role": HASURA_USER,
            "X-Hasura-Admin-Secret": HASURA_PASSWORD,
        }

        self._session = Session()

    def test_hasura_is_healthy(self):
        with self._session as s:
            r = s.get(
                f"{self._base_url}/healthz",
                timeout=1,
            )

            self.assertEqual(200, r.status_code)

    def test_query(self):
        with self._session as s:
            r = s.post(
                f"{self._base_url}/v1/graphql",
                headers=self._headers,
                data=json.dumps(
                    {
                        "operationName": "ThingLocationStatByThing",
                        "variables": None,
                        "query": _query,
                    }
                ),
            )
            self.assertEqual(200, r.status_code)

            data = r.json()
            self.assertDictEqual(
                {
                    "data": {
                        "thing": [
                            {
                                "thing_location_stat_by_thing_uuid": [
                                    {
                                        "location": {
                                            "type": "Point",
                                            "crs": {
                                                "type": "name",
                                                "properties": {
                                                    "name": "urn:ogc:def:crs:EPSG::4236"
                                                },
                                            },
                                            "coordinates": [115.8613, -31.9523],
                                        },
                                        "timestamp": ANY,
                                    }
                                ],
                                "uuid": ANY,
                            }
                        ]
                    }
                },
                data,
            )

        raw_timestamp = data["data"]["thing"][0]["thing_location_stat_by_thing_uuid"][
            0
        ]["timestamp"]
        self.assertIsInstance(parse(raw_timestamp), datetime.datetime)

        raw_uuid = data["data"]["thing"][0]["uuid"]
        self.assertIsInstance(UUID(raw_uuid), UUID)

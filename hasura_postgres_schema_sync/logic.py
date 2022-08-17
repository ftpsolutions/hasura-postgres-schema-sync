import datetime
import json
import os
import time
import traceback
from collections import OrderedDict

from .config import POSTGRES_SCHEMA
from .hasura import (
    is_hasura_available,
    export_metadata,
    replace_metadata,
)
from .helpers import call_until_truthy_or_timeout
from .postgres import (
    get_postgres_connection,
    is_postgres_available,
    get_tables_and_views,
    get_columns_for_table_or_view,
    get_foreign_keys_for_table_or_view,
)

_healthy_path = "/tmp/hasura-postgres-schema-sync-healthy"

_last_metadata_tables_as_json = None


def _wait_for_services():
    print(f"{datetime.datetime.now().isoformat()}; waiting for Hasura...")
    call_until_truthy_or_timeout(
        method=is_hasura_available, timeout=30, message="failed to connect to Hasura"
    )
    print(f"{datetime.datetime.now().isoformat()}; done.\n")

    print(f"{datetime.datetime.now().isoformat()}; waiting for Postgres...")
    call_until_truthy_or_timeout(
        method=is_postgres_available,
        timeout=30,
        message="failed to connect to Postgres",
    )
    print(f"{datetime.datetime.now().isoformat()}; done.\n")


def _get_new_metadata_tables():
    conn = get_postgres_connection()

    all_tables_or_views = []
    for table_or_view_name, _, _ in get_tables_and_views(conn):
        columns = get_columns_for_table_or_view(table_or_view_name, conn)
        foreign_keys = get_foreign_keys_for_table_or_view(table_or_view_name, conn)
        all_tables_or_views.append((table_or_view_name, columns, foreign_keys))

    metadata_tables = OrderedDict()

    created_object_relationships = []
    for table_or_view_name, columns, foreign_keys in all_tables_or_views:
        # track the tables
        metadata_tables[table_or_view_name] = {
            "object_relationships": [],
            "array_relationships": [],
            "table": {
                "name": table_or_view_name,
                "schema": POSTGRES_SCHEMA,
            },
        }

        # track the stat table -> object table relationships (many-to-one)
        for (
            column_name,
            foreign_table_or_view_name,
            foreign_column_name,
        ) in foreign_keys:
            relationship = f"{foreign_table_or_view_name}_by_{column_name}"

            metadata_tables[table_or_view_name]["object_relationships"].append(
                {
                    "name": relationship,
                    "using": {
                        "foreign_key_constraint_on": column_name,
                    },
                }
            )

            created_object_relationships.append(
                (
                    table_or_view_name,
                    column_name,
                    foreign_table_or_view_name,
                    foreign_column_name,
                )
            )

    # track the object table -> stat table relationships (one-to-many)
    for (
        table_or_view_name,
        column_name,
        foreign_table_or_view_name,
        foreign_column_name,
    ) in created_object_relationships:
        relationship = f"{table_or_view_name}_by_{column_name}"

        metadata_tables[foreign_table_or_view_name]["array_relationships"].append(
            {
                "name": relationship,
                "using": {
                    "foreign_key_constraint_on": {
                        "column": column_name,
                        "table": {
                            "name": table_or_view_name,
                            "schema": POSTGRES_SCHEMA,
                        },
                    }
                },
            }
        )

    metadata_tables = list(metadata_tables.values())

    return metadata_tables


def _work():
    global _last_metadata_tables_as_json

    metadata_tables = _get_new_metadata_tables()
    metadata_tables_as_json = json.dumps(metadata_tables, indent=4, sort_keys=True)

    if _last_metadata_tables_as_json == metadata_tables_as_json:
        return

    print(
        f"{datetime.datetime.now().isoformat()}; state of schema from Postgres has changed; updating metadata in Hasura..."
    )

    metadata = export_metadata()
    metadata["sources"][0]["tables"] = metadata_tables

    replace_metadata(metadata)

    _last_metadata_tables_as_json = metadata_tables_as_json

    print(f"{datetime.datetime.now().isoformat()}; done.\n")


def main():
    _wait_for_services()

    while 1:
        before = datetime.datetime.now()
        deadline = before + datetime.timedelta(seconds=10)

        try:
            _work()
            if not os.path.exists(_healthy_path):
                with open(_healthy_path, "w"):
                    pass
        except Exception:
            if os.path.exists(_healthy_path):
                os.remove(_healthy_path)

            traceback.print_exc()

        after = datetime.datetime.now()
        if after > deadline:
            continue

        time.sleep((deadline - after).total_seconds())

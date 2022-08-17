from typing import Optional, List, Any, Tuple

from psycopg2 import connect

from .config import (
    POSTGRES_SCHEMA,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_DB,
)


def get_postgres_connection():
    conn = connect(
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
    )
    conn.set_session(readonly=True)
    return conn


def is_postgres_available(conn: Optional[Any] = None) -> bool:
    conn = conn or get_postgres_connection()
    with conn.cursor() as cur:
        with cur:
            cur.execute("SELECT 1;")
            return cur.fetchall()[0][0]


def get_tables_and_views(conn: Optional[Any] = None) -> List[Tuple[str, bool, bool]]:
    conn = conn or get_postgres_connection()
    with conn.cursor() as cur:
        with cur:
            cur.execute(
                f"""
SELECT * FROM (
    SELECT table_name, true, false 
    FROM information_schema.tables 
    WHERE table_schema = '{POSTGRES_SCHEMA}'
    UNION
    SELECT table_name, false, true 
    FROM information_schema.views 
    WHERE table_schema = '{POSTGRES_SCHEMA}'
) AS q
ORDER BY table_name ASC;
            """.strip()
            )
            return cur.fetchall()


def get_columns_for_table_or_view(
    table_or_view_name: str, conn: Optional[Any] = None
) -> List[Tuple[str, str]]:
    conn = conn or get_postgres_connection()
    with conn.cursor() as cur:
        with cur:
            cur.execute(
                f"""
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_schema = '{POSTGRES_SCHEMA}'
    AND table_name = '{table_or_view_name}'
ORDER BY table_name ASC;
            """.strip()
            )
            return cur.fetchall()


def get_foreign_keys_for_table_or_view(
    table_or_view_name: str, conn: Optional[Any] = None
) -> List[Tuple]:
    conn = conn or get_postgres_connection()
    with conn.cursor() as cur:
        with cur:
            cur.execute(
                f"""
SELECT 
    kcu.column_name, 
    ccu.table_name AS foreign_table_name, 
    ccu.column_name AS foreign_column_name
FROM information_schema.table_constraints AS tc
JOIN information_schema.key_column_usage AS kcu
    ON tc.constraint_name = kcu.constraint_name 
    AND tc.table_schema = kcu.table_schema
JOIN information_schema.constraint_column_usage AS ccu
    ON ccu.constraint_name = tc.constraint_name 
    AND ccu.table_schema = tc.table_schema
WHERE 
    tc.constraint_type = 'FOREIGN KEY' 
    AND tc.table_name = '{table_or_view_name}'
    AND tc.table_schema = '{POSTGRES_SCHEMA}'
ORDER BY tc.table_name ASC;     
    """.strip()
            )
            return cur.fetchall()

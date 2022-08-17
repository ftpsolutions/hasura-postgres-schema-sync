import os

POSTGRES_SCHEMA = os.getenv("POSTGRES_SCHEMA") or None
if not POSTGRES_SCHEMA:
    raise ValueError("POSTGRES_SCHEMA env var not set")

POSTGRES_HOST = os.getenv("POSTGRES_HOST") or None
if not POSTGRES_HOST:
    raise ValueError("POSTGRES_HOST env var not set")

POSTGRES_PORT = os.getenv("POSTGRES_PORT") or None
if not POSTGRES_PORT:
    raise ValueError("POSTGRES_HOST env var not set")
POSTGRES_PORT = int(POSTGRES_PORT)

POSTGRES_USER = os.getenv("POSTGRES_USER") or None
if not POSTGRES_USER:
    raise ValueError("POSTGRES_USER env var not set")

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD") or None
if not POSTGRES_PASSWORD:
    raise ValueError("POSTGRES_PASSWORD env var not set")

POSTGRES_DB = os.getenv("POSTGRES_DB") or None
if not POSTGRES_DB:
    raise ValueError("POSTGRES_DB env var not set")

HASURA_HOST = os.getenv("HASURA_HOST") or None
if not HASURA_HOST:
    raise ValueError("HASURA_HOST env var not set")

HASURA_PORT = os.getenv("HASURA_PORT") or None
if not HASURA_PORT:
    raise ValueError("HASURA_PORT env var not set")
HASURA_PORT = int(HASURA_PORT)

HASURA_USER = os.getenv("HASURA_USER") or None
if not HASURA_USER:
    raise ValueError("HASURA_USER env var not set")

HASURA_PASSWORD = os.getenv("HASURA_PASSWORD") or None
if not HASURA_PASSWORD:
    raise ValueError("HASURA_PASSWORD env var not set")

import os
from pathlib import Path
import psycopg
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / ".env.development"
if not env_path.exists():
    env_path = BASE_DIR / ".env"

load_dotenv(dotenv_path=env_path)

db_name = os.getenv("DB_NAME", "django_catalog_db")
db_user = os.getenv("DB_USER", "postgres")
db_password = os.getenv("DB_PASSWORD", "")
db_host = os.getenv("DB_HOST", "localhost")
db_port = os.getenv("DB_PORT", "5432")

conn_str = f"host={db_host} port={db_port} user={db_user} password={db_password} dbname=postgres"

with psycopg.connect(conn_str, autocommit=True) as conn:
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
        if not cur.fetchone():
            cur.execute(f'CREATE DATABASE "{db_name}"')

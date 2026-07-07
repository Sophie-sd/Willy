#!/usr/bin/env bash
set -euo pipefail

echo "==> [entrypoint] Starting ZooWilly"
cd /app

# ─── 1. WAIT FOR DATABASE
echo "==> Waiting for PostgreSQL..."
python <<'WAIT_DB'
import os, sys, time

db_url = os.environ.get("DATABASE_URL", "")
if not db_url:
    print("==> DATABASE_URL not set, skipping DB wait")
    sys.exit(0)

print(f"==> Connecting to DB...")
import psycopg

for attempt in range(30):
    try:
        psycopg.connect(db_url).close()
        print(f"==> DB ready (attempt {attempt + 1})")
        sys.exit(0)
    except Exception as e:
        print(f"  {attempt + 1}/30: {type(e).__name__}")
        time.sleep(2)

print("==> FATAL: DB not ready after 60s")
sys.exit(1)
WAIT_DB

# ─── 2. MIGRATIONS
echo "==> Running migrations..."
python manage.py migrate --noinput --verbosity 1

echo "==> Importing page content (idempotent)..."
python manage.py migrate_page_content

# ─── 3. STATIC FILES
echo "==> Collecting static files..."
python manage.py collectstatic --noinput --verbosity 0

_count=$(find "${STATIC_ROOT:-/app/staticfiles}" -type f 2>/dev/null | wc -l | tr -d ' ')
echo "==> Static files: ${_count}"

if [ "${_count:-0}" -lt 5 ]; then
    echo "==> ERROR: Static files not collected (count: ${_count})"
    exit 1
fi

# ─── 4. ENSURE VOLUME DIRS
mkdir -p /app/staticfiles /app/media
touch /app/staticfiles/.keep /app/media/.keep

echo "==> All checks passed. Starting: $*"
exec "$@"

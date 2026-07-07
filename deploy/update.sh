#!/usr/bin/env bash
# Production deploy — run on server: bash deploy/update.sh
set -euo pipefail

cd "$(dirname "$0")/.."

echo "==> Resetting local changes to tracked product images (if any)..."
git checkout -- static/images/products/*.jpg 2>/dev/null || true

echo "==> Pulling latest code..."
git pull origin main

echo "==> Building web image..."
docker compose build --no-cache web

echo "==> Starting containers..."
docker compose up -d

echo "==> Waiting for web container..."
sleep 5

echo "==> Migrations and content import..."
docker compose exec -T web python manage.py migrate --noinput
docker compose exec -T web python manage.py migrate_page_content

echo "==> Verifying unfold..."
docker compose exec -T web python -c "import unfold; print('unfold', unfold.__version__)"
docker compose exec -T web python manage.py check

echo "==> Done. Open /admin/ in browser (hard refresh)."

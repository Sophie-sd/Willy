#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────────
# Let's Encrypt bootstrap for zoowilly.com.ua
# Run once on fresh server BEFORE docker-compose up
#
# Usage:
#   chmod +x deploy/init-ssl.sh
#   ./deploy/init-ssl.sh
# ─────────────────────────────────────────────────────────────────────────────
set -euo pipefail

DOMAIN="zoowilly.com.ua"
EMAIL="oksanadaragan9@gmail.com"
CERTBOT_CONF="./certbot/conf"
CERTBOT_WWW="./certbot/www"

echo "==> Creating required directories..."
mkdir -p "$CERTBOT_CONF/live/$DOMAIN"
mkdir -p "$CERTBOT_WWW"

echo "==> Creating temporary self-signed certificate (for nginx initial start)..."
docker run --rm \
    -v "$CERTBOT_CONF:/etc/letsencrypt" \
    certbot/certbot:latest \
    certonly --staging \
    --webroot -w /var/www/certbot \
    -d "$DOMAIN" -d "www.$DOMAIN" \
    --email "$EMAIL" \
    --agree-tos \
    --no-eff-email \
    --force-renewal \
    2>/dev/null || true

# Create dummy cert so nginx can start
if [ ! -f "$CERTBOT_CONF/live/$DOMAIN/fullchain.pem" ]; then
    echo "==> Generating dummy self-signed cert to bootstrap nginx..."
    openssl req -x509 -nodes -newkey rsa:2048 -days 1 \
        -keyout "$CERTBOT_CONF/live/$DOMAIN/privkey.pem" \
        -out    "$CERTBOT_CONF/live/$DOMAIN/fullchain.pem" \
        -subj "/CN=$DOMAIN" 2>/dev/null
fi

# Download recommended TLS params
if [ ! -f "$CERTBOT_CONF/options-ssl-nginx.conf" ]; then
    echo "==> Downloading TLS options..."
    curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf \
        > "$CERTBOT_CONF/options-ssl-nginx.conf"
fi

if [ ! -f "$CERTBOT_CONF/ssl-dhparams.pem" ]; then
    echo "==> Generating DH params (takes ~30s)..."
    openssl dhparam -out "$CERTBOT_CONF/ssl-dhparams.pem" 2048 2>/dev/null
fi

echo "==> Starting nginx (with dummy cert)..."
docker compose up -d nginx

echo "==> Waiting for nginx to start..."
sleep 5

echo "==> Requesting real Let's Encrypt certificate..."
docker compose run --rm certbot \
    certonly --webroot \
    -w /var/www/certbot \
    -d "$DOMAIN" -d "www.$DOMAIN" \
    --email "$EMAIL" \
    --agree-tos \
    --no-eff-email \
    --force-renewal

echo "==> Reloading nginx with real certificate..."
docker compose exec nginx nginx -s reload

echo "==> SSL bootstrap complete!"
echo "==> zoowilly.com.ua is now served over HTTPS"

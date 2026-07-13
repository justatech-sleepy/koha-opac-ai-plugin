#!/usr/bin/env bash

set -e

PROJECT="$HOME/koha-opac-ai-assistant"

echo "========================================"
echo " Koha OPAC AI Assistant Deployment"
echo "========================================"

echo "[1/5] Copying CSS..."
sudo cp "$PROJECT/frontend/css/"*.css \
/usr/share/koha/opac/htdocs/opac-tmpl/bootstrap/css/

echo "[2/5] Copying JavaScript..."
sudo cp "$PROJECT/frontend/js/"*.js \
/usr/share/koha/opac/htdocs/opac-tmpl/bootstrap/js/

echo "[3/5] Copying Data..."
sudo mkdir -p /usr/share/koha/opac/htdocs/opac-tmpl/bootstrap/data
sudo cp "$PROJECT/frontend/data/"*.json \
/usr/share/koha/opac/htdocs/opac-tmpl/bootstrap/data/

echo "[4/5] Restarting Apache..."
sudo systemctl restart apache2

echo "[5/5] Restarting Plack..."
sudo koha-plack --restart library

echo ""
echo "========================================"
echo " Deployment Successful!"
echo "========================================"

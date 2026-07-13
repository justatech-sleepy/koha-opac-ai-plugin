#!/usr/bin/env bash

set -e

PROJECT="${PROJECT_DIR:-$HOME/koha-opac-ai-assistant}"
KOHA_THEME_DIR="${KOHA_THEME_DIR:-/usr/share/koha/opac/htdocs/opac-tmpl/bootstrap}"
KOHA_INSTANCE="${KOHA_INSTANCE:-library}"

echo "========================================"
echo " Koha OPAC AI Assistant Deployment"
echo "========================================"
echo "Project Dir: $PROJECT"
echo "Theme Dir:   $KOHA_THEME_DIR"
echo "Instance:    $KOHA_INSTANCE"
echo "========================================"

echo "[1/5] Copying CSS..."
sudo cp "$PROJECT/frontend/css/"*.css "$KOHA_THEME_DIR/css/"

echo "[2/5] Copying JavaScript..."
sudo cp "$PROJECT/frontend/js/"*.js "$KOHA_THEME_DIR/js/"

echo "[3/5] Copying Data..."
sudo mkdir -p "$KOHA_THEME_DIR/data"
sudo cp "$PROJECT/frontend/data/"*.json "$KOHA_THEME_DIR/data/" || true

echo "[4/5] Restarting Apache..."
sudo systemctl restart apache2

echo "[5/5] Restarting Plack..."
sudo koha-plack --restart "$KOHA_INSTANCE"

echo ""
echo "========================================"
echo " Deployment Successful!"
echo "========================================"

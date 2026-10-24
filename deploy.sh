#!/bin/sh
set -eu

TARGET="${1:-}"

case "$TARGET" in
  blue|green) ;;
  *)
    echo "Uso: ./deploy.sh blue|green"
    exit 1
    ;;
esac

VERSION="1.3.0"
[ "$TARGET" = "green" ] && VERSION="1.4.0"

echo "Validando health y readiness de $TARGET..."

curl -fsS "http://127.0.0.1:$(
  [ "$TARGET" = "blue" ] && echo 8001 || echo 8002
)/health"

curl -fsS "http://127.0.0.1:$(
  [ "$TARGET" = "blue" ] && echo 8001 || echo 8002
)/readiness"

echo
echo "Conmutando trafico hacia $TARGET ($VERSION)..."
printf '{"active":"%s"}\n' "$TARGET" > active.json

echo "Version activa:"
curl -fsS http://127.0.0.1:8000/version
echo

#!/usr/bin/env bash
set -euo pipefail
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

DEV=${1:-}
if [ "$DEV" = "--dev" ]; then
  export HTTP_PORT=${HTTP_PORT:-8082}
  export WS_PORT=${WS_PORT:-8767}
fi


HTTP_PORT=${HTTP_PORT:-8080}
WS_PORT=${WS_PORT:-8765}
if lsof -Pi :$HTTP_PORT -sTCP:LISTEN -t >/dev/null 2>&1; then HTTP_PORT=$((HTTP_PORT+1)); fi
if lsof -Pi :$WS_PORT   -sTCP:LISTEN -t >/dev/null 2>&1; then WS_PORT=$((WS_PORT+1)); fi
export HTTP_PORT WS_PORT

python3 dashboard/server.py &
DASH_PID=$!
sleep 1

trap 'echo; echo "Stopping..."; kill $DASH_PID 2>/dev/null || true; exit 0' INT TERM

while true; do
  python3 vyktor.py || true
  sleep 2
done


echo ""
echo "=============================================================="
echo "© 2025 NERON Intelligence Systems — VYKTOR v1.3.2 DEV (HERMES)"
echo "Neural Evolution Engine • Dashboard: http://${HTTP_HOST:-127.0.0.1}:${HTTP_PORT:-8081}"
echo "=============================================================="
echo ""


export VYKTOR_VERSION="v1.3.3 DEV (DASH)"

echo ""
echo "=============================================================="
echo "© 2025 NERON Intelligence Systems — VYKTOR v1.3.3 DEV (DASH)"
echo "Neural Evolution Engine • Dashboard: http://${HTTP_HOST:-127.0.0.1}:${HTTP_PORT:-8081}"
echo "=============================================================="
echo ""

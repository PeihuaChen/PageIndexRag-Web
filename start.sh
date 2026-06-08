#!/bin/bash

echo ""
echo "========================================"
echo "  PageIndex Web - Starting..."
echo "========================================"
echo ""

cd "$(dirname "$0")"

cleanup() {
    echo ""
    echo "Stopping server..."
    [ -n "$BACKEND_PID" ] && kill "$BACKEND_PID" 2>/dev/null
    wait 2>/dev/null
    echo "Server stopped."
    exit 0
}

trap cleanup SIGINT SIGTERM

echo "Starting server on http://0.0.0.0:8001 ..."
python -m uvicorn server.main:app --host 0.0.0.0 --port 8001 &
BACKEND_PID=$!

sleep 2

echo ""
echo "========================================"
echo "  Web UI:  http://0.0.0.0:8001"
echo "  API:     http://0.0.0.0:8001/api"
echo "  Health:  http://0.0.0.0:8001/api/health"
echo "========================================"
echo ""
echo "Press Ctrl+C to stop the server..."

wait

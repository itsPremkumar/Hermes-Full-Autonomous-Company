#!/usr/bin/env bash
# Paperclip 24/7 watchdog — checks if server is alive, restarts if down.
# Run via Hermes cron: cronjob(action='create', name='paperclip-watchdog',
#   schedule='5m', script='watchdog.sh', no_agent=true)
# Place in ~/.hermes/scripts/watchdog.sh

HEALTH_URL="${PAPERCLIP_HEALTH_URL:-http://localhost:3100/api/health}"
SERVER_BAT="${PAPERCLIP_SERVER_BAT:-C:/paperclip-company/run-server.bat}"

if ! curl -sf "$HEALTH_URL" > /dev/null 2>&1; then
  echo "[$(date)] Paperclip server DOWN — restarting..."
  cd "$(dirname "$SERVER_BAT")" && cmd.exe /c "$SERVER_BAT" > /dev/null 2>&1 &
  echo "[$(date)] Restart initiated — PID=$!"
else
  echo "[$(date)] Paperclip server UP — OK"
fi

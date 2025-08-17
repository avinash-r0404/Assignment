#!/usr/bin/env bash
set -euo pipefail

# Simple smoke test: spin up compose, hit health, then stop.
docker compose up -d --build

echo "Waiting for AI backend health..."
for i in {1..30}; do
  if curl -sf http://localhost:8000/health >/dev/null; then
    echo "AI backend healthy."
    break
  fi
  sleep 2
done

echo "Upload a sample image manually at http://localhost:8080"
echo "When done testing: docker compose down"

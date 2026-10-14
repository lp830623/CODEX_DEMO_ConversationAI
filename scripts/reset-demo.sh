#!/usr/bin/env sh
set -eu
port="${DEMO_PORT:-8102}"
curl --fail --silent --show-error -X POST "http://127.0.0.1:$port/api/reset" -H 'Content-Type: application/json' -d '{}'
printf '\n'

#!/usr/bin/env bash

set -ef

cli_help() {
  cli_name=${0##*/}
  echo "
$cli_name
Optimizer Service entrypoint cli
Usage: $cli_name [command]
Commands:
  runserver     Start the FastAPI server
  *             Help
"
  exit 1
}

case "$1" in
  runserver)
    echo "Starting Optimizer Service..."
    exec uvicorn app.main:app --host 0.0.0.0 --port 8002 --reload
    ;;
  *)
    cli_help
    ;;
esac

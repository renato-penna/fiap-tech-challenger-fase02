#!/usr/bin/env bash

set -ef

cli_help() {
  cli_name=${0##*/}
  echo "
$cli_name
Frontend Service entrypoint cli
Usage: $cli_name [command]
Commands:
  runserver     Start the Streamlit server
  *             Help
"
  exit 1
}

case "$1" in
  runserver)
    exec streamlit run app/main.py --server.port=8501 --server.address=0.0.0.0
    ;;
  *)
    cli_help
    ;;
esac

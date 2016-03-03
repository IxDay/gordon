#!/bin/bash

read -r -d '' HELP <<'EOF'
Usage: helper.sh [COMMAND or SQL FILE]
By default if no COMMAND or SQL FILE is provided, run the plsql command
against the rulzurdb database

  help                  print this message

  create_db             create rulzurdb and rulzurdb_test and fill up rulzurdb
                        with some sample

  reinitialize          drop rulzurdb and rulzurdb_test data then fill up
                        rulzurdb again.

  full_reinitialize     drop rulzurdb and rulzurdb_test databases and run the
                        create_db command.

  SQL FILE              execute the file against the rulzurdb database

EOF

set -e

CMD="psql -U rulzurdb -h db"

case "$1" in
"help")
    echo "$HELP"
    ;;
"create_db")
    eval "$CMD -d template1 -c 'CREATE DATABASE rulzurdb'"
    eval "$CMD -d template1 -c 'CREATE DATABASE rulzurdb_test'"

    eval "$CMD -d rulzurdb -a -f utils/create_tables.sql"
    eval "$CMD -d rulzurdb_test -a -f utils/create_tables.sql"

    eval "$CMD -d rulzurdb -a -f utils/init.sql"
    ;;
"reinitialize")
    eval "$CMD -d rulzurdb -a -f utils/clean_all.sql"
    eval "$CMD -d rulzurdb -a -f utils/init.sql"
    ;;
"full_reinitialize")
    eval "$CMD -d template1 -c 'DROP DATABASE IF EXISTS rulzurdb'"
    eval "$CMD -d template1 -c 'DROP DATABASE IF EXISTS rulzurdb_test'"
    exec $(readlink -f "$0") create_db
    ;;
*)
    FILE_OPT=""

    if [ ! -z "$1" ]; then
        FILE_OPT="-a -f $1"
    fi
    eval "$CMD -d rulzurdb $FILE_OPT"
    ;;
esac

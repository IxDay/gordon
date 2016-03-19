#!/bin/bash

read -r -d '' HELP <<'EOF'
Usage: helper.sh [COMMAND or SQL FILE]
By default if no COMMAND or SQL FILE is provided, run the plsql command
against the potato database

  help                  print this message

  create_db             create potato and potato_test and fill up potato
                        with some sample

  reinitialize          drop potato and potato_test data then fill up
                        potato again.

  full_reinitialize     drop potato and potato_test databases and run the
                        create_db command.

  SQL FILE              execute the file against the potato database

EOF

set -e

CMD="psql -U potato -h db"

case "$1" in
"help")
    echo "$HELP"
    ;;
"create_db")
    eval "$CMD -d template1 -c 'CREATE DATABASE potato'"
    eval "$CMD -d template1 -c 'CREATE DATABASE potato_test'"

    eval "$CMD -d potato -a -f utils/create_tables.sql"
    eval "$CMD -d potato_test -a -f utils/create_tables.sql"

    eval "$CMD -d potato -a -f utils/init.sql"
    ;;
"reinitialize")
    eval "$CMD -d potato -a -f utils/clean_all.sql"
    eval "$CMD -d potato -a -f utils/init.sql"
    ;;
"full_reinitialize")
    eval "$CMD -d template1 -c 'DROP DATABASE IF EXISTS potato'"
    eval "$CMD -d template1 -c 'DROP DATABASE IF EXISTS potato_test'"
    exec $(readlink -f "$0") create_db
    ;;
*)
    FILE_OPT=""

    if [ ! -z "$1" ]; then
        FILE_OPT="-a -f $1"
    fi
    eval "$CMD -d potato $FILE_OPT"
    ;;
esac

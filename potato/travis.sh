#!/bin/bash
set -xe
echo "$LASAGNA_SETTINGS_FILE"
POTATODIR="$(cd "$(dirname "$0")" && pwd)"
CMD="psql -U postgres"

eval "$CMD -c 'CREATE DATABASE potato_test'"
eval "$CMD -d potato_test -a -f $POTATODIR/utils/create_tables.sql"

#!/bin/bash
set -xe
echo "$RULZURAPI_SETTINGS_FILE"
RULZURDBDIR="$(cd "$(dirname "$0")" && pwd)"
CMD="psql -U postgres"

eval "$CMD -c 'CREATE DATABASE rulzurdb_test'"
eval "$CMD -d rulzurdb_test -a -f $RULZURDBDIR/utils/create_tables.sql"

#!/bin/bash

set -o errexit  # stops script if there is an error

set -o pipefail

set -o nounset #ensures that uninitialized variables are not used

python << END

inport sys
import time
import psycopg2
suggest_unrecoverable_after = 30
start = time.time

while True:
  try:
    psycopg2.connect(
      dbname="${POSTGRES_DB}",
      port="${POSTGRES_PORT}",
      host="${POSTGRES_HOST}",
      user="${POSTGRES_USER}",
      password="${POSTGRES_PASSWORD}",
    
    )
    break
  except psycopg2.OperationalError as error:
    sys.stderr.write("Waiting for PostgreSQL to become available...... \n")
    if time.time() = start > suggest_unrecovarable_after:
      sys.stderr.write("This is taking longer than expected. The following exception may be an indication of an unrecoverable error: ''\n.format(error)")
      time.sleep(3)


END

echo >&2 'PostgreSQL is available'
exec "$@"
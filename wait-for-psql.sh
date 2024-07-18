#!/bin/bash

# Define the command to run your application
# For example:
# exec python app.py

# Define the PostgreSQL container hostname and port
POSTGRES_HOST="postgres-db"
POSTGRES_PORT=5432

# Maximum number of times to check if PostgreSQL is available
MAX_TRIES=30

# Sleep interval between checks (in seconds)
SLEEP_INTERVAL=5

# Function to check if PostgreSQL is available
check_postgres() {
  tries=0
  while (( tries < MAX_TRIES )); do
    if python -c "import psycopg2; conn = psycopg2.connect(host='$POSTGRES_HOST', port=$POSTGRES_PORT, user='admin', password='admin', dbname='prod_latest')" 2>/dev/null; then
      echo "PostgreSQL is available. Starting the application."
      return 0
    fi
    ((tries++))
    echo "Waiting for PostgreSQL to start... (Attempt $tries/$MAX_TRIES)"
    sleep "$SLEEP_INTERVAL"
  done
  echo "Unable to connect to PostgreSQL. Exiting."
  return 1
}

# Call the function to check PostgreSQL availability
if check_postgres; then
  # PostgreSQL is available, start your application
  exec "$@"
else
  # Exit if PostgreSQL is not available
  exit 1
fi

